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

    const botDiv = appendMessage('bot', '...');
    const res = await fetch('/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMsg })
    });
    const data = await res.json();

    await streamText(botDiv, data.reply);
    chatDiv.scrollTop = chatDiv.scrollHeight;
};

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;

    if (sender === 'bot' && text) {
        div.innerHTML = marked.parse(text);
    } else if (sender === 'bot') {
        div.innerHTML = '';  // placeholder for streaming
    } else {
        div.textContent = text;
    }

    chatDiv.appendChild(div);
    return div;
}

async function streamText(element, fullText) {
    let displayed = '';
    for (let i = 0; i < fullText.length; i++) {
        displayed += fullText[i];
        element.innerHTML = marked.parse(displayed);
        chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 10));
    }
}
