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

# 작업을 업데이트하는 함수
def update_task(task_id: int, new_description: str) -> None:
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task:
        task['description'] = new_description
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f'Task {task_id} updated successfully')
    else:
        print(f'Task {task_id} not found')

# 작업을 삭제하는 함수
def delete_task(task_id: int) -> None:
    tasks = load_tasks()
    original_count = len(tasks)
    tasks = [task for task in tasks if task['id'] != task_id]

    if len(tasks) < original_count:
        save_tasks(tasks)
        print(f'Task {task_id} deleted successfully')
    else:
        print(f'Task {task_id} not found')

# 작업 상태를 업데이트하는 함수
def update_task_status(task_id: int, status: str) -> None:
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)

    if task:
        task['status'] = status
        task['updatedAt'] = datetime.now().isoformat()
        save_tasks(tasks)
        print(f'Task {task_id} marked as {status}')
    else:
        print(f'Task {task_id} not found')

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

    # update command
    parser_update = subparsers.add_parser(
        "update",
        help="Update an existing task",
        description="Updates the description of an existing task."
    )
    parser_update.add_argument("task_id", type=int, help="ID of the task to update")
    parser_update.add_argument("description", help="New description of the task")

    # delete command
    parser_delete = subparsers.add_parser(
        "delete",
        help="Delete a task",
        description="Deletes a task by its ID."
    )
    parser_delete.add_argument("task_id", type=int, help="ID of the task to delete")

    # mark-in-progress command
    parser_mark_in_progress = subparsers.add_parser(
        "mark-in-progress",
        help="Mark a task as in-progress",
        description="Marks a task as in-progress."
    )
    parser_mark_in_progress.add_argument("task_id", type=int, help="ID of the task to mark as in-progress")

    # mark-done command
    parser_mark_done = subparsers.add_parser(
        "mark-done",
        help="Mark a task as done",
        description="Marks a task as done."
    )
    parser_mark_done.add_argument("task_id", type=int, help="ID of the task to mark as done")

    return parser.parse_args()

args = parse_args()

if args.command == "add":
    add_task(args.description)
elif args.command == "update":
    update_task(args.task_id, args.description)
elif args.command == "delete":
    delete_task(args.task_id)
elif args.command == "mark-in-progress":
    update_task_status(args.task_id, "in-progress")
elif args.command == "mark-done":
    update_task_status(args.task_id, "done")
else:
    print("Unknown command. Use -h or --help for a list of available commands.")