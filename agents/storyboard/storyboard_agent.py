from llm.groq_provider import generate

def create_storyboard(script: str):

    prompt = f"""
    You are a medical animation director.

    Convert script into storyboard.

    IMPORTANT RULES:
    - Return ONLY valid JSON array
    - NO markdown
    - NO triple backticks
    - NO explanation

    Each scene must include:
    - scene_number
    - visual_description
    - voice_over_text
    - on_screen_text
    - camera_motion

    SCRIPT:
    {script}
    """

    return generate(prompt)

 # ✅ Convert string → real JSON
    try:
        return json.loads(response)
    except Exception as e:
        return {
            "error": "Invalid JSON from LLM",
            "raw_output": response
        }