const chatBox = document.getElementById('chat-box');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const clearChatBtn = document.getElementById('clear-chat');
const toggleLimitBtn = document.getElementById('toggle-limit');
const limitToggleText = '100 Messages History Limit';

let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
let isLimitEnabled = JSON.parse(localStorage.getItem('limitTo100')) || false;

function appendMessage(sender, message) {
    const container = document.createElement('div');
    container.classList.add('flex', sender === 'user' ? 'justify-end' : 'justify-start');

    const bubble = document.createElement('div');
    bubble.classList.add('p-3', 'rounded-lg', 'max-w-[75%]', 'whitespace-pre-wrap', 'flex', 'items-start', 'gap-2');
    bubble.classList.add(sender === 'user' ? 'bg-blue-100' : 'bg-green-100');

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

function updateChatHistory() {
    if (isLimitEnabled && chatHistory.length > 100) {
        chatHistory = chatHistory.slice(-100);
    }
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const question = userInput.value.trim();
    if (!question) return;

    appendMessage('user', question);
    chatHistory.push({ role: 'user', content: question });
    userInput.value = '';
    updateChatHistory();

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
        updateChatHistory();
    } catch (error) {
        appendMessage('bot', "❌ Sorry, something went wrong.");
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

toggleLimitBtn.addEventListener('click', () => {
    isLimitEnabled = !isLimitEnabled;
    localStorage.setItem('limitTo100', JSON.stringify(isLimitEnabled));
    updateLimitButtonText();

    if (isLimitEnabled && chatHistory.length > 100) {
        chatHistory = chatHistory.slice(-100);
        updateChatHistory();
        renderChatHistory();
    }
});

function updateLimitButtonText() {
    toggleLimitBtn.textContent = isLimitEnabled ? `${limitToggleText}: ON` : `${limitToggleText}: OFF`;
}

updateLimitButtonText();
renderChatHistory();

userInput.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        chatForm.dispatchEvent(new Event("submit"));
    }
});