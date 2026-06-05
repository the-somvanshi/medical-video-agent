import json
from pathlib import Path

from llm.groq_provider import generate


def create_image_prompt(scene):

    visual_description = scene.get("visual_description", "")
    voice_over = scene.get("voice_over_text", "")

    prompt = f"""
You are an expert medical IMAGE prompt engineer.

Convert the scene into a SINGLE high-quality IMAGE generation prompt.

IMPORTANT RULES:
- Only generate static image description (NOT video, NOT animation)
- Do NOT include camera movement (no zoom, pan, motion)
- Do NOT include time-based actions (no "showing", "transition", "sequence")
- Focus on one frozen moment in time
- Medical educational style
- Scientifically accurate anatomy and biology
- Ultra detailed, professional medical illustration
- Pure white background when appropriate
- No text
- No labels

Scene Visual Description:
{visual_description}

Voice Over Context:
{voice_over}

Return ONLY the final image prompt. No explanation.
"""

    try:
        return generate(prompt).strip()

    except Exception as e:
        print(f"Prompt generation failed: {e}")
        return visual_description


def create_prompt_file(storyboard_path):

    storyboard_path = Path(storyboard_path)

    if not storyboard_path.exists():
        raise FileNotFoundError(
            f"Storyboard not found: {storyboard_path}"
        )

    prompt_path = (
        storyboard_path.parent
        / "prompt.json"
    )

    print(
        f"\nReading storyboard:\n{storyboard_path}\n"
    )

    with open(
        storyboard_path,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)

    storyboard = data.get(
        "storyboard",
        []
    )

    # Handle stringified JSON
    if isinstance(
        storyboard,
        str
    ):
        storyboard = json.loads(
            storyboard
        )

    prompt_scenes = []

    total_scenes = len(
        storyboard
    )

    print(
        f"Found {total_scenes} scenes\n"
    )

    for scene in storyboard:

        scene_number = scene.get(
            "scene_number",
            "Unknown"
        )

        print(
            f"Generating Scene {scene_number}..."
        )

        image_prompt = (
            create_image_prompt(scene)
        )

        new_scene = dict(scene)

        new_scene[
            "image_prompt"
        ] = image_prompt

        prompt_scenes.append(
            new_scene
        )

    prompt_data = {

        "topic":
        data.get(
            "topic",
            ""
        ),

        "scenes":
        prompt_scenes

    }

    with open(
        prompt_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            prompt_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print(
        f"\nPrompt file created:\n{prompt_path}"
    )

    return prompt_path


if __name__ == "__main__":

    storyboard_file = r"E:\JS_PROJECTS\DIRECTOR_AGENT\medical-video-agent\projects\general_anesthesia_20260605_195119\storyboard.json"

    create_prompt_file(
        storyboard_file
    )