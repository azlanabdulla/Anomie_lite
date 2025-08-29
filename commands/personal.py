import json, os

NOTES_FILE = "data/notes.txt"
TODO_FILE  = "data/todos.json"

def register(bot):
    bot.register("note add", note_add_cmd, "Add a note: note add <text>")
    bot.register("note read", note_read_cmd, "Read all notes")
    bot.register("todo add", todo_add_cmd, "Add a task: todo add <text>")
    bot.register("todo list", todo_list_cmd, "List tasks")
    bot.register("todo done", todo_done_cmd, "Mark task done by index: todo done 2")
    bot.register("todo clear", todo_clear_cmd, "Clear all tasks")

def note_add_cmd(user_input):
    text = user_input[len("note add"):].strip()
    if not text:
        return "Usage: note add <text>"
    os.makedirs("data", exist_ok=True)
    with open(NOTES_FILE, "a", encoding="utf-8") as f:
        f.write(text + "\n")
    return "Note saved."

def note_read_cmd(_):
    if not os.path.exists(NOTES_FILE):
        return "No notes yet."
    with open(NOTES_FILE, "r", encoding="utf-8") as f:
        data = f.read().strip()
    return "Your Notes:\n" + (data if data else "(empty)")

def load_todos():
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save_todos(items):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, indent=2, ensure_ascii=False)

def todo_add_cmd(user_input):
    text = user_input[len("todo add"):].strip()
    if not text:
        return "Usage: todo add <text>"
    items = load_todos()
    items.append({"task": text, "done": False})
    save_todos(items)
    return "Task added."

def todo_list_cmd(_):
    items = load_todos()
    if not items:
        return "(no tasks)"
    lines = []
    for i, it in enumerate(items, 1):
        status = "✔" if it.get("done") else "•"
        lines.append(f"{i}. [{status}] {it.get('task')}")
    return "\n".join(lines)

def todo_done_cmd(user_input):
    parts = user_input.split()
    if len(parts) < 3 or not parts[2].isdigit():
        return "Usage: todo done <index>"
    idx = int(parts[2]) - 1
    items = load_todos()
    if 0 <= idx < len(items):
        items[idx]["done"] = True
        save_todos(items)
        return f"Marked done: {items[idx]['task']}"
    return "Invalid index."

def todo_clear_cmd(_):
    save_todos([])
    return "All tasks cleared."
