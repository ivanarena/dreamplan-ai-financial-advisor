const chatDiv = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('message');

form.onsubmit = async (e) => {
    e.preventDefault();
    const userMsg = input.value.trim();
    if (!userMsg) return;

    appendMessage('user', userMsg);
    input.value = '';
    chatDiv.scrollTop = chatDiv.scrollHeight;

    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
    });
    const data = await res.json();
    appendMessage('bot', data.reply);
    chatDiv.scrollTop = chatDiv.scrollHeight;
};

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;
    div.textContent = (sender === 'user' ? 'You: ' : 'Bot: ') + text;
    chatDiv.appendChild(div);
}
