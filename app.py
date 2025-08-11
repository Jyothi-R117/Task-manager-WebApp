from flask import Flask, render_template, request, redirect, url_for
import json
import os
from datetime import datetime

app = Flask(__name__)
TASKS_FILE = "tasks.json"

def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

@app.route("/")
def index():
    tasks = load_tasks()
    todo = [t for t in tasks if t["status"] == "To Do"]
    in_progress = [t for t in tasks if t["status"] == "In Progress"]
    completed = [t for t in tasks if t["status"] == "Completed"]
    return render_template("index.html", todo=todo, in_progress=in_progress, completed=completed)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    description = request.form.get("description")
    priority = request.form.get("priority")
    deadline = request.form.get("deadline")
    tasks = load_tasks()
    tasks.append({
        "title": title,
        "description": description,
        "priority": priority,
        "deadline": deadline,
        "status": "To Do"
    })
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/move/<title>/<status>")
def move(title, status):
    tasks = load_tasks()
    for task in tasks:
        if task["title"] == title:
            task["status"] = status
            break
    save_tasks(tasks)
    return redirect(url_for("index"))

@app.route("/delete/<title>")
def delete(title):
    tasks = [t for t in load_tasks() if t["title"] != title]
    save_tasks(tasks)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
