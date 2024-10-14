async function fetchTasks() {
    let response = await fetch("/tasks/");
    let tasks = await response.json();
    let taskList = document.getElementById("task-list");
    taskList.innerHTML = '';
    tasks.forEach(task => {
        let li = document.createElement("li");
        li.textContent = task.title;
        taskList.appendChild(li);
    });
}

async function addTask() {
    let taskTitle = document.getElementById("new-task").value;
    await fetch("/tasks/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: taskTitle })
    });
    fetchTasks();
}
