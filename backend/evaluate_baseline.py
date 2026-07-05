from app.llm_client import call_llm

def baseline_response(user_message: str) -> str:
    prompt = f"""You are a career advisor. Respond to this message with career recommendations.

Message: "{user_message}"
"""
    return call_llm(prompt, temperature=0.5)

if __name__ == "__main__":
    test_messages = [
        "I have no idea what I'm doing with my life, everything feels overwhelming, but I do enjoy working with numbers",
        "I'm pretty confident I want to go into software engineering",
        "I can't decide between medicine and engineering, both seem equally good",
        "I don't really understand what a data analyst actually does day to day",
    ]

    for msg in test_messages:
        print(f"\n{'='*80}\nMessage: {msg}\n{'='*80}")
        print(baseline_response(msg))