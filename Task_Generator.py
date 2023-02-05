from flask import Flask, render_template, request, redirect, session
import random
import json

app = Flask(__name__)

try:
    with open("task_database.json", "r") as file:
        tasks = json.load(file)
except:
    tasks = []

n = 0


def generate_task():
    total_priority = sum(task["priority"] for task in tasks)
    random_number = random.uniform(0, total_priority)
    running_sum = 0
    for task in tasks:
        running_sum += task["priority"]
        if running_sum > random_number:
            return task["task"]

# The function returns a dictionary where the tasks are sorted 
# in descending based on their priority
def sort_by_priority(tasks: dict):
    return sorted(tasks, key=lambda task: task["priority"], reverse=True)

print(sort_by_priority(tasks))

@app.route("/")
def home():
    n = len(tasks)  # updates n everytime the home is rendered
    picked_task = ''
    if tasks:
        picked_task = generate_task()
    return render_template("home.html", tasks=tasks, n=n, picked_task=picked_task)


@app.route("/add_task", methods=["POST"])
def add_task():
    task = request.form["task"]
    priority = int(request.form["priority"])
    tasks.append({"task": task, "priority": priority})
    with open("task_database.json", "w") as file:
        json.dump(tasks, file)
    return redirect("/")


@app.route("/remove_task/<int:index>")
def remove_task(index):
    tasks.pop(index)
    return redirect("/")

# if __name__ == "__main__":
#     app.run(debug=False)
