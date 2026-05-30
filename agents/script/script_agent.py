from llm.groq_provider import generate

def generate_script(topic: str) -> str:
    prompt = f"""
    You are a medical education script writer.

    Create a clear, engaging YouTube script on:
    {topic}

    Structure:
    1. Hook (attention grabbing)
    2. Simple explanation
    3. Real-life example
    4. Conclusion

    Keep language simple and visual.
    """

    return generate(prompt) # type: ignore