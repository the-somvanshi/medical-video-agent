from pathlib import Path

folders = [
    "app",
    "agents/research",
    "agents/script",
    "agents/storyboard",
    "agents/assets",
    "agents/animation",
    "llm",
    "knowledge",
    "datasets",
    "outputs",
    "tests",
]

files = [
    "main.py",
    ".env",
    "agents/__init__.py",
    "llm/__init__.py",
    "llm/groq_provider.py",
]

for folder in folders:
    Path(folder).mkdir(parents=True, exist_ok=True)

for file in files:
    path = Path(file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.touch(exist_ok=True)

print("✅ Project structure created successfully!")