mkdir templates
cat << 'EOF' > templates/index.html
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Global Coder Chat</title>
    <!-- Highlight.js for code formatting -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css" id="hl-style">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <style>
        /* Theme Variables */
        :root {
            --bg-color: #f0f2f5;
            --container-bg: #ffffff;
            --text-color: #1a1a1a;
            --text-muted: #666;
            --border-color: #e4e6eb;
            --msg-bg: #f2f2f2;
            --primary: #0a7cff;
            --primary-hover: #0066d6;
        }
        [data-theme="dark"] {
            --bg-color: #121212;
            --container-bg: #1e1e1e;
            --text-color: #e4e6eb;
            --text-muted: #b0b3b8;
            --border-color: #3e4042;
            --msg-bg: #242526;
            --primary: #4d94ff;
            --primary-hover: #3b7cff;
        }

        * { box-sizing: border-box; transition: background-color 0.3s, color 0.3s; }
        body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; background: var(--bg-color); color: var(--text-color); margin: 0; display: flex; justify-content: center; height: 100vh; padding: 10px; }
        
        .chat-container { width: 100%; max-width: 800px; background: var(--container-bg); display: flex; flex-direction: column; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); overflow: hidden; }
        
        /* Header */
        header { display: flex; justify-content: space-between; align-items: center; padding: 15px 20px; border-bottom: 1px solid var(--border-color); }
        header h2 { margin: 0; font-size: 1.2rem; display: flex; align-items: center; gap: 8px; }
        
        /* Theme Toggle Button */
        .theme-btn { background: transparent; border: 1px solid var(--border-color); color: var(--text-color); padding: 6px 12px; border-radius: 20px; cursor: pointer; font-size: 0.9rem; font-weight: 600; }
        .theme-btn:hover { background: var(--msg-bg); }

        /* Chat Area */
        #messages { flex: 1; overflow-y: auto; padding: 20px; margin: 0; list-style: none; display: flex; flex-direction: column; gap: 12px; }
        .msg { background: var(--msg-bg); padding: 12px 16px; border-radius: 8px; max-width: 90%; align-self: flex-start; word-wrap: break-word; }
        .msg-header { font-size: 0.85rem; font-weight: bold; color: var(--primary); margin-bottom: 5px; display: block; }
        pre { margin: 8px 0 0 0; border-radius: 6px; }
        
        /* Input Area */
        .input-area { padding: 15px; border-top: 1px solid var(--border-color); display: flex; gap: 10px; background: var(--container-bg); }
        .input-area input { background: var(--msg-bg); color: var(--text-color); border: 1px solid transparent; padding: 12px; border-radius: 8px; font-size: 1rem; outline: none; }
        .input-area input:focus { border: 1px solid var(--primary); }
        #username { width: 100px; font-weight: bold; }
        #msg-input { flex: 1; }
        button[type="submit"] { background: var(--primary); color: #fff; border: none; padding: 12px 20px; border-radius: 8px; font-size: 1rem; font-weight: bold; cursor: pointer; transition: background 0.2s; }
        button[type="submit"]:hover { background: var(--primary-hover); }

        /* Mobile tweaks */
        @media (max-width: 500px) {
            #username { width: 80px; }
            .input-area { padding: 10px; gap: 5px; }
            header { padding: 12px; }
        }
    </style>
</head>
<body>

<div class="chat-container">
    <header>
        <h2>👨‍💻 Coder Chat</h2>
        <button class="theme-btn" id="theme-toggle">☀️ Light</button>
    </header>
    
    <ul id="messages"></ul>

    <form class="input-area" id="chat-form">
        <input type="text" id="username" placeholder="Name" required maxlength="12">
        <input type="text" id="msg-input" placeholder="Type message or paste code..." autocomplete="off" required>
        <button type="submit">Send</button>
    </form>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>
<script>
    // Theme Logic
    const themeToggle = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;
    const hlStyle = document.getElementById('hl-style');

    // Load saved theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    htmlEl.setAttribute('data-theme', savedTheme);
    updateThemeUI(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = htmlEl.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        htmlEl.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeUI(newTheme);
    });

    function updateThemeUI(theme) {
        if (theme === 'dark') {
            themeToggle.innerText = '☀️ Light';
            hlStyle.href = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-dark.min.css';
        } else {
            themeToggle.innerText = '🌙 Dark';
            hlStyle.href = 'https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/atom-one-light.min.css';
        }
    }

    // Socket.io Chat Logic
    const socket = io();
    const chatForm = document.getElementById('chat-form');
    const msgInput = document.getElementById('msg-input');
    const usernameInput = document.getElementById('username');
    const messages = document.getElementById('messages');

    // Safe HTML escape
    function escapeHtml(text) {
        return text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const user = usernameInput.value.trim();
        const text = msgInput.value.trim();
        
        if (user && text) {
            socket.emit('message', { user, text });
            msgInput.value = '';
        }
    });

    socket.on('message', (data) => {
        const li = document.createElement('li');
        li.className = 'msg';
        
        const safeUser = escapeHtml(data.user);
        const safeText = escapeHtml(data.text);
        
        // Render as code if it looks like code, else normal text
        li.innerHTML = `<span class="msg-header">${safeUser}</span>
                        <pre><code>${safeText}</code></pre>`;
        
        messages.appendChild(li);
        
        // Apply syntax highlighting to the new message
        document.querySelectorAll('pre code').forEach((el) => {
            hljs.highlightElement(el);
        });

        // Scroll to bottom smoothly
        messages.scrollTo({ top: messages.scrollHeight, behavior: 'smooth' });
    });
</script>
</body>
</html>
EOF
