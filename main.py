from asyncio import subprocess
import json
from pathlib import Path
from datetime import datetime
from fastapi import FastAPI # type: ignore
from llm.groq_provider import generate
from pydantic import BaseModel
from agents.script.script_agent import generate_script as build_script # type: ignore
from agents.storyboard.storyboard_agent import create_storyboard # type: ignore
from agents.animation.animation_agent import generate_animation as build_animation # type: ignore

PROJECTS_DIR = Path("projects")
PROJECTS_DIR.mkdir(exist_ok=True)
app = FastAPI()

@app.get("/")
def root():
    return {"message": "Medical Video Agent Running"}

@app.get("/chat")
def chat():
    answer = generate(
        "Explain  general anesthesia in simple words."
    )

    return {
        "response": answer
    }
class TopicRequest(BaseModel):
    topic: str

@app.post("/generate-script")
def generate_script(req: TopicRequest):
    script = build_script(req.topic) # type: ignore
    return {"script": script}

@app.post("/generate-storyboard")
def generate_storyboard(req: TopicRequest):

    script = build_script(req.topic)
    storyboard = create_storyboard(script)

    return {
        "script": script,
        "storyboard": storyboard
    }

# @app.post("/generate-animation")
# def generate_animation(req: TopicRequest):

#     script = build_script(req.topic)
#     storyboard = create_storyboard(script)
#     animation = build_animation(storyboard) # type: ignore

#     return {
#         "script": script,
#         "storyboard": storyboard,
#         "animation": animation
#     }
@app.post("/generate-animation")
def generate_animation(req: TopicRequest):

    # Generate content
    script = build_script(req.topic)

    storyboard = create_storyboard(script)

    animation = build_animation(storyboard)

    # Create project folder
    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    project_name = (
        req.topic
        .replace(" ", "_")
        .lower()
    )

    project_dir = (
        PROJECTS_DIR /
        f"{project_name}_{timestamp}"
    )

    project_dir.mkdir(parents=True)

    # Save everything
    output = {
        "topic": req.topic,
        "script": script,
        "storyboard": storyboard,
        "animation": animation
    }

    json_file = (
        project_dir /
        "storyboard.json"
    )

    with open(
        json_file,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            output,
            f,
            indent=4,
            ensure_ascii=False
        )
    import subprocess

    subprocess.run(
    [
        "python",
        "prompt_worker.py",
        str(json_file)
    ],
    check=True
    )

    return {
        "status": "success",
        "project_dir": str(project_dir),
        "json_file": str(json_file)
    }