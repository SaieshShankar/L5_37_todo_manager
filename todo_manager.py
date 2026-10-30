
"""
Todo Manager
A simple task management program with JSON persistence.
"""

import json
import secrets
from datetime import datetime

tasks = {}
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


# FIX 1: Mutable default argument changed from [] to None.
# This prevents a shared list from being reused across function calls.
def add_task(title, priority="medium", labels=None):
    """Add a new task with a priority and optional labels."""
    if labels is None:
        labels = []

    task_id = len(tasks) + 1
    labels.append(priority)

    # FIX 2: Labels are now stored in the task dictionary.
    tasks[task_id] = {
        "title": title,
        "priority": priority,
        "done": False,
        "labels": labels.copy(),
        "created": datetime.now().isoformat(),
    }
    return task_id


def complete_task(task_id):
    """Mark a task as completed using its ID."""
    if task_id in tasks:
        tasks[task_id]["done"] = True
        return True

    print("No task with id", task_id)
    return False


def pending_tasks():
    """Return pending tasks sorted according to priority."""
    pending = [
        task for task in tasks.values()
        if not task["done"]
    ]

    pending.sort(
        key=lambda task: PRIORITY_ORDER[task["priority"]]
    )

    return [task["title"] for task in pending]


def find_task(keyword):
    """Find and return a task ID matching the given keyword."""
    for task_id, task in tasks.items():
        if keyword.lower() in task["title"].lower():
            return task_id

    # FIX 3: Explicitly return None if no matching task is found.
    return None


# FIX 4: Replaced unsafe Pickle serialization with JSON.
# JSON avoids the arbitrary code execution risk associated with pickle.load().
def save_tasks(file_name="tasks.json"):
    """Save all tasks to a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


def load_tasks(file_name="tasks.json"):
    """Load tasks from a JSON file."""
    with open(file_name, "r", encoding="utf-8") as file:
        # FIX 5: json.load() replaces unsafe pickle.load().
        return json.load(file)


def export_json(file_name="tasks.json"):
    """Export all tasks into a JSON file."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=2)


# FIX 6: Removed remindByEmail() and os.system().
# The original function constructed shell commands using external input,
# creating a potential command injection vulnerability.


def main():
    """Run the Todo Manager demonstration."""
    add_task("Submit lab report", "high")
    add_task("Buy groceries")
    add_task("Call plumber", "low")
    add_task("Book train tickets", "high")

    complete_task(2)
    complete_task(99)

    print("Pending tasks:", pending_tasks())
    print("Task id for 'plumber':", find_task("plumber"))
    print("Task id for 'gym':", find_task("gym"))

    # FIX 7: Use secrets.choice() instead of random.choice().
    # This eliminates Bandit's B311 warning.
    # The empty-list check prevents an IndexError.
    pending = pending_tasks()

    if pending:
        suggestion = secrets.choice(pending)
        print("Try this next:", suggestion)
    else:
        print("No pending tasks available.")

    save_tasks()

    # FIX 8: JSON object keys become strings after loading.
    restored = load_tasks()
    print("Tasks restored from file:", len(restored))

    export_json()
    print("Exported tasks to tasks.json")


if __name__ == "__main__":
    main()
