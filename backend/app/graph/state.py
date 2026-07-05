from typing import TypedDict, List, Optional

class AdvisorState(TypedDict):
    user_message: str
    conversation_history: List[dict]
    is_distress: Optional[bool]
    affect: Optional[str]          # e.g. "confident", "anxious", "confused", "undecided"
    extracted_profile: Optional[dict]   # skills, interests, constraints
    retrieved_careers: Optional[List[dict]]
    explanation: Optional[str]
    final_response: Optional[str]