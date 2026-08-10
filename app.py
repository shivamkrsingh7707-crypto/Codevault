from flask import Flask, render_template_string, request
from flask_socketio import SocketIO, emit
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.config["SECRET_KEY"] = "codevault-secret-key"

socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="gevent"
)

DB = "chat.db"


def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def get_messages():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    rows = conn.execute("""
        SELECT username, message, timestamp
        FROM messages
        ORDER BY id ASC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def save_message(username, message):
    timestamp = datetime.now().strftime("%d %b %Y, %I:%M %p")

    conn = sqlite3.connect(DB)

    conn.execute(
        """
        INSERT INTO messages (username, message, timestamp)
        VALUES (?, ?, ?)
        """,
        (username, message, timestamp)
    )

    conn.commit()
    conn.close()

    return timestamp


@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
    <meta name="viewport"
          content="width=device-width, initial-scale=1">

    <title>CodeVault</title>

    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #0b1020;
            color: white;
        }

        header {
            padding: 18px;
            background: #111827;
            border-bottom: 1px solid #273244;
            font-size: 22px;
            font-weight: bold;
        }

        .container {
            max-width: 900px;
            margin: auto;
            padding: 20px;
        }

        .dashboard {
            display: grid;
            grid-template-columns:
                repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }

        .card {
            background: #151e30;
            padding: 18px;
            border-radius: 14px;
            text-align: center;
        }

        .card b {
            display: block;
            font-size: 25px;
            margin-bottom: 5px;
        }

        .chat {
            background: #111827;
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid #273244;
        }

        .chat-header {
            padding: 16px;
            font-size: 19px;
            font-weight: bold;
            border-bottom: 1px solid #273244;
        }

        #messages {
            height: 430px;
            overflow-y: auto;
            padding: 15px;
        }

        .message {
            background: #1b2638;
            padding: 10px 13px;
            margin-bottom: 10px;
            border-radius: 12px;
        }

        .username {
            font-weight: bold;
            margin-bottom: 4px;
        }

        .time {
            font-size: 11px;
            opacity: .55;
            margin-top: 5px;
        }

        .input-area {
            display: flex;
            gap: 8px;
            padding: 12px;
            border-top: 1px solid #273244;
        }

        input {
            flex: 1;
            padding: 13px;
            border-radius: 10px;
            border: 1px solid #344154;
            background: #0b1020;
            color: white;
            outline: none;
        }

        button {
            border: none;
            padding: 13px 18px;
            border-radius: 10px;
            background: #2563eb;
            color: white;
            font-weight: bold;
            cursor: pointer;
        }

        button:hover {
            opacity: .9;
        }

        .status {
            padding: 10px 15px;
            font-size: 13px;
            opacity: .7;
        }
    </style>
</head>

<body>

<header>
    💻 CodeVault
</header>

<div class="container">

    <div class="dashboard">
        <div class="card">
            <b>🐍</b>
            Python
        </div>

        <div class="card">
            <b>📊</b>
            Skills
        </div>

        <div class="card">
            <b>🚀</b>
            Projects
        </div>
    </div>

    <div class="chat">

        <div class="chat-header">
            💬 CodeVault Chat
        </div>

        <div class="status" id="status">
            Connecting...
        </div>

        <div id="messages"></div>

        <div class="input-area">

            <input
                id="username"
                placeholder="Your name"
                maxlength="30"
            >

            <input
                id="message"
                placeholder="Type a message..."
                maxlength="500"
            >

            <button onclick="sendMessage()">
                Send
            </button>

        </div>

    </div>

</div>


<script>

const socket = io();

const messagesBox = document.getElementById("messages");
const messageInput = document.getElementById("message");
const usernameInput = document.getElementById("username");
const statusBox = document.getElementById("status");


function addMessage(data) {

    const div = document.createElement("div");

    div.className = "message";

    div.innerHTML = `
        <div class="username">
            ${escapeHTML(data.username)}
        </div>

        <div>
            ${escapeHTML(data.message)}
        </div>

        <div class="time">
            ${escapeHTML(data.timestamp)}
        </div>
    `;

    messagesBox.appendChild(div);

    messagesBox.scrollTop = messagesBox.scrollHeight;
}


function escapeHTML(text) {

    const div = document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}


socket.on("connect", () => {

    statusBox.textContent = "🟢 Connected";

});


socket.on("disconnect", () => {

    statusBox.textContent = "🔴 Disconnected";

});


socket.on("chat_history", (messages) => {

    messagesBox.innerHTML = "";

    messages.forEach(addMessage);

});


socket.on("new_message", (data) => {

    addMessage(data);

});


function sendMessage() {

    const username =
        usernameInput.value.trim();

    const message =
        messageInput.value.trim();


    if (!username) {

        alert("Please enter your name.");

        return;
    }


    if (!message) {

        return;
    }


    socket.emit("send_message", {

        username: username,

        message: message

    });


    messageInput.value = "";

    messageInput.focus();

}


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (event.key === "Enter") {

            sendMessage();

        }

    }
);

</script>

</body>
</html>
    """)


@socketio.on("connect")
def handle_connect():

    emit(
        "chat_history",
        get_messages()
    )


@socketio.on("send_message")
def handle_message(data):

    username = str(
        data.get("username", "Anonymous")
    ).strip()

    message = str(
        data.get("message", "")
    ).strip()


    if not username or not message:
        return


    username = username[:30]
    message = message[:500]


    timestamp = save_message(
        username,
        message
    )


    socketio.emit(
        "new_message",
        {
            "username": username,
            "message": message,
            "timestamp": timestamp
        }
    )


init_db()


if __name__ == "__main__":

    socketio.run(
        app,
        host="0.0.0.0",
        port=5000
    )
