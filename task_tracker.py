import json
import os
from datetime import datetime
from typing import List, Optional
import argparse

# JSON 파일 경로
TASKS_FILE = 'tasks.json'

# 작업을 로드하는 함수
def load_tasks() -> List[dict]:
    if not os.path.exists(TASKS_FILE):
        return []

    try:
        with open(TASKS_FILE, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        return []

# 작업을 저장하는 함수
def save_tasks(tasks: List[dict]) -> None:
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# 작업을 추가하는 함수
def add_task(description: str) -> None:
    tasks = load_tasks()
    task_id = max((task['id'] for task in tasks), default=0) + 1
    task = {
        'id': task_id,
        'description': description,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added successfully (ID: {task_id})')

def parse_args():
    parser = argparse.ArgumentParser(
        description="Task Tracker CLI - A simple command line tool to track and manage tasks.",
        epilog="Use the help option (-h or --help) for more details on each command."
    )

    subparsers = parser.add_subparsers(dest="command", required=True, help="Commands")

    # add command
    parser_add = subparsers.add_parser(
        "add",
        help="Add a new task",
        description="Adds a new task to the task tracker."
    )
    parser_add.add_argument("description", help="Description of the task")


    return parser.parse_args()

args = parse_args()

if args.command == "add":
    add_task(args.description)
else:
    print("Unknown command. Use -h or --help for a list of available commands.")