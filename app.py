from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "codevault-secret"

socketio = SocketIO(app, cors_allowed_origins="*")

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<title>CodeVault</title>

<style>
* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: Arial, sans-serif;
}

body {
    background: #080b12;
    color: white;
}

.container {
    width: 92%;
    max-width: 1150px;
    margin: auto;
    padding: 25px 0 60px;
}

header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.logo {
    font-size: 26px;
    font-weight: bold;
}

.logo span {
    color: #7182ff;
}

.online {
    background: #141a28;
    padding: 10px 15px;
    border-radius: 14px;
    color: #65d99a;
}

.hero {
    background: linear-gradient(135deg, #151d3b, #101522);
    border: 1px solid #252d49;
    border-radius: 25px;
    padding: 30px;
    margin-bottom: 20px;
}

.hero h1 {
    font-size: 30px;
    margin-bottom: 10px;
}

.hero p {
    color: #8e98b4;
}

button {
    border: 0;
    padding: 11px 17px;
    border-radius: 12px;
    background: #7182ff;
    color: white;
    font-weight: bold;
    cursor: pointer;
}

button:hover {
    opacity: .85;
}

.red {
    background: #df5863;
}

.green {
    background: #31ad76;
}

.grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
}

.card {
    background: #111621;
    border: 1px solid #222a40;
    border-radius: 20px;
    padding: 20px;
}

.label {
    color: #8993ad;
    font-size: 13px;
    margin-bottom: 10px;
}

.number {
    font-size: 30px;
    font-weight: bold;
}

.section {
    margin-top: 30px;
}

.section h2 {
    margin-bottom: 15px;
}

.form {
    display: flex;
    gap: 8px;
    margin-bottom: 15px;
}

input,
select {
    flex: 1;
    padding: 13px;
    border-radius: 12px;
    border: 1px solid #29324b;
    background: #0d121d;
    color: white;
    outline: none;
}

.skills,
.projects {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
}

.skill,
.project {
    background: #111621;
    border: 1px solid #222a40;
    border-radius: 18px;
    padding: 20px;
}

.skill-top {
    display: flex;
    justify-content: space-between;
}

.bar {
    height: 8px;
    background: #252d43;
    border-radius: 20px;
    overflow: hidden;
    margin: 12px 0;
}

.fill {
    height: 100%;
    background: #7182ff;
}

.status {
    display: inline-block;
    margin: 12px 0;
    padding: 6px 10px;
    border-radius: 8px;
    background: #29324b;
    font-size: 12px;
}

/* CHAT */

.chat-box {
    background: #111621;
    border: 1px solid #222a40;
    border-radius: 20px;
    overflow: hidden;
}

.chat-header {
    padding: 18px 20px;
    border-bottom: 1px solid #222a40;
}

.messages {
    height: 400px;
    overflow-y: auto;
    padding: 18px;
}

.message {
    margin-bottom: 14px;
}

.message-name {
    color: #7182ff;
    font-weight: bold;
    margin-bottom: 4px;
}

.message-text {
    background: #1a2132;
    padding: 10px 13px;
    border-radius: 12px;
    display: inline-block;
    max-width: 85%;
    word-break: break-word;
}

.message-time {
    color: #69748f;
    font-size: 11px;
    margin-left: 7px;
}

.system {
    color: #69748f;
    text-align: center;
    margin: 12px;
    font-size: 13px;
}

.chat-input {
    display: flex;
    gap: 8px;
    padding: 15px;
    border-top: 1px solid #222a40;
}

.chat-input input {
    min-width: 0;
}

.empty {
    color: #737e99;
    padding: 15px 0;
}

@media(max-width: 800px) {
    .grid {
        grid-template-columns: repeat(2, 1fr);
    }

    .skills,
    .projects {
        grid-template-columns: 1fr;
    }
}

@media(max-width: 550px) {
    .grid {
        grid-template-columns: 1fr;
    }

    .form,
    .chat-input {
        flex-direction: column;
    }

    .hero h1 {
        font-size: 24px;
    }

    .messages {
        height: 350px;
    }
}
</style>
</head>

<body>

<div class="container">

<header>
    <div class="logo">
        Code<span>Vault</span> 💻
    </div>

    <div class="online">
        🟢 <span id="online">0</span> online
    </div>
</header>


<section class="hero">

    <h1 id="welcome">
        Welcome, Developer 👋
    </h1>

    <p>
        Track your coding journey and connect with other developers.
    </p>

    <br>

    <button onclick="setName()">
        Set Developer Name
    </button>

</section>


<div class="grid">

    <div class="card">
        <div class="label">CODING HOURS</div>
        <div class="number" id="hours">0</div>
    </div>

    <div class="card">
        <div class="label">SKILLS</div>
        <div class="number" id="skillCount">0</div>
    </div>

    <div class="card">
        <div class="label">PROJECTS</div>
        <div class="number" id="projectCount">0</div>
    </div>

    <div class="card">
        <div class="label">COMPLETED</div>
        <div class="number" id="completed">0</div>
    </div>

</div>


<!-- SKILLS -->

<div class="section">

<h2>🧠 My Skills</h2>

<div class="form">

<input
    id="skillName"
    placeholder="Skill name e.g. Python"
>

<input
    id="skillProgress"
    type="number"
    min="0"
    max="100"
    placeholder="Progress %"
>

<button onclick="addSkill()">
    Add
</button>

</div>

<div class="skills" id="skills"></div>

</div>


<!-- PROJECTS -->

<div class="section">

<h2>🚀 My Projects</h2>

<div class="form">

<input
    id="projectName"
    placeholder="Project name"
>

<input
    id="projectDescription"
    placeholder="Short description"
>

<select id="projectStatus">
    <option>Planning</option>
    <option>In Progress</option>
    <option>Completed</option>
</select>

<button onclick="addProject()">
    Add
</button>

</div>

<div class="projects" id="projects"></div>

</div>


<!-- REAL TIME CHAT -->

<div class="section">

<h2>💬 Developer Chat</h2>

<div class="chat-box">

<div class="chat-header">
    <strong>🌐 Global Coding Chat</strong>
    <p style="color:#8993ad;margin-top:5px">
        Chat with other developers in real time.
    </p>
</div>

<div class="messages" id="messages"></div>

<div class="chat-input">

<input
    id="messageInput"
    placeholder="Write a message..."
    autocomplete="off"
>

<button onclick="sendMessage()">
    Send
</button>

</div>

</div>

</div>

</div>


<script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

<script>

/* LOCAL DASHBOARD DATA */

let skills =
JSON.parse(localStorage.getItem("cv_skills")) || [];

let projects =
JSON.parse(localStorage.getItem("cv_projects")) || [];

let codingMinutes =
Number(localStorage.getItem("cv_minutes")) || 0;

let completed =
Number(localStorage.getItem("cv_completed")) || 0;

let developerName =
localStorage.getItem("cv_name") || "";


/* NAME */

function setName() {

    let name = prompt("Enter your developer name:");

    if (!name) return;

    developerName = name.trim();

    localStorage.setItem(
        "cv_name",
        developerName
    );

    render();

}


/* SKILLS */

function addSkill() {

    let name =
        document.getElementById("skillName")
        .value.trim();

    let progress =
        Number(
            document.getElementById("skillProgress")
            .value
        );

    if (!name) {
        alert("Enter skill name!");
        return;
    }

    if (
        isNaN(progress) ||
        progress < 0 ||
        progress > 100
    ) {
        alert("Progress must be between 0 and 100!");
        return;
    }

    skills.push({
        name: name,
        progress: progress
    });

    document.getElementById("skillName").value = "";
    document.getElementById("skillProgress").value = "";

    save();
    render();
}


function deleteSkill(index) {

    skills.splice(index, 1);

    save();
    render();

}


/* PROJECTS */

function addProject() {

    let name =
        document.getElementById("projectName")
        .value.trim();

    let description =
        document.getElementById("projectDescription")
        .value.trim();

    let status =
        document.getElementById("projectStatus")
        .value;

    if (!name) {
        alert("Enter project name!");
        return;
    }

    projects.push({
        name: name,
        description: description,
        status: status
    });

    document.getElementById("projectName").value = "";
    document.getElementById("projectDescription").value = "";

    save();
    render();

}


function deleteProject(index) {

    projects.splice(index, 1);

    save();
    render();

}


function completeProject(index) {

    if (projects[index].status !== "Completed") {

        projects[index].status = "Completed";

        completed++;

        save();
        render();

    }

}


/* SAVE */

function save() {

    localStorage.setItem(
        "cv_skills",
        JSON.stringify(skills)
    );

    localStorage.setItem(
        "cv_projects",
        JSON.stringify(projects)
    );

    localStorage.setItem(
        "cv_minutes",
        codingMinutes
    );

    localStorage.setItem(
        "cv_completed",
        completed
    );

}


/* RENDER */

function render() {

    document.getElementById("hours")
        .innerText =
        (codingMinutes / 60).toFixed(1);

    document.getElementById("skillCount")
        .innerText = skills.length;

    document.getElementById("projectCount")
        .innerText = projects.length;

    document.getElementById("completed")
        .innerText = completed;


    if (developerName) {

        document.getElementById("welcome")
            .innerText =
            "Welcome back, " +
            developerName +
            " 👋";

    }


    /* SKILLS */

    let skillBox =
        document.getElementById("skills");

    skillBox.innerHTML = "";

    if (skills.length === 0) {

        skillBox.innerHTML =
            '<div class="empty">Add your first skill.</div>';

    }

    skills.forEach((skill, index) => {

        skillBox.innerHTML += `

        <div class="skill">

            <div class="skill-top">

                <strong>
                    💡 ${escapeHTML(skill.name)}
                </strong>

                <strong>
                    ${skill.progress}%
                </strong>

            </div>

            <div class="bar">

                <div
                    class="fill"
                    style="width:${skill.progress}%">
                </div>

            </div>

            <button
                class="red"
                onclick="deleteSkill(${index})">

                Remove

            </button>

        </div>

        `;

    });


    /* PROJECTS */

    let projectBox =
        document.getElementById("projects");

    projectBox.innerHTML = "";

    if (projects.length === 0) {

        projectBox.innerHTML =
            '<div class="empty">Add your first project.</div>';

    }

    projects.forEach((project, index) => {

        projectBox.innerHTML += `

        <div class="project">

            <h3>
                🚀 ${escapeHTML(project.name)}
            </h3>

            <p style="color:#8993ad;margin-top:8px">
                ${escapeHTML(project.description)}
            </p>

            <div class="status">
                ${escapeHTML(project.status)}
            </div>

            <br>

            ${
                project.status !== "Completed"
                ?
                `<button
                    class="complete"
                    onclick="completeProject(${index})">
                    Mark Completed
                </button>`
                :
                ""
            }

            <button
                class="red"
                onclick="deleteProject(${index})">
                Delete
            </button>

        </div>

        `;

    });

}


function escapeHTML(value) {

    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");

}


/* REAL-TIME CHAT */

const socket = io();

const messageInput =
    document.getElementById("messageInput");

const messages =
    document.getElementById("messages");


function sendMessage() {

    let text =
        messageInput.value.trim();

    if (!text) return;

    let name =
        developerName || "Anonymous";

    socket.emit(
        "send_message",
        {
            name: name,
            text: text
        }
    );

    messageInput.value = "";

}


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);


socket.on(
    "message",
    function(data) {

        let div =
            document.createElement("div");

        div.className = "message";

        let name =
            document.createElement("div");

        name.className =
            "message-name";

        name.innerText =
            data.name;

        let text =
            document.createElement("span");

        text.className =
            "message-text";

        text.innerText =
            data.text;

        let time =
            document.createElement("span");

        time.className =
            "message-time";

        time.innerText =
            data.time;

        div.appendChild(name);
        div.appendChild(text);
        div.appendChild(time);

        messages.appendChild(div);

        messages.scrollTop =
            messages.scrollHeight;

    }
);


socket.on(
    "system_message",
    function(text) {

        let div =
            document.createElement("div");

        div.className = "system";

        div.innerText = text;

        messages.appendChild(div);

        messages.scrollTop =
            messages.scrollHeight;

    }
);


socket.on(
    "online_count",
    function(count) {

        document.getElementById("online")
            .innerText = count;

    }
);


render();

</script>

</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML)


connected_users = 0


@socketio.on("connect")
def user_connect():

    global connected_users

    connected_users += 1

    emit(
        "online_count",
        connected_users,
        broadcast=True
    )

    emit(
        "system_message",
        "🟢 You joined the developer chat."
    )


@socketio.on("disconnect")
def user_disconnect():

    global connected_users

    connected_users = max(
        0,
        connected_users - 1
    )

    socketio.emit(
        "online_count",
        connected_users
    )


@socketio.on("send_message")
def handle_message(data):

    name = str(
        data.get("name", "Anonymous")
    )[:30]

    text = str(
        data.get("text", "")
    ).strip()[:500]

    if not text:
        return

    now = datetime.now().strftime("%H:%M")

    socketio.emit(
        "message",
        {
            "name": name,
            "text": text,
            "time": now
        }
    )


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000,
        allow_unsafe_werkzeug=True
    )
