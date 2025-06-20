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

    await streamText(botDiv, data.reply, data.reply_id);
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

async function streamText(element, fullText, replyId) {
    let displayed = '';
    for (let i = 0; i < fullText.length; i++) {
        displayed += fullText[i];
        element.innerHTML = marked.parse(displayed);
        chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 10));
    }

    // Create feedback panel container
    const feedbackPanel = document.createElement('div');
    feedbackPanel.className = 'bot feedback-panel';
    feedbackPanel.setAttribute('role', 'radiogroup');
    feedbackPanel.setAttribute('aria-label', 'How helpful did you find this response?');

    // Create label
    const label = document.createElement('p');
    label.textContent = 'How helpful did you find this response?';
    feedbackPanel.appendChild(label);

    // Create buttons 0-5 for feedback
    for (let i = 0; i <= 5; i++) {
        const btn = document.createElement('button');
        btn.className = 'feedback-btn';
        btn.type = 'button';
        btn.textContent = i;
        btn.setAttribute('role', 'radio');
        btn.setAttribute('aria-checked', 'false');
        btn.dataset.value = i;
        feedbackPanel.appendChild(btn);
    }

    // Add submit button
    const submitBtn = document.createElement('button');
    submitBtn.className = 'submit-feedback';
    submitBtn.textContent = 'Submit';
    submitBtn.disabled = true; // disabled until user picks a rating
    feedbackPanel.appendChild(submitBtn);

    console.log(element, element.parentNode, element.nextSibling);
    element.parentNode.insertBefore(feedbackPanel, element.nextSibling);

    // Track selected rating
    let selectedRating = null;

    // Handle button clicks (select rating)
    feedbackPanel.querySelectorAll('.feedback-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            // Clear all aria-checked
            feedbackPanel.querySelectorAll('.feedback-btn').forEach(b => {
                b.setAttribute('aria-checked', 'false');
                b.classList.remove('selected');
            });

            // Mark clicked button as selected
            btn.setAttribute('aria-checked', 'true');
            btn.classList.add('selected');
            selectedRating = btn.dataset.value;
            submitBtn.disabled = false;
        });
    });

    // Submit feedback
    submitBtn.onclick = async () => {
        if (selectedRating === null) return;

        submitBtn.disabled = true;

        try {
            await fetch('/feedback', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ feedback: parseInt(selectedRating), reply_id: replyId }),
            });
            feedbackPanel.innerHTML = '';
        } catch (error) {
            feedbackPanel.innerHTML = '<p>Failed to submit feedback. Please try again.</p>';
        }
    };
}

