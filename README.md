\# Career Advisor AI



\*\*🔗 Live Demo:\*\* \[career-advisor-ai-n5mdufdvfvevq8ynkef3pk.streamlit.app](https://career-advisor-ai-n5mdufdvfvevq8ynkef3pk.streamlit.app)

\*\*⚙️ Backend API:\*\* \[career-advisor-ai-backend.onrender.com](https://career-advisor-ai-backend.onrender.com)



> Note: The backend is hosted on Render's free tier, which spins down after \~15 minutes of inactivity. The first message after inactivity may take 30-60 seconds to respond while it wakes up.



An explainable, affect-aware AI career advisor built with LangGraph, RAG, and LLMs (via Groq/LLaMA 3.3).



\## Problem



Existing AI career recommendation systems fall into two separate camps:

\- \*\*Explainable recommenders\*\* (e.g., grounded job-matching systems) provide justified recommendations but ignore the user's emotional state.

\- \*\*Affect-aware chatbots\*\* detect and respond to user emotion but aren't grounded in real occupational data, risking generic or hallucinated advice.



This project combines both: grounded, explainable recommendations \*\*and\*\* emotionally-adapted delivery, in a single pipeline.



\## Architecture



User message

&#x20;  -> Distress check (safety guardrail)

&#x20;  -> Affect detection (confident / anxious / confused / undecided / neutral)

&#x20;  -> Profile extraction (skills, interests, constraints, goals)

&#x20;  -> Sufficient-info check (asks clarifying question if too little context)

&#x20;  -> RAG retrieval (ChromaDB over 1016 O\*NET occupations, enriched with Holland Code interest traits)

&#x20;  -> Grounded explanation generation (cites specific retrieved facts)

&#x20;  -> Affect-adapted response composition (tone/structure shaped by detected affect)



\## Tech Stack



\- \*\*Backend\*\*: FastAPI, LangGraph, ChromaDB

\- \*\*LLM\*\*: LLaMA 3.3 70B via Groq API

\- \*\*Frontend\*\*: Streamlit

\- \*\*Data\*\*: O\*NET 30.3 Database (Occupation Data, Essential Skills, Career Interest Types)



\## Setup



1\. Clone the repo and create a virtual environment:

python -m venv venv

venv\\Scripts\\activate

pip install -r backend/requirements.txt

2\. Add your Groq API key to `backend/.env`:

GROQ\_API\_KEY=your\_key\_here

3\. Build the knowledge base (requires O\*NET text files placed in `backend/app/data/onet\_raw/`):

cd backend/app/data

python prepare\_kb.py

python build\_vectorstore.py

4\. Run the backend:

cd backend

uvicorn app.main:app --reload

5\. Run the frontend (in a separate terminal):

cd frontend

streamlit run streamlit\_app.py



\## Evaluation



See `backend/evaluation\_rubric.md`, `backend/baseline\_outputs.txt`, and `backend/system\_outputs.txt` for a comparison between this system and a plain, ungrounded LLM baseline across affect states.



\## Known Limitations



\- Retrieval uses a lightweight sentence-embedding model (all-MiniLM-L6-v2) which can anchor on surface lexical overlap over semantic meaning in some cases (e.g., queries about "helping people" can under-rank counseling/therapy roles in favor of literal title matches). Documented as a direction for future work (stronger embedding model or re-ranking step).

\- Affect classification is more reliable at emotional extremes (clear anxiety, clear confidence) than for plainly neutral/informational messages.

\- Evaluation was self-scored by the author using a defined rubric; independent human validation was not performed due to project scope.



\## Author



Swarnali Ghosh



