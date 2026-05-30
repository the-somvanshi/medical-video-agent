from fastapi import FastAPI # type: ignore
from llm.groq_provider import generate
from pydantic import BaseModel
from agents.script.script_agent import generate_script as build_script # type: ignore
from agents.storyboard.storyboard_agent import create_storyboard # type: ignore
from agents.animation.animation_agent import generate_animation as build_animation # type: ignore

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Medical Video Agent Running"}

@app.get("/chat")
def chat():
    answer = generate(
        "Explain hypertension in simple words."
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

@app.post("/generate-animation")
def generate_animation(req: TopicRequest):

    script = build_script(req.topic)
    storyboard = create_storyboard(script)
    animation = build_animation(storyboard) # type: ignore

    return {
        "script": script,
        "storyboard": storyboard,
        "animation": animation
    }