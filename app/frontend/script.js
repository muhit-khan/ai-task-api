// Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = '/ai-task/';

// DOM Elements
const chatMessages = document.getElementById('chatMessages');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');
const taskType = document.getElementById('taskType');
const contextInput = document.getElementById('contextInput');
const contextText = document.getElementById('contextText');
const platformInput = document.getElementById('platformInput');
const platformType = document.getElementById('platformType');
const newChatBtn = document.getElementById('newChatBtn');
const chatHistory = document.getElementById('chatHistory');
const apiStatus = document.getElementById('apiStatus');

// State
let currentChat = [];
let chatHistoryList = JSON.parse(localStorage.getItem('chatHistory')) || [];

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load chat history
    renderChatHistory();
    
    // Check API status
    checkApiStatus();
    
    // Set up event listeners
    setupEventListeners();
    
    // Set initial task type
    handleTaskTypeChange();
});

// Set up event listeners
function setupEventListeners() {
    // Send message on button click
    sendBtn.addEventListener('click', sendMessage);
    
    // Send message on Enter key (but allow Shift+Enter for new line)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Auto-resize textarea
    userInput.addEventListener('input', () => {
        userInput.style.height = 'auto';
        userInput.style.height = Math.min(userInput.scrollHeight, 200) + 'px';
    });
    
    // Task type change
    taskType.addEventListener('change', handleTaskTypeChange);
    
    // New chat button
    newChatBtn.addEventListener('click', startNewChat);
    
    // Auto-save chat to history periodically
    setInterval(saveCurrentChat, 30000); // Every 30 seconds
}

// Handle task type change
function handleTaskTypeChange() {
    const selectedTask = taskType.value;
    
    // Show/hide context input
    if (selectedTask === 'qa') {
        contextInput.classList.remove('hidden');
    } else {
        contextInput.classList.add('hidden');
    }
    
    // Show/hide platform input
    if (selectedTask === 'content_generation') {
        platformInput.classList.remove('hidden');
    } else {
        platformInput.classList.add('hidden');
    }
}

// Check API status
async function checkApiStatus() {
    try {
        const response = await fetch(`${API_BASE_URL}/`);
        if (response.ok) {
            apiStatus.innerHTML = '<i class="fas fa-circle"></i> API Connected';
            apiStatus.className = 'status-indicator connected';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        apiStatus.innerHTML = '<i class="fas fa-circle"></i> API Disconnected';
        apiStatus.className = 'status-indicator disconnected';
        console.error('API connection error:', error);
    }
}

// Send message
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    const selectedTask = taskType.value;
    
    // Add user message to chat
    addMessageToChat('user', message, selectedTask);
    
    // Clear input
    userInput.value = '';
    userInput.style.height = 'auto';
    
    // Disable send button while processing
    sendBtn.disabled = true;
    
    // Add loading indicator
    const loadingElement = addLoadingIndicator();
    
    try {
        // Prepare request payload
        let payload = { task: selectedTask };
        
        switch (selectedTask) {
            case 'qa':
                payload.question = message;
                if (contextText.value.trim()) {
                    payload.context = contextText.value.trim();
                }
                break;
            case 'content_generation':
                payload.prompt = message;
                payload.platform = platformType.value;
                break;
            case 'image_generation':
                payload.prompt = message;
                break;
            case 'latest_answer':
                // No additional parameters needed
                break;
        }
        
        // Send request to API
        const response = await fetch(`${API_BASE_URL}${API_ENDPOINT}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(payload),
        });
        
        // Remove loading indicator
        loadingElement.remove();
        
        if (response.ok) {
            const data = await response.json();
            addMessageToChat('ai', data.result, selectedTask);
        } else {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `API Error: ${response.status}`);
        }
    } catch (error) {
        // Remove loading indicator
        loadingElement.remove();
        
        // Add error message
        addErrorMessage(error.message);
        console.error('Error sending message:', error);
    } finally {
        // Re-enable send button
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Add message to chat
function addMessageToChat(sender, content, taskType = '') {
    const messageElement = document.createElement('div');
    messageElement.className = `message ${sender}-message`;
    
    const avatar = sender === 'user' ? 
        '<div class="message-avatar user-avatar"><i class="fas fa-user"></i></div>' :
        '<div class="message-avatar ai-avatar"><i class="fas fa-robot"></i></div>';
    
    const senderName = sender === 'user' ? 'You' : 'AI Assistant';
    const taskName = getTaskDisplayName(taskType);
    
    let contentHtml = '';
    if (sender === 'ai' && taskType === 'image_generation') {
        // Handle image generation result
        if (content.startsWith('Error') || content.includes('simulated')) {
            contentHtml = `<p>${content}</p>`;
        } else {
            // For base64 images, we would display them, but for now we'll show a placeholder
            contentHtml = `
                <p>Image generated successfully!</p>
                <div class="image-placeholder">
                    <p>Image Preview (Base64 data not rendered in this demo)</p>
                </div>
            `;
        }
    } else {
        // Handle regular text content
        contentHtml = `<p>${escapeHtml(content)}</p>`;
    }
    
    messageElement.innerHTML = `
        ${avatar}
        <div class="message-content">
            <div class="message-header">
                <h4>${senderName}${taskType ? ` (${taskName})` : ''}</h4>
                <span class="message-timestamp">${getCurrentTime()}</span>
            </div>
            ${contentHtml}
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    
    // Add to current chat history
    currentChat.push({
        sender,
        content,
        taskType,
        timestamp: new Date().toISOString()
    });
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Add loading indicator
function addLoadingIndicator() {
    const loadingElement = document.createElement('div');
    loadingElement.className = 'message ai-message';
    loadingElement.innerHTML = `
        <div class="message-avatar ai-avatar"><i class="fas fa-robot"></i></div>
        <div class="message-content">
            <div class="message-header">
                <h4>AI Assistant</h4>
                <span class="message-timestamp">${getCurrentTime()}</span>
            </div>
            <div class="loading-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    chatMessages.appendChild(loadingElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return loadingElement;
}

// Add error message
function addErrorMessage(message) {
    const errorElement = document.createElement('div');
    errorElement.className = 'message ai-message';
    errorElement.innerHTML = `
        <div class="message-avatar ai-avatar"><i class="fas fa-robot"></i></div>
        <div class="message-content">
            <div class="message-header">
                <h4>AI Assistant</h4>
                <span class="message-timestamp">${getCurrentTime()}</span>
            </div>
            <div class="error-message">
                <strong>Error:</strong> ${escapeHtml(message)}
            </div>
        </div>
    `;
    chatMessages.appendChild(errorElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Get current time formatted
function getCurrentTime() {
    return new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Get task display name
function getTaskDisplayName(taskType) {
    const names = {
        'qa': 'Q&A',
        'content_generation': 'Content Generation',
        'image_generation': 'Image Generation',
        'latest_answer': 'Latest Answer'
    };
    return names[taskType] || taskType;
}

// Start new chat
function startNewChat() {
    // Save current chat if it has messages
    if (currentChat.length > 0) {
        saveCurrentChat();
    }
    
    // Clear chat messages
    chatMessages.innerHTML = `
        <div class="welcome-message">
            <div class="welcome-content">
                <h2>Welcome to AI Task Interface</h2>
                <p>I can help you with various AI tasks. Select a task type and start chatting!</p>
                <div class="features-grid">
                    <div class="feature-card">
                        <i class="fas fa-question-circle"></i>
                        <h3>Q&A</h3>
                        <p>Ask questions with optional context</p>
                    </div>
                    <div class="feature-card">
                        <i class="fas fa-file-alt"></i>
                        <h3>Content</h3>
                        <p>Generate platform-specific content</p>
                    </div>
                    <div class="feature-card">
                        <i class="fas fa-image"></i>
                        <h3>Images</h3>
                        <p>Create images from text prompts</p>
                    </div>
                    <div class="feature-card">
                        <i class="fas fa-history"></i>
                        <h3>History</h3>
                        <p>Retrieve previous answers</p>
                    </div>
                </div>
            </div>
        </div>
    `;
    
    // Reset context and platform inputs
    contextText.value = '';
    platformType.value = 'twitter';
    handleTaskTypeChange();
    
    // Clear current chat
    currentChat = [];
    
    // Update UI
    userInput.focus();
}

// Save current chat to history
function saveCurrentChat() {
    if (currentChat.length === 0) return;
    
    // Create chat summary from first message
    const firstMessage = currentChat[0].content;
    const summary = firstMessage.length > 30 ? firstMessage.substring(0, 30) + '...' : firstMessage;
    
    // Create chat object
    const chat = {
        id: Date.now(),
        summary: summary,
        timestamp: new Date().toISOString(),
        messages: [...currentChat]
    };
    
    // Add to beginning of history
    chatHistoryList.unshift(chat);
    
    // Keep only last 20 chats
    if (chatHistoryList.length > 20) {
        chatHistoryList = chatHistoryList.slice(0, 20);
    }
    
    // Save to localStorage
    localStorage.setItem('chatHistory', JSON.stringify(chatHistoryList));
    
    // Update UI
    renderChatHistory();
}

// Render chat history
function renderChatHistory() {
    chatHistory.innerHTML = '';
    
    chatHistoryList.forEach(chat => {
        const chatElement = document.createElement('div');
        chatElement.className = 'chat-history-item';
        chatElement.innerHTML = `
            <i class="fas fa-comment"></i>
            <span>${escapeHtml(chat.summary)}</span>
        `;
        chatElement.addEventListener('click', () => loadChat(chat));
        chatHistory.appendChild(chatElement);
    });
}

// Load chat from history
function loadChat(chat) {
    // Clear current chat
    startNewChat();
    
    // Load messages
    chat.messages.forEach(message => {
        addMessageToChat(message.sender, message.content, message.taskType);
    });
    
    // Update current chat
    currentChat = [...chat.messages];
}

// Periodically check API status
setInterval(checkApiStatus, 30000); // Every 30 seconds