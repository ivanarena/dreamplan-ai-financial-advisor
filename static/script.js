const chatDiv = document.getElementById('chat');
const form = document.getElementById('chat-form');
const input = document.getElementById('message');

window.addEventListener('DOMContentLoaded', async () => {
    // Append empty bot message div first (placeholder)
    const botDiv = appendMessage('bot', '');
    // Stream the initial greeting animated
    await streamText(botDiv, `👋 **Hi there! I'm your personal financial planning assistant.**

To help you explore different retirement and savings scenarios, I'll simulate your future financial outlook using your personal data — just like in the example you'll see later. I'll send your details to our financial engine and give you a clear breakdown of your retirement income, savings, mortgage situation, and more.

**To get started, could you please share the following information:**
- Your age (required) 🧑
- Your gross monthly salary (required) 💼
- Spouse's age (if applicable) 👩‍❤️‍👨
- Spouse's gross monthly salary 💼
- Houses value 🏠
- Current mortgages or housing debts 💳
- Your current savings 💰

Once I have this, I'll calculate your financial projection and give you a detailed summary with insights and recommendations.

You can also ask me any financial questions you have about investments, pensions, savings, or other financial topics! 💭

**Ready when you are! 😊**
`);
});

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
        await new Promise(r => setTimeout(r, 20));
    }
}
