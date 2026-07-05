import streamlit as st
import requests

st.set_page_config(page_title="Career Advisor AI", page_icon="🎯")

st.title("🎯 Career Advisor AI")
st.caption("An explainable, affect-aware AI career advisor")

API_URL = "https://career-advisor-ai-backend.onrender.com/advise"
# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Tell me about your skills, interests, or career worries...")

if user_input:
    # Show user message immediately
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                res = requests.post(
                    API_URL,
                    json={
                        "message": user_input,
                        "history": st.session_state.messages[:-1]  # exclude the just-added user message to avoid duplication
                    },
                    timeout=60
                )
                res.raise_for_status()
                data = res.json()

                response_text = data["response"]
                affect = data["affect"]

                st.markdown(response_text)
                st.caption(f"Detected tone: *{affect}*")

                st.session_state.messages.append(
                    {"role": "assistant", "content": response_text}
                )
            except Exception as e:
                error_msg = f"Something went wrong: {e}"
                st.error(error_msg)
                st.session_state.messages.append(
                    {"role": "assistant", "content": error_msg}
                )