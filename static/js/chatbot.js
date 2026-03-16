/* FarmSphere — Chatbot JS */
let chatHistory = [];
let isBusy = false;

const chatInput  = document.getElementById('chatInput');
const sendBtn    = document.getElementById('sendBtn');
const chatMsgs   = document.getElementById('chatMessages');

// Auto-resize textarea
chatInput?.addEventListener('input', () => {
    chatInput.style.height = 'auto';
    chatInput.style.height = Math.min(chatInput.scrollHeight, 120) + 'px';
});

// Send on Enter (Shift+Enter = newline)
chatInput?.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); sendMessage(); }
});

function askBot(q) {
    chatInput.value = q;
    sendMessage();
}

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text || isBusy) return;

    appendMsg('user', text);
    chatHistory.push({ role:'user', content:text });
    chatInput.value = '';
    chatInput.style.height = 'auto';

    isBusy = true;
    sendBtn.disabled = true;
    showTyping();

    const fd = new FormData();
    fd.append('message', text);
    fd.append('history', JSON.stringify(chatHistory.slice(-12)));

    try {
        const d = await apiFetch('/api/chat', { method:'POST', body:fd });
        removeTyping();
        const reply = d.reply || d.response || 'Sorry, I could not generate a response.';
        appendMsg('bot', reply);
        chatHistory.push({ role:'assistant', content:reply });
    } catch (err) {
        removeTyping();
        appendMsg('bot', '⚠️ Connection error. Please check your server and try again.');
    } finally {
        isBusy = false;
        sendBtn.disabled = false;
    }
}

function appendMsg(role, text) {
    const isBot = role === 'bot';
    const time  = new Date().toLocaleTimeString('en-IN', { hour:'2-digit', minute:'2-digit' });

    // Lightweight markdown: **bold**, line breaks
    const html = text
        .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
        .replace(/\n/g, '<br>');

    const div = document.createElement('div');
    div.className = `msg ${isBot ? 'bot-msg' : 'user-msg'}`;
    div.innerHTML = `
        <div class="msg-av">${isBot ? '🤖' : '👨‍🌾'}</div>
        <div>
            <div class="msg-bubble">${html}</div>
            <div class="msg-time">${isBot ? 'FarmBot' : 'You'} · ${time}</div>
        </div>`;
    chatMsgs.appendChild(div);
    chatMsgs.scrollTop = chatMsgs.scrollHeight;
}

function showTyping() {
    const div = document.createElement('div');
    div.className = 'msg bot-msg';
    div.id = 'typingDot';
    div.innerHTML = `
        <div class="msg-av">🤖</div>
        <div class="typing-bubble">
            <span class="td"></span><span class="td"></span><span class="td"></span>
        </div>`;
    chatMsgs.appendChild(div);
    chatMsgs.scrollTop = chatMsgs.scrollHeight;
}

function removeTyping() {
    document.getElementById('typingDot')?.remove();
}

function clearChat() {
    chatHistory = [];
    chatMsgs.innerHTML = '';
    appendMsg('bot', '🔄 Chat cleared! Ask me anything about farming.');
}
