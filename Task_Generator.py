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

#Added two new functions to change a task's name or priority
# The functions take the name of the task and a dictionary with tasks
#and a new name or priority for the task 

def change_task_title(name, tasks, new_name):
    for task in tasks:
        if task["task"] == name:
            task["task"] = new_name
    with open("task_database.json", "w") as file:
        json.dump(tasks, file)

def change_task_priority(name, tasks, new_priority):
    for task in tasks:
        if task["task"] == name:
            task["task"] = new_priority
    with open("task_database.json", "w") as file:
        json.dump(tasks, file)



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
