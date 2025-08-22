// Configuration
const API_BASE_URL = 'http://localhost:8000';
const API_ENDPOINT = '/ai-task/';
const MODEL_INFO_ENDPOINT = '/ai-task/models/info';
const MODEL_STATUS_ENDPOINT = '/ai-task/models/status';
const MODEL_VALIDATE_ENDPOINT = '/ai-task/models/validate';

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
const charCount = document.getElementById('charCount');
const mobileToggle = document.getElementById('mobileToggle');
const sidebar = document.querySelector('.sidebar');

// State
let currentChat = [];
let chatHistoryList = JSON.parse(localStorage.getItem('chatHistory')) || [];
let modelInfo = null;
let isConnected = false;

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load chat history
    renderChatHistory();

    // Check API status and load model info
    initializeApp();

    // Set up event listeners
    setupEventListeners();

    // Set initial task type
    handleTaskTypeChange();

    // Setup character counter
    setupCharacterCounter();
});

// Initialize app with API and model info
async function initializeApp() {
    try {
        await checkApiStatus();
        if (isConnected) {
            await loadModelInfo();
        }
    } catch (error) {
        console.error('Failed to initialize app:', error);
    }
}

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

        // Update character count and send button state
        updateCharacterCount();
        updateSendButtonState();
    });

    // Task type change
    taskType.addEventListener('change', handleTaskTypeChange);

    // New chat button
    newChatBtn.addEventListener('click', startNewChat);

    // Mobile sidebar toggle
    if (mobileToggle) {
        mobileToggle.addEventListener('click', toggleMobileSidebar);
    }

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && sidebar.classList.contains('open')) {
            if (!sidebar.contains(e.target) && !mobileToggle.contains(e.target)) {
                closeMobileSidebar();
            }
        }
    });

    // Handle window resize
    window.addEventListener('resize', () => {
        if (window.innerWidth > 768) {
            sidebar.classList.remove('open');
        }
    });

    // Feature card click handlers
    document.addEventListener('click', (e) => {
        const featureCard = e.target.closest('.feature-card');
        if (featureCard && featureCard.dataset.task) {
            const task = featureCard.dataset.task;
            taskType.value = task;
            handleTaskTypeChange();

            // Focus on input after selection
            setTimeout(() => {
                userInput.focus();
            }, 100);
        }
    });

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
            isConnected = true;
            apiStatus.innerHTML = '<i class="fas fa-circle"></i> <span>API Connected</span>';
            apiStatus.className = 'status-indicator connected';

            // Load model information when connected
            await loadModelInfo();
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        isConnected = false;
        apiStatus.innerHTML = '<i class="fas fa-circle"></i> <span>API Disconnected</span>';
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
            console.log('API Response data:', data); // Debug log
            console.log('Content length:', data.result?.length); // Debug log
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
        if (content.startsWith('Error') || content.includes('simulated') || content.includes('failed')) {
            contentHtml = `<div class="error-content"><p>${escapeHtml(content)}</p></div>`;
        } else {
            // Display actual base64 image
            contentHtml = `
                <div class="image-result">
                    <p><strong>Image generated successfully!</strong></p>
                    <div class="image-container">
                        <img src="data:image/png;base64,${content}" alt="Generated image" class="generated-image" 
                             loading="lazy" 
                             onerror="this.onerror=null; this.src=''; this.alt='Failed to load image'; this.className='image-error';">
                        <div class="image-actions">
                            <button class="download-btn" onclick="downloadImage('${content}', 'ai-generated-image.png')">
                                <i class="fas fa-download"></i> Download
                            </button>
                        </div>
                    </div>
                </div>
            `;
        }
    } else {
        // Handle regular text content with better formatting
        const formattedContent = formatTextContent(content);
        contentHtml = `<div class="text-content">${formattedContent}</div>`;
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

    // Add copy buttons if this is a content generation message
    if (sender === 'ai' && taskType === 'content_generation') {
        setTimeout(() => addCopyButtonsToContentPosts(messageElement), 100);
    }

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
                <p>Choose a task below and start chatting with our AI assistant!</p>
                <div class="features-grid">
                    <div class="feature-card" data-task="qa">
                        <i class="fas fa-question-circle"></i>
                        <h3>Q&A</h3>
                        <p>Ask questions with optional context</p>
                    </div>
                    <div class="feature-card" data-task="content_generation">
                        <i class="fas fa-file-alt"></i>
                        <h3>Content</h3>
                        <p>Generate platform-specific content</p>
                    </div>
                    <div class="feature-card" data-task="image_generation">
                        <i class="fas fa-image"></i>
                        <h3>Images</h3>
                        <p>Create images from text prompts</p>
                    </div>
                    <div class="feature-card" data-task="latest_answer">
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

// Setup character counter
function setupCharacterCounter() {
    updateCharacterCount();
}

// Update character count display
function updateCharacterCount() {
    if (!charCount) return;
    const count = userInput.value.length;
    const maxLength = userInput.maxLength || 4000;
    charCount.textContent = `${count}/${maxLength}`;

    if (count > maxLength * 0.9) {
        charCount.classList.add('warning');
    } else {
        charCount.classList.remove('warning');
    }
}

// Update send button state
function updateSendButtonState() {
    const hasText = userInput.value.trim().length > 0;
    const selectedTask = taskType.value;

    // Enable send button if there's text, except for latest_answer which doesn't need input
    sendBtn.disabled = !hasText && selectedTask !== 'latest_answer';
}

// Load model information
async function loadModelInfo() {
    try {
        const response = await fetch(`${API_BASE_URL}${MODEL_STATUS_ENDPOINT}`);
        if (response.ok) {
            modelInfo = await response.json();
            updateModelDisplay();
        }
    } catch (error) {
        console.error('Failed to load model info:', error);
    }
}

// Update model display in UI
function updateModelDisplay() {
    if (modelInfo) {
        // Update task hints based on current models
        updateTaskHints();
    }
}

// Update task hints based on selected task
function updateTaskHints() {
    const selectedTask = taskType.value;
    const hints = {
        'qa': 'Ask questions with optional context for better answers',
        'content_generation': 'Generate platform-specific content for social media',
        'image_generation': 'Describe what image you want to create',
        'latest_answer': 'Retrieve your most recent answer (no input needed)'
    };

    const hintElement = document.getElementById('taskHint');
    if (hintElement) {
        hintElement.textContent = hints[selectedTask] || '';
    }
}

// Helper function to decode HTML entities
function decodeHtmlEntities(text) {
    if (!text) return '';

    // Create a temporary div element to decode HTML entities
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = text;
    let decoded = tempDiv.textContent || tempDiv.innerText || '';

    // Additional manual decoding for common entities that might still be present
    const entityMap = {
        '&#039;': "'",
        '&quot;': '"',
        '&amp;': '&',
        '&lt;': '<',
        '&gt;': '>',
        '&#x27;': "'",
        '&#x2F;': '/',
        '&#x60;': '`',
        '&#x3D;': '='
    };

    // Replace any remaining HTML entities
    for (const [entity, char] of Object.entries(entityMap)) {
        decoded = decoded.replace(new RegExp(entity, 'g'), char);
    }

    return decoded;
}

// Helper function to clean HTML entities from final output
function cleanHtmlEntities(html) {
    if (!html) return '';

    return html
        .replace(/&#039;/g, "'")
        .replace(/&quot;/g, '"')
        .replace(/&amp;/g, '&')
        .replace(/&lt;/g, '<')
        .replace(/&gt;/g, '>')
        .replace(/&#x27;/g, "'")
        .replace(/&#x2F;/g, '/')
        .replace(/&#x60;/g, '`')
        .replace(/&#x3D;/g, '=');
}

// Format text content for better display with markdown support
function formatTextContent(text) {
    if (!text) return '';

    // First decode HTML entities (like &#039; to apostrophe)
    let formatted = decodeHtmlEntities(text);

    // Then escape HTML to prevent XSS, but preserve our formatting
    formatted = escapeHtml(formatted);

    // Enhanced markdown parsing with better regex patterns
    // Convert markdown-style bold formatting **text** to <strong>
    formatted = formatted.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Convert markdown-style italic formatting *text* to <em>
    formatted = formatted.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Convert markdown-style code formatting `code` to <code>
    formatted = formatted.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Convert URLs to links
    formatted = formatted.replace(
        /(https?:\/\/[^\s<>"]+)/gi,
        '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
    );

    // Convert hashtags to styled spans
    formatted = formatted.replace(
        /#([a-zA-Z0-9_]+)/g,
        '<span class="hashtag">#$1</span>'
    );

    // Convert @mentions to styled spans
    formatted = formatted.replace(
        /@([a-zA-Z0-9_]+)/g,
        '<span class="mention">@$1</span>'
    );

    // Check for various content patterns that indicate multiple posts
    const multiPostPatterns = [
        /Option\s+\d+:/gi,                           // "Option 1:", "Option 2:", etc.
        /\*\*(Post|Tweet|Caption|Description)\s+\d+:/gi,  // "**Post 1:**", etc.
        />(.*?)</g,                                  // "> content" (quoted content)
        /\d+\./g                                     // Numbered lists
    ];

    let hasMultiplePosts = multiPostPatterns.some(pattern => pattern.test(formatted));

    if (hasMultiplePosts) {
        // Handle "Option X:" format specifically
        if (/Option\s+\d+:/gi.test(formatted)) {
            const sections = formatted.split(/(?=Option\s+\d+:)/gi)
                .filter(section => section.trim())
                .map(section => section.trim());

            console.log('Parsed Option sections:', sections);

            if (sections.length > 1) {
                const formattedSections = sections.map((section, index) => {
                    if (section) {
                        // Convert line breaks and handle quoted content
                        let sectionContent = section
                            .replace(/\n/g, '<br>')
                            .replace(/&gt;\s*(.*?)(?=<br>|$)/g, '<blockquote>$1</blockquote>');

                        return `<div class="content-post" data-post="${index + 1}">
                            <div class="content-text">${sectionContent}</div>
                        </div>`;
                    }
                    return '';
                }).filter(Boolean);

                return cleanHtmlEntities(`<div class="content-posts-container">${formattedSections.join('')}</div>`);
            }
        }

        // Handle standard "**Post X:**" format
        else if (/\*\*(Post|Tweet|Caption|Description)\s+\d+:/gi.test(formatted)) {
            const sections = formatted.split(/(?=\*\*(?:Post|Tweet|Caption|Description)\s+\d+[:\*])/i)
                .filter(section => section.trim())
                .map(section => section.trim());

            console.log('Parsed standard sections:', sections);

            if (sections.length > 1) {
                const formattedSections = sections.map((section, index) => {
                    if (section) {
                        const sectionWithBreaks = section.replace(/\n/g, '<br>');
                        return `<div class="content-post" data-post="${index + 1}">
                            <div class="content-text">${sectionWithBreaks}</div>
                        </div>`;
                    }
                    return '';
                }).filter(Boolean);

                return cleanHtmlEntities(`<div class="content-posts-container">${formattedSections.join('')}</div>`);
            }
        }
    }

    // If no multiple posts detected, handle as single content
    // Convert line breaks to <br> tags
    formatted = formatted.replace(/\n/g, '<br>');

    // Final decode of any remaining HTML entities
    formatted = decodeHtmlEntities(formatted);

    // For single content or other formats
    let result = `<div class="content-text">${formatted}</div>`;

    // Ensure final HTML entity decoding throughout the entire result
    return cleanHtmlEntities(result);
}

// Download image function
function downloadImage(base64Data, filename) {
    try {
        const link = document.createElement('a');
        link.href = `data:image/png;base64,${base64Data}`;
        link.download = filename;
        link.style.display = 'none';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    } catch (error) {
        console.error('Failed to download image:', error);
        alert('Failed to download image. Please try again.');
    }
}

// Mobile sidebar toggle functions
function toggleMobileSidebar() {
    if (sidebar.classList.contains('open')) {
        closeMobileSidebar();
    } else {
        openMobileSidebar();
    }
}

function openMobileSidebar() {
    sidebar.classList.add('open');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling
}

function closeMobileSidebar() {
    sidebar.classList.remove('open');
    document.body.style.overflow = ''; // Restore scrolling
}

// Touch gesture support for mobile sidebar
let touchStartX = 0;
let touchEndX = 0;

// Add touch event listeners for swipe gestures
document.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
});

document.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    handleSwipeGesture();
});

function handleSwipeGesture() {
    const swipeThreshold = 50;
    const swipeDistance = touchEndX - touchStartX;

    // Only handle swipes on mobile
    if (window.innerWidth <= 768) {
        // Swipe right to open sidebar (from left edge)
        if (swipeDistance > swipeThreshold && touchStartX < 50) {
            openMobileSidebar();
        }
        // Swipe left to close sidebar
        else if (swipeDistance < -swipeThreshold && sidebar.classList.contains('open')) {
            closeMobileSidebar();
        }
    }
}

// Add copy buttons to content posts
function addCopyButtonsToContentPosts(messageElement) {
    const contentPosts = messageElement.querySelectorAll('.content-post');
    contentPosts.forEach((post, index) => {
        if (!post.querySelector('.copy-btn')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-btn';
            copyBtn.innerHTML = '<i class="fas fa-copy"></i>';
            copyBtn.title = `Copy post ${index + 1}`;
            copyBtn.setAttribute('aria-label', `Copy post ${index + 1} to clipboard`);
            copyBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                copyPostContent(post, index + 1);
            });
            post.appendChild(copyBtn);
        }
    });
}

// Copy post content to clipboard
function copyPostContent(postElement, postNumber = null) {
    // Get the text content, removing the header and copy button
    const textContent = postElement.cloneNode(true);
    const header = textContent.querySelector('strong');
    const copyBtn = textContent.querySelector('.copy-btn');
    const successMsg = textContent.querySelector('.copy-success');

    if (header) header.remove();
    if (copyBtn) copyBtn.remove();
    if (successMsg) successMsg.remove();

    // Get clean text without HTML tags
    let cleanText = textContent.textContent.trim();

    // Remove any remaining unwanted characters
    cleanText = cleanText.replace(/\s+/g, ' ').trim();

    // Copy to clipboard
    navigator.clipboard.writeText(cleanText).then(() => {
        // Show success feedback
        const successMessage = document.createElement('div');
        successMessage.className = 'copy-success';
        successMessage.innerHTML = `<i class="fas fa-check"></i> ${postNumber ? `Post ${postNumber} ` : ''}Copied!`;
        successMessage.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: var(--success-color);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
            z-index: 10;
            animation: fadeInOut 2s ease;
            font-weight: 600;
            box-shadow: var(--shadow-md);
        `;

        postElement.style.position = 'relative';
        postElement.appendChild(successMessage);

        // Remove success message after 2 seconds
        setTimeout(() => {
            if (successMessage.parentNode) {
                successMessage.remove();
            }
        }, 2000);

        console.log('Copied text:', cleanText); // Debug log
    }).catch(err => {
        console.error('Failed to copy text: ', err);
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = cleanText;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
            alert(`${postNumber ? `Post ${postNumber} ` : ''}Copied to clipboard!`);
        } catch (fallbackErr) {
            alert('Failed to copy to clipboard');
        }
        document.body.removeChild(textArea);
    });
}

// Add CSS animation for copy success
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeInOut {
        0% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
        20% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        80% { opacity: 1; transform: translate(-50%, -50%) scale(1); }
        100% { opacity: 0; transform: translate(-50%, -50%) scale(0.8); }
    }
    
    .copy-btn {
        position: absolute;
        top: 8px;
        right: 8px;
        background: var(--bg-hover);
        border: 1px solid var(--border-primary);
        border-radius: 4px;
        padding: 4px 8px;
        cursor: pointer;
        opacity: 0;
        transition: all 0.2s ease;
        color: var(--text-secondary);
        font-size: 12px;
    }
    
    .content-post:hover .copy-btn {
        opacity: 1;
    }
    
    .copy-btn:hover {
        background: var(--text-accent);
        color: white;
        transform: scale(1.1);
    }
`;
document.head.appendChild(style);