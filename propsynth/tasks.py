# This is the data loader which turns task folders in the tasks dir on disk into Task objects 

from dataclasses import dataclass # decorator that generates boilerplate for making a class
from pathlib import Path # handles paths for us as objects
import json # reads JSON, json.loads parses text into a python dict

# Get the absolute path to the tasks directory
# __file__ is this file, .resolve() makes it a full absolute path, .parent goes up a folder, / "tasks" joins on tasks folder
TASKS_DIR = Path(__file__).resolve().parent.parent / "tasks"

@dataclass(frozen = True) # make immutable tasks/instances because tasks are fixed input data (can't reassign a field)
class Task:
    name: str # dir name, ex: "merge_sorted"
    entrypoint: str # function the model must define, the named thing the tests will call to exercise the solution
    prompt: str # english spec shown to the model
    properties_path: Path # the path to the property tests file

# Takes the path to a task folder and builds a Task class from it
def load_task(task_dir: Path) -> Task:
    # gets the meta file from the task dir, reads the text as a str, and json.loads it to parse the string into a dict
    meta = json.loads((task_dir / "meta.json").read_text()) 
    # gets the prompt file from task dir and reads the text as a str
    prompt = (task_dir / "prompt.md").read_text()
    # constructs a Task class for the task dir
    return Task(
        name = task_dir.name, # .name of a Path is the final folder name, ex: "merge_sorted"
        entrypoint = meta["entrypoint"], # pulls the entrypoint value (func model must define) from the meta dict
        prompt = prompt, # the english spec str
        properties_path = task_dir / "properties.py", # path to the properties file
    )

# Loads all the tasks at once into a list of all the Task objects
def load_all_tasks(tasks_dir: Path = TASKS_DIR) -> list[Task]:
    # list comprehension (compact looping and filtering)
    return [
        load_task (d)
        # loops over each task in the tasks_dir, iterdir lists the contents, sorted() puts them in consistent order so eval runs are comparable
        for d in sorted(tasks_dir.iterdir())
        # loads only items that are folders and also contain a meta.json to guarantee the item is a task
        if d.is_dir() and (d / "meta.json").exists() 
    ]
