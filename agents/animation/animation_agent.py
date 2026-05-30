import json
import re
from llm.groq_provider import generate


def extract_json(text: str):
    """
    Robust JSON extractor for messy LLM output
    """
    # remove markdown code blocks
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)

    # try to find JSON array
    match = re.search(r"\[.*\]", text, re.DOTALL)
    if not match:
        return []

    try:
        return json.loads(match.group(0))
    except Exception:
        return []


def generate_animation(storyboard: list):
    """
    Converts storyboard → animation plan (engine-ready JSON)
    """

    schema = """
Each scene MUST include:

{
  "scene_number": number,
  "elements": [
    {
      "type": "text | image | diagram | character",
      "content": "what to show",
      "position": "center | left | right | top | bottom"
    }
  ],
  "animations": [
    {
      "target": "element name or camera",
      "action": "fade_in | fade_out | zoom | pan | move | highlight",
      "duration": number
    }
  ],
  "timing": {
    "start": number,
    "end": number
  }
}
"""

    prompt = """
You are a professional animation director for medical educational videos.

Convert this storyboard into an animation plan.

STRICT RULES:
- Output ONLY valid JSON array
- No explanation
- No markdown
- No extra text

""" + schema + "\n\nStoryboard:\n" + json.dumps(storyboard, indent=2)

    response = generate(prompt)

    return extract_json(response) # type: ignore
    """
    Converts storyboard → animation plan (engine-ready JSON)
    """

    prompt = f"""
You are a professional animation director for medical educational videos.

Convert this storyboard into an animation plan.

STRICT RULES:
- Output ONLY valid JSON array
- No explanation
- No markdown
- No extra text

Each scene MUST include:

{
  "scene_number": number,
  "elements": [
    {
      "type": "text | image | diagram | character",
      "content": "what to show",
      "position": "center | left | right | top | bottom"
    }
  ],
  "animations": [
    {
      "target": "element name or camera",
      "action": "fade_in | fade_out | zoom | pan | move | highlight",
      "duration": number
    }
  ],
  "timing": {
    "start": number,
    "end": number
  }
}

Storyboard:
{json.dumps(storyboard, indent=2)}
"""

    response = generate(prompt)

    return extract_json(response) # type: ignore