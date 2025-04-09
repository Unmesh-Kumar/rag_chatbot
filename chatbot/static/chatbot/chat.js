const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const clearChatBtn = document.getElementById('clear-chat');

let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

function appendMessage(sender, message) {
    const container = document.createElement('div');
    container.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start');

    const bubble = document.createElement('div');
    bubble.classList.add('p-3', 'rounded-lg', 'max-w-[75%]', 'whitespace-pre-wrap', 'flex', 'items-start', 'gap-2');

    if (sender === 'user') {
        bubble.classList.add('bg-blue-100');
    } else {
        bubble.classList.add('bg-green-100');
    }

    const avatar = document.createElement('div');
    avatar.textContent = sender === 'user' ? '🧑' : '🤖';

    const text = document.createElement('div');
    text.innerHTML = ` ${message}`;

    bubble.appendChild(avatar);
    bubble.appendChild(text);
    container.appendChild(bubble);
    chatBox.appendChild(container);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function renderChatHistory() {
    chatBox.innerHTML = '';
    chatHistory.forEach(({ role, content }) => {
        appendMessage(role === 'user' ? 'user' : 'bot', content);
    });
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage('user', question);
    chatHistory.push({ role: 'user', content: question });
    userInput.value = '';
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));

    try {
        const response = await fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            },
            body: JSON.stringify({ question, history: chatHistory })
        });
        const data = await response.json();
        appendMessage('bot', data.answer);
        chatHistory.push({ role: 'bot', content: data.answer });
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    } catch (error) {
        appendMessage('bot', "❌ Sorry, something went wrong.");
    }
});

userInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.dispatchEvent(new Event("submit"));
    }
});

function getCSRFToken() {
    const name = 'csrftoken';
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return '';
}

clearChatBtn.addEventListener('click', () => {
    chatHistory = [];
    localStorage.removeItem('chatHistory');
    chatBox.innerHTML = '';
});

// On page load
renderChatHistory();