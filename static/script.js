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
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMsg })
        });

        const data = await res.json();
        await streamText(botDiv, data.reply, data.session_id);
    } catch (err) {
        botDiv.innerHTML = '<p style="color: red;">Failed to fetch response.</p>';
    }
    chatDiv.scrollTop = chatDiv.scrollHeight;
};

function appendMessage(sender, text) {
    const div = document.createElement('div');
    div.className = sender;

    if (sender === 'bot' && text) {
        div.innerHTML = marked.parse(text);
    } else if (sender === 'bot') {
        div.innerHTML = ''; // Placeholder
    } else {
        div.textContent = text;
    }

    chatDiv.appendChild(div);
    return div;
}

async function streamText(element, fullText, sessionId) {
    let displayed = '';
    for (let i = 0; i < fullText.length; i++) {
        displayed += fullText[i];
        element.innerHTML = marked.parse(displayed);
        chatDiv.scrollTop = chatDiv.scrollHeight;
        await new Promise(r => setTimeout(r, 10));
    }

    const endBtn = document.getElementById('end-chat');
    if (endBtn) {
        endBtn.onclick = () => {
            console.log('End chat button clicked, showing feedback form');
            if (element.nextSibling && element.nextSibling.classList?.contains('feedback-form')) return;

            const feedbackForm = document.createElement('form');
            feedbackForm.className = 'feedback-form';
            feedbackForm.id = 'feedback-form';
            feedbackForm.setAttribute('aria-label', 'Feedback form');

            const questions = [
                { id: 'correctness', text: 'How correct was the response?' },
                { id: 'relevance', text: 'How relevant was the response?' },
                { id: 'clarity', text: 'How clear was the response?' },
                { id: 'satisfaction', text: 'How satisfied are you with the response?' }
            ];

            questions.forEach(q => {
                const fieldset = document.createElement('fieldset');
                fieldset.setAttribute('role', 'group');
                const legend = document.createElement('legend');
                legend.textContent = q.text;
                fieldset.appendChild(legend);

                const slider = document.createElement('input');
                slider.type = 'range';
                slider.name = q.id;
                slider.min = '0';
                slider.max = '9';
                slider.value = '5';
                slider.required = true;

                const valueLabel = document.createElement('span');
                valueLabel.textContent = slider.value;

                slider.oninput = () => {
                    valueLabel.textContent = slider.value;
                };

                fieldset.appendChild(slider);
                fieldset.appendChild(valueLabel);

                feedbackForm.appendChild(fieldset);
            });

            const commentFieldset = document.createElement('fieldset');
            commentFieldset.setAttribute('role', 'group');
            const commentLegend = document.createElement('legend');
            commentLegend.textContent = 'Additional comments';
            commentFieldset.appendChild(commentLegend);

            const commentBox = document.createElement('textarea');
            commentBox.name = 'comments';
            commentBox.rows = 6;
            commentBox.placeholder = 'Enter any additional feedback here...';
            commentFieldset.appendChild(commentBox);

            feedbackForm.appendChild(commentFieldset);

            const submitBtn = document.createElement('button');
            submitBtn.type = 'submit';
            submitBtn.className = 'submit-feedback';
            submitBtn.textContent = 'Submit';
            feedbackForm.appendChild(submitBtn);

            element.parentNode.insertBefore(feedbackForm, element.nextSibling);

            feedbackForm.onsubmit = async (e) => {
                e.preventDefault();
                submitBtn.disabled = true;

                const feedback = {};
                questions.forEach(q => {
                    feedback[q.id] = parseInt(feedbackForm[q.id].value, 10);
                });
                feedback.comments = feedbackForm.comments.value;

                try {
                    await fetch('/feedback', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ ...feedback, session_id: sessionId }),
                    });
                    feedbackForm.style.opacity = '1';
                    feedbackForm.innerHTML = '<p>Thank you for your feedback!</p>';
                    setTimeout(() => {
                        feedbackForm.style.opacity = '0';
                        setTimeout(() => {
                            chatDiv.innerHTML = '';
                            input.value = '';
                        }, 500);
                    }, 3000);
                } catch (error) {
                    feedbackForm.innerHTML = '<p>Failed to submit feedback. Please try again.</p>';
                }
            };
        };
    }
}
