import os
import json
from .state import AdvisorState
from app.llm_client import call_llm

# Resolve chroma_db path relative to this file's location, not the working directory
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "..", "chroma_db")

AFFECT_LABELS = ["confident", "anxious", "confused", "undecided", "neutral"]

def has_sufficient_info(profile: dict) -> bool:
    return bool(
        profile.get("skills") or
        profile.get("interests") or
        profile.get("stated_goal")
    )


def clarify_response(state: AdvisorState) -> AdvisorState:
    state["final_response"] = (
        "I'd love to help you explore career options! Could you tell me a bit more — "
        "for example, what subjects or activities you enjoy, or anything you're good at? "
        "Even a rough idea helps me give you better suggestions."
    )
    return state

def check_for_distress(state: AdvisorState) -> AdvisorState:
    prompt = f"""Does this message contain language suggesting the person may be in emotional distress,
expressing hopelessness, self-harm ideation, or a mental health crisis — as opposed to ordinary
career-related stress or indecision?

Message: "{state['user_message']}"

Respond with only one word: YES or NO."""

    result = call_llm(prompt, temperature=0.0).strip().upper()
    state["is_distress"] = (result == "YES")
    return state


def detect_affect(state: AdvisorState) -> AdvisorState:
    prompt = f"""Classify the emotional/confidence state expressed in this message about career decisions.
Choose exactly one label from this list: {", ".join(AFFECT_LABELS)}.

Use these definitions and examples to guide your choice:
- anxious: expresses overwhelm, worry, stress, or fear about the future (e.g., "everything feels overwhelming", "I'm scared I'll fail", "this is stressing me out")
- confused: expresses not understanding options or lacking information/clarity (e.g., "I don't understand what these jobs actually involve", "what does this even mean")
- undecided: expresses being torn between two or more specific, named options (e.g., "I can't decide between X and Y")
- confident: expresses clear direction or certainty (e.g., "I know I want to do X")
- neutral: none of the above apply strongly; a plain factual statement

Message: "{state['user_message']}"

Respond with only the single label, nothing else."""

    result = call_llm(prompt, temperature=0.0)
    label = result.strip().lower()

    if label not in AFFECT_LABELS:
        label = "neutral"

    state["affect"] = label
    return state


def extract_profile(state: AdvisorState) -> AdvisorState:
    history_text = ""
    if state.get("conversation_history"):
        history_text = "\n".join(
            [f"{turn['role']}: {turn['content']}" for turn in state["conversation_history"]]
        )

    prompt = f"""Extract structured career-relevant information from this conversation.
Consider both the conversation history (for context) and the latest message (primary focus).
Return ONLY valid JSON, no other text, in this exact format:

{{
  "skills": ["list of skills or strengths mentioned or implied, across the whole conversation"],
  "interests": ["list of interests, subjects, or activities mentioned, across the whole conversation"],
  "constraints": ["list of constraints like location, budget, time, education level — empty list if none mentioned"],
  "stated_goal": "any explicit career goal mentioned, or null if none"
}}

Conversation history:
{history_text if history_text else "(no prior messages)"}

Latest message: "{state['user_message']}"
"""

    result = call_llm(prompt, temperature=0.0)

    try:
        cleaned = result.strip().strip("```json").strip("```").strip()
        profile = json.loads(cleaned)
    except json.JSONDecodeError:
        profile = {
            "skills": [],
            "interests": [],
            "constraints": [],
            "stated_goal": None,
            "raw_message": state["user_message"]
        }

    state["extracted_profile"] = profile
    return state


def retrieve_careers(state: AdvisorState) -> AdvisorState:
    import chromadb
    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_collection("careers")

    profile = state["extracted_profile"]
    query_parts = profile.get("skills", []) + profile.get("interests", [])
    query_text = ", ".join(query_parts) if query_parts else state["user_message"]

    results = collection.query(
        query_texts=[query_text],
        n_results=5
    )

    careers = []
    for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
        careers.append({"title": meta["title"], "text": doc})

    state["retrieved_careers"] = careers
    return state


def generate_explanation(state: AdvisorState) -> AdvisorState:
    profile = state["extracted_profile"]
    careers = state["retrieved_careers"]

    careers_context = "\n\n".join(
        [f"- {c['title']}: {c['text']}" for c in careers]
    )

    prompt = f"""You are a career advisor. Based on the user's profile below, explain why EACH of the retrieved careers could be a good fit.

Your explanation for each career MUST reference a specific fact from that career's description or skills (quoted from the text below) — do not give generic reasoning that could apply to any career.

User profile:
- Skills: {profile.get('skills', [])}
- Interests: {profile.get('interests', [])}
- Constraints: {profile.get('constraints', [])}
- Stated goal: {profile.get('stated_goal')}

Retrieved careers:
{careers_context}

For each career, write 1-2 sentences explaining the fit, grounded in specific facts from its description above. Format as a numbered list with the career title bolded."""

    explanation = call_llm(prompt, temperature=0.3)
    state["explanation"] = explanation
    return state


def compose_response(state: AdvisorState) -> AdvisorState:
    affect = state["affect"]
    explanation = state["explanation"]

    tone_instructions = {
        "anxious": (
            "The user is feeling anxious or overwhelmed. Rewrite the explanation below to be "
            "reassuring and calm. Lead with validation that career uncertainty is normal, "
            "simplify the options into a smaller, less overwhelming set of next steps, and "
            "avoid dense lists — use a warmer, conversational tone."
        ),
        "confused": (
            "The user seems confused or unclear about direction. Rewrite the explanation below "
            "to be extra clear and structured, breaking down WHY each option is being suggested "
            "in simple terms, and explicitly clarify any jargon."
        ),
        "undecided": (
            "The user is torn between options. Rewrite the explanation below to help them compare "
            "trade-offs directly and constructively — highlight what distinguishes the top options "
            "from each other rather than just listing facts about each independently."
        ),
        "confident": (
            "The user is confident and decisive. Rewrite the explanation below to be direct and "
            "efficient — skip reassurance, get straight to the substantive comparison, and include "
            "concrete next steps or action items."
        ),
        "neutral": (
            "Rewrite the explanation below in a clear, friendly, professional tone."
        ),
    }

    instruction = tone_instructions.get(affect, tone_instructions["neutral"])

    prompt = f"""{instruction}

Original explanation:
{explanation}

Rewrite it now, preserving all factual content and citations, but adapting the delivery as instructed."""

    final_response = call_llm(prompt, temperature=0.4)
    state["final_response"] = final_response
    return state