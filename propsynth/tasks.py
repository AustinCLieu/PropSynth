from dataclasses import dataclass
from pathlib import Path
import json

# Get the relative tasks directory
TASKS_DIR = Path(__file__).resolve().parent.parent / "tasks"

@dataclass(frozen = True) # make immutable tasks/instances
class Task:
    name: str # dir name, ex: "merge_sorted"
    entrypoint: str # function the solution must define
    prompt: str # natural-language spec shown to the model
    properties_path: Path # path to property

def load_task(task_dir: Path) -> Task:
    meta = json.loads((task_dir / "meta.json").read_text())
    prompt = (task_dir / "prompt.md").read_text()
    return Task(
        name = task_dir.name,
        entrypoint = meta["entrypoint"],
        prompt = prompt,
        properties_path = task_dir / "properties.py",
    )

def load_all_tasks(tasks_dir: Path = TASKS_DIR) -> list[Task]:
    return [
        load_task (d)
        for d in sorted(tasks_dir.iterdir()) # each element in tasks
        if d.is_dir() and (d / "meta.json").exists() # makes sure the element is a folder and has a meta.json, guarantees a task
    ]
