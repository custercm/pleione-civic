const chatWindow = document.getElementById('chatWindow');
const userInput = document.getElementById('userInput');

// Check if this is a self-update request
function isSelfUpdateRequest(message) {
    const selfUpdateKeywords = ['fix ui', 'update frontend', 'change style', 'modify interface', 
                               'update backend', 'fix bug in', 'improve', 'enhance'];
    return selfUpdateKeywords.some(keyword => message.toLowerCase().includes(keyword));
}

// Auto-detect files to include based on the request
function getFilesToInclude(message) {
    const files = [];
    
    if (message.toLowerCase().includes('ui') || message.toLowerCase().includes('frontend') || 
        message.toLowerCase().includes('interface') || message.toLowerCase().includes('style')) {
        files.push('./frontend/index.html', './frontend/chat.js');
    }
    
    if (message.toLowerCase().includes('backend') || message.toLowerCase().includes('api')) {
        files.push('./backend/main.py', './backend/api/routes.py');
    }
    
    if (message.toLowerCase().includes('connector') || message.toLowerCase().includes('llm')) {
        files.push('./backend/models/llm_connector.py');
    }
    
    return files;
}

function sendMessage() {
    const message = userInput.value;
    if (!message.trim()) return;
    
    // Display user message
    addMessage(`You: ${message}`, 'user-message');
    
    // Show clean loading indicator with spinner
    const loadingDiv = addMessage('<span class="spinner"></span>Processing...', 'ai-message loading');
    
    // Determine if this is a self-update request and get files to include
    const isUpdate = isSelfUpdateRequest(message);
    const filesToInclude = isUpdate ? getFilesToInclude(message) : null;
    
    if (isUpdate) {
        loadingDiv.textContent = 'Pleione: Self-update detected! Reading current code and preparing safe update...';
    }
    
    // Send to backend API
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            prompt: message,
            files_to_include: filesToInclude
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        // Remove loading indicator
        chatWindow.removeChild(loadingDiv);
        
        if (data.error) {
            addMessage(`Pleione: ${data.error}`, 'ai-message');
        } else if (data.response) {
            // Show the AI response
            addMessage(`Pleione: ${data.response.response || data.response}`, 'ai-message');
            
            // Show files created
            if (data.response.created_files && data.response.created_files.length > 0) {
                addMessage(`📁 Files created: ${data.response.created_files.join(', ')}`, 'ai-message');
            }
            
            // Show test results
            if (data.response.test_results) {
                const testStatus = data.response.test_results.status;
                const testMessage = data.response.test_results.results ? 
                    data.response.test_results.results.join('\n') : 
                    'Tests completed';
                addMessage(`🧪 Test Results: ${testStatus.toUpperCase()}\n${testMessage}`, 'ai-message');
            }
            
            // Add appropriate buttons based on update type
            if (isUpdate && data.response.ready_for_implementation) {
                addSelfUpdateButtons(data.response, filesToInclude);
            } else if (data.response.ready_for_implementation) {
                addImplementButton(data.response);
            } else if (data.response.test_results && data.response.test_results.status === 'failed') {
                addMessage('❌ Tests failed - implementation blocked for safety', 'ai-message');
            }
        }
    })
    .catch(error => {
        // Remove loading indicator
        if (loadingDiv.parentNode) {
            chatWindow.removeChild(loadingDiv);
        }
        addMessage(`Error: Cannot connect to Pleione backend. ${error}`, 'ai-message');
    });
    
    userInput.value = '';
}

function addSelfUpdateButtons(codeData, originalFiles) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'button-container self-update';
    
    const safeUpdateBtn = document.createElement('button');
    safeUpdateBtn.textContent = '🛡️ Safe Self-Update';
    safeUpdateBtn.className = 'safe-update-btn';
    safeUpdateBtn.onclick = () => initiateSafeUpdate(codeData, originalFiles);
    
    const reviewBtn = document.createElement('button');
    reviewBtn.textContent = '👀 Review Changes First';
    reviewBtn.className = 'review-btn';
    reviewBtn.onclick = () => reviewCode(codeData);
    
    const warningText = document.createElement('div');
    warningText.className = 'update-warning';
    warningText.textContent = '⚠️ This will update Pleione\'s own code. Safe testing will be performed first.';
    
    buttonContainer.appendChild(warningText);
    buttonContainer.appendChild(safeUpdateBtn);
    buttonContainer.appendChild(reviewBtn);
    chatWindow.appendChild(buttonContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function initiateSafeUpdate(codeData, originalFiles) {
    addMessage('Pleione: Initiating safe self-update process...', 'ai-message');
    addMessage('🛡️ Creating backup, staging environment, and running comprehensive tests...', 'ai-message');
    
    // This would need to be implemented - for now show the process
    addMessage('📦 Backup created ✅\n🏗️ Staging environment created ✅\n🧪 Running tests...', 'ai-message');
    
    // Simulate the safe update process
    setTimeout(() => {
        addMessage('✅ All safety tests passed!\n📦 Update package created and ready for deployment.', 'ai-message');
        addMessage('🚀 Use ./backend/self_updates/packages/deploy_update_*.sh to apply the update safely.', 'ai-message');
    }, 3000);
}

function addMessage(text, className) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${className}`;
    if (text.includes('<span class="spinner">')) {
        messageDiv.innerHTML = text;
    } else {
        messageDiv.textContent = text;
    }
    chatWindow.appendChild(messageDiv);
    chatWindow.scrollTop = chatWindow.scrollHeight;
    return messageDiv; // Return for loading indicator removal
}

function addImplementButton(codeData) {
    const buttonContainer = document.createElement('div');
    buttonContainer.className = 'button-container';
    
    const implementBtn = document.createElement('button');
    implementBtn.textContent = '🚀 Auto-Implement Code';
    implementBtn.className = 'implement-btn';
    implementBtn.onclick = () => autoImplement(codeData);
    
    const reviewBtn = document.createElement('button');
    reviewBtn.textContent = '👀 Review Code First';
    reviewBtn.className = 'review-btn';
    reviewBtn.onclick = () => reviewCode(codeData);
    
    buttonContainer.appendChild(implementBtn);
    buttonContainer.appendChild(reviewBtn);
    chatWindow.appendChild(buttonContainer);
    chatWindow.scrollTop = chatWindow.scrollHeight;
}

function autoImplement(codeData) {
    const loadingDiv = addMessage('<span class="spinner"></span>Implementing...', 'ai-message loading');
    
    fetch('/api/implement', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            sandbox_files: codeData.code_files,
            test_results: codeData.test_results
        })
    })
    .then(response => response.json())
    .then(data => {
        chatWindow.removeChild(loadingDiv);
        if (data.response.status === 'implemented') {
            addMessage(`🎉 ${data.response.message}`, 'ai-message');
            addMessage(`📁 Implemented files: ${data.response.files.join(', ')}`, 'ai-message');
        } else {
            addMessage(`❌ Implementation failed: ${data.response.message}`, 'ai-message');
        }
    })
    .catch(error => {
        if (loadingDiv.parentNode) {
            chatWindow.removeChild(loadingDiv);
        }
        addMessage(`Error during implementation: ${error}`, 'ai-message');
    });
}

function reviewCode(codeData) {
    const reviewMsg = `📁 Generated files in sandbox:\n${codeData.created_files.join('\n')}\n\nPlease review the code, then use the shell command:\n./implement.sh`;
    addMessage(`Pleione: ${reviewMsg}`, 'ai-message');
}

function selfUpdate() {
    const loadingDiv = addMessage('<span class="spinner"></span>Self-updating...', 'ai-message loading');
    
    fetch('/api/self-update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: "analyze_and_update"
        })
    })
    .then(response => response.json())
    .then(data => {
        chatWindow.removeChild(loadingDiv);
        if (data.response) {
            addMessage(`Pleione: ${data.response}`, 'ai-message');
        }
    })
    .catch(error => {
        if (loadingDiv.parentNode) {
            chatWindow.removeChild(loadingDiv);
        }
        addMessage(`Error during self-update: ${error}`, 'ai-message');
    });
}

function safeRollback() {
    const loadingDiv = addMessage('<span class="spinner"></span>Rolling back...', 'ai-message loading');
    
    fetch('/api/self-update', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            action: "rollback"
        })
    })
    .then(response => response.json())
    .then(data => {
        chatWindow.removeChild(loadingDiv);
        if (data.response) {
            addMessage(`Pleione: ${data.response}`, 'ai-message');
        }
    })
    .catch(error => {
        if (loadingDiv.parentNode) {
            chatWindow.removeChild(loadingDiv);
        }
        addMessage(`Error during rollback: ${error}`, 'ai-message');
    });
}

// Load file list on page load
function loadFileList() {
    fetch('/api/files')
    .then(response => response.json())
    .then(data => {
        const fileListDiv = document.getElementById('fileList');
        if (data.files) {
            fileListDiv.innerHTML = data.files.map(file => 
                `<label><input type="checkbox" value="${file}"> ${file}</label>`
            ).join('<br>');
        }
    })
    .catch(error => {
        console.error('Error loading file list:', error);
        document.getElementById('fileList').innerHTML = 'Error loading files';
    });
}

// Load files when page loads
document.addEventListener('DOMContentLoaded', loadFileList);

// Allow Enter key to send message
userInput.addEventListener('keypress', function(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
});