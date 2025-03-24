/**
 * Legal Advisor AI - Production Version
 * Professional JavaScript for enterprise application
 */

// Initialize all animations and interactions when the document is loaded
document.addEventListener('DOMContentLoaded', function() {
    console.log('Initializing Legal Advisor AI - Production Version');
    initializeAnimations();
    
    // Check if we're here from a page reload for chat reset
    handleChatReset();
    
    // Set up Streamlit app observer to handle re-renders
    observeStreamlitApp();
    
    // Make sure new chat button is initialized when rendering finishes
    setTimeout(initializeNewChatButton, 500);
    
    // Add event listener for a retry mechanism to ensure the button is initialized
    document.addEventListener('streamlit:render', function(e) {
        console.log('Streamlit render event detected');
        setTimeout(initializeNewChatButton, 200);
    });
});

/**
 * Main initialization function for all animations and interactions
 */
function initializeAnimations() {
    // Apply theming
    handleThemePreference();
    
    // Initialize UI enhancements
    enhanceChatContainer();
    enhanceChatMessages();
    highlightLegalTerms();
    enhanceUIElements();
    improveAccessibility();
    
    // Initialize file uploader enhancements
    enhanceFileUploader();
    
    // Add typing effect to new messages
    addTypingEffect();
    
    // Animate scales and legal imagery
    animateScalesLogo();
    
    // Initialize new chat button if exists
    initializeNewChatButton();
    
    // Initialize chat history if exists
    initializeChatHistory();
    
    // Add keyboard shortcuts
    addKeyboardShortcuts();
    
    // Initialize the theme toggle in the top right
    initializeThemeToggle();
}

/**
 * Handle theme preference and add theme toggle functionality
 */
function handleThemePreference() {
    // Check for saved preference
    const savedTheme = localStorage.getItem('theme');
    const prefersDarkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Apply saved theme or default based on system preference
    if (savedTheme === 'light') {
        document.body.classList.add('light-mode-forced');
        document.body.classList.remove('dark-mode-forced');
    } else if (savedTheme === 'dark') {
        document.body.classList.add('dark-mode-forced');
        document.body.classList.remove('light-mode-forced');
    } else {
        // No saved preference, respect system preference
        if (prefersDarkMode) {
            document.body.classList.add('dark-mode-forced');
            document.body.classList.remove('light-mode-forced');
        } else {
            document.body.classList.add('light-mode-forced');
            document.body.classList.remove('dark-mode-forced');
        }
    }
    
    // Create or update the theme toggle if it doesn't exist
    if (!document.getElementById('darkModeToggle')) {
        const toggle = document.createElement('button');
        toggle.id = 'darkModeToggle';
        toggle.setAttribute('aria-label', 'Toggle dark mode');
        toggle.innerHTML = document.body.classList.contains('light-mode-forced') 
            ? '<i class="fas fa-moon"></i> Dark Mode' 
            : '<i class="fas fa-sun"></i> Light Mode';
            
        toggle.addEventListener('click', toggleDarkMode);
        document.body.appendChild(toggle);
    }
    
    // Initialize the corner theme toggle button if it exists
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle && !themeToggle.dataset.initialized) {
        themeToggle.addEventListener('click', toggleDarkMode);
        themeToggle.innerHTML = document.body.classList.contains('light-mode-forced') 
            ? '<i class="fas fa-moon"></i>' 
            : '<i class="fas fa-sun"></i>';
        themeToggle.title = document.body.classList.contains('light-mode-forced') 
            ? 'Switch to dark mode' 
            : 'Switch to light mode';
        themeToggle.dataset.initialized = 'true';
    }
    
    // Update all theme toggle buttons to have consistent state
    updateThemeToggleButtons();
    
    // Add system theme preference listener
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        // Only update if no saved preference exists
        if (!localStorage.getItem('theme')) {
            if (e.matches) {
                document.body.classList.add('dark-mode-forced');
                document.body.classList.remove('light-mode-forced');
            } else {
                document.body.classList.add('light-mode-forced');
                document.body.classList.remove('dark-mode-forced');
            }
            // Update toggle buttons
            updateThemeToggleButtons();
        }
    });
}

/**
 * Toggle between dark and light mode
 */
function toggleDarkMode() {
    const isDarkMode = document.body.classList.contains('dark-mode-forced');
    
    // Update theme classes
    if (isDarkMode) {
        document.body.classList.remove('dark-mode-forced');
        document.body.classList.add('light-mode-forced');
        localStorage.setItem('theme', 'light');
    } else {
        document.body.classList.add('dark-mode-forced');
        document.body.classList.remove('light-mode-forced');
        localStorage.setItem('theme', 'dark');
    }
    
    // Update all theme toggle buttons
    updateThemeToggleButtons();
}

/**
 * Update all theme toggle buttons to reflect current theme
 */
function updateThemeToggleButtons() {
    const isDarkMode = document.body.classList.contains('dark-mode-forced');
    const isLightMode = document.body.classList.contains('light-mode-forced');
    
    // Update the main darkModeToggle if it exists
    const darkModeToggle = document.getElementById('darkModeToggle');
    if (darkModeToggle) {
        darkModeToggle.innerHTML = isDarkMode ? 
            '<i class="fas fa-sun"></i> Light Mode' : 
            '<i class="fas fa-moon"></i> Dark Mode';
    }
    
    // Update the themeToggle in the corner
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.innerHTML = isDarkMode ? 
            '<i class="fas fa-sun"></i>' : 
            '<i class="fas fa-moon"></i>';
        themeToggle.title = isDarkMode ? 'Switch to light mode' : 'Switch to dark mode';
    }
}

/**
 * Enhance the chat container with auto-scrolling and UI improvements
 */
function enhanceChatContainer() {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return;
    
    // Auto-scroll to bottom on new messages
    chatContainer.scrollTop = chatContainer.scrollHeight;
    
    // Check if scroll indicator already exists
    if (!document.querySelector('.scroll-indicator')) {
        // Add scroll indicator when not at bottom
        const scrollIndicator = document.createElement('div');
        scrollIndicator.className = 'scroll-indicator';
        scrollIndicator.innerHTML = '<i class="fas fa-chevron-down"></i>';
        scrollIndicator.style.opacity = '0'; // Start hidden
        document.body.appendChild(scrollIndicator);
        
        // Scroll to bottom when indicator is clicked
        scrollIndicator.addEventListener('click', function() {
            chatContainer.scrollTo({
                top: chatContainer.scrollHeight,
                behavior: 'smooth'
            });
        });
    }
    
    // Get the scroll indicator reference
    const scrollIndicator = document.querySelector('.scroll-indicator');
    
    // Show/hide scroll indicator based on scroll position
    chatContainer.addEventListener('scroll', function() {
        const isScrolledUp = chatContainer.scrollHeight - chatContainer.scrollTop > chatContainer.clientHeight + 100;
        scrollIndicator.style.opacity = isScrolledUp ? '1' : '0';
        scrollIndicator.style.pointerEvents = isScrolledUp ? 'auto' : 'none';
    });
}

/**
 * Enhanced professional typing effect for chat messages
 */
function addTypingEffect() {
    const chatContainer = document.querySelector('.chat-container');
    if (!chatContainer) return;
    
    // Find the newest bot message that hasn't been animated yet
    const botMessages = document.querySelectorAll('.bot-message[data-new-message="true"]');
    if (botMessages.length === 0) return;
    
    const latestMessage = botMessages[botMessages.length - 1];
    latestMessage.removeAttribute('data-new-message');
    
    const originalContent = latestMessage.innerHTML;
    const cleanedContent = originalContent.trim();
    
    // Only apply effect to non-empty messages
    if (!cleanedContent) return;
    
    // Keep original content for later reference
    latestMessage.dataset.originalContent = originalContent;
    
    // Clear the message content initially
    latestMessage.innerHTML = '';
    
    // Create a typing container
    const typingContainer = document.createElement('div');
    typingContainer.className = 'typing-container';
    latestMessage.appendChild(typingContainer);
    
    // Parse HTML to preserve formatting
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = cleanedContent;
    
    // Function to type out the content with HTML preservation
    function typeContent(element, parentElement) {
        // Process each child node
        Array.from(element.childNodes).forEach(node => {
            if (node.nodeType === Node.TEXT_NODE) {
                // Text node - type it out character by character
                typeTextWithVariableSpeed(node.textContent, parentElement);
            } else if (node.nodeType === Node.ELEMENT_NODE) {
                // Element node - create it and recursively process its children
                const newElement = document.createElement(node.tagName);
                
                // Copy attributes
                Array.from(node.attributes).forEach(attr => {
                    newElement.setAttribute(attr.name, attr.value);
                });
                
                parentElement.appendChild(newElement);
                
                // Process children of this element
                typeContent(node, newElement);
            }
        });
    }
    
    // Type text with variable speed based on punctuation
    function typeTextWithVariableSpeed(text, parentElement) {
        let index = 0;
        const characters = text.split('');
        const blinker = document.createElement('span');
        blinker.className = 'typing-blinker';
        parentElement.appendChild(blinker);
        
        function typeCharacter() {
            if (index < characters.length) {
                const char = characters[index];
                const textNode = document.createTextNode(char);
                parentElement.insertBefore(textNode, blinker);
                
                index++;
                
                // Variable speed based on punctuation
                let delay = 10 + Math.random() * 15; // Base speed with slight randomization
                
                // Slow down for punctuation
                if ('.!?'.includes(char)) {
                    delay = 250 + Math.random() * 150; // Longer pause after sentence endings
                } else if (',;:)('.includes(char)) {
                    delay = 100 + Math.random() * 50; // Medium pause for other punctuation
                }
                
                setTimeout(typeCharacter, delay);
                
                // Scroll to keep the typing in view
                const chatContainer = document.querySelector('.chat-container');
                if (chatContainer) {
                    chatContainer.scrollTop = chatContainer.scrollHeight;
                }
            } else {
                // Remove blinker when done typing
                blinker.remove();
            }
        }
        
        // Start typing
        setTimeout(typeCharacter, 100);
    }
    
    // Start the typing effect
    typeContent(tempDiv, typingContainer);
    
    // Scroll to bottom to ensure the typing is visible
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Enhanced chat messages with animations and interaction effects
 */
function enhanceChatMessages() {
    const chatMessages = document.querySelectorAll('.bot-message, .user-message');
    
    chatMessages.forEach((message, index) => {
        // Skip messages that already have been enhanced
        if (message.classList.contains('enhanced')) return;
        
        // Add enhanced class to prevent duplicate processing
        message.classList.add('enhanced');
        
        // Add fade-in and translate effect with staggered delay
        message.style.opacity = '0';
        message.style.transform = 'translateY(10px)';
        
        setTimeout(() => {
            message.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateY(0)';
        }, 50 * index);
        
        // Add subtle hover effect
        message.addEventListener('mouseenter', () => {
            const isDarkMode = document.body.classList.contains('dark-mode-forced');
            const hoverColor = isDarkMode ? 'rgba(255, 255, 255, 0.03)' : 'rgba(0, 0, 0, 0.01)';
            message.style.backgroundColor = hoverColor;
        });
        
        message.addEventListener('mouseleave', () => {
            const userMsg = message.classList.contains('user-message');
            const botMsg = message.classList.contains('bot-message');
            const userBg = userMsg ? 'var(--user-msg-bg)' : '';
            const botBg = botMsg ? 'var(--bot-msg-bg)' : '';
            message.style.backgroundColor = userBg || botBg;
        });
    });
}

/**
 * Create professional animations for scales logo
 */
function animateScalesLogo() {
    const scalesIcons = document.querySelectorAll('.scales-icon, .scales-img');
    
    scalesIcons.forEach(icon => {
        icon.style.animation = 'scales 5s ease-in-out infinite';
        
        // Add subtle hover effect
        icon.addEventListener('mouseenter', () => {
            icon.style.animation = 'none';
            icon.style.transform = 'scale(1.1)';
            icon.style.transition = 'transform 0.3s ease';
        });
        
        icon.addEventListener('mouseleave', () => {
            icon.style.transform = 'scale(1)';
            icon.style.animation = 'scales 5s ease-in-out infinite';
        });
    });
}

/**
 * Enhance the file uploader with drag-drop and visual feedback
 */
function enhanceFileUploader() {
    const fileUploader = document.querySelector('[data-testid="stFileUploader"]');
    if (!fileUploader) return;
    
    // Add visual cues for drag-drop
    fileUploader.addEventListener('dragover', (e) => {
        e.preventDefault();
        fileUploader.style.borderColor = 'var(--accent-color)';
        fileUploader.style.backgroundColor = 'rgba(var(--accent-light-rgb), 0.1)';
        fileUploader.style.boxShadow = '0 0 15px rgba(var(--accent-light-rgb), 0.3)';
    });
    
    fileUploader.addEventListener('dragleave', (e) => {
        e.preventDefault();
        fileUploader.style.borderColor = 'var(--border-color)';
        fileUploader.style.backgroundColor = 'var(--container-bg)';
        fileUploader.style.boxShadow = 'none';
    });
    
    fileUploader.addEventListener('drop', () => {
        setTimeout(() => {
            fileUploader.style.borderColor = 'var(--border-color)';
            fileUploader.style.backgroundColor = 'var(--container-bg)';
            fileUploader.style.boxShadow = 'none';
        }, 300);
    });
}

/**
 * Highlight legal terms with professional tooltips
 */
function highlightLegalTerms() {
    // Common legal terms
    const legalTerms = [
        'plaintiff', 'defendant', 'appellant', 'respondent', 'petitioner', 
        'jurisdiction', 'statute', 'tort', 'liability', 'injunction',
        'damages', 'contract', 'breach', 'remedy', 'precedent',
        'discovery', 'evidence', 'testimony', 'deposition', 'affidavit',
        'subpoena', 'litigation', 'settlement', 'judgment', 'verdict',
        'appeal', 'motion', 'habeas corpus', 'pro bono', 'pro se'
    ];
    
    const botMessages = document.querySelectorAll('.bot-message');
    
    botMessages.forEach(message => {
        // Skip messages already processed
        if (message.dataset.termsHighlighted === 'true') return;
        
        let html = message.innerHTML;
        
        // Highlight each legal term with a tooltip
        legalTerms.forEach(term => {
            const regex = new RegExp(`\\b${term}\\b`, 'gi');
            html = html.replace(regex, `<span class="legal-term" title="${term}">$&</span>`);
        });
        
        message.innerHTML = html;
        message.dataset.termsHighlighted = 'true';
    });
}

/**
 * Enhance UI elements with animations and interactions
 */
function enhanceUIElements() {
    // Add hover effects to buttons
    document.querySelectorAll('button').forEach(button => {
        if (button.dataset.enhanced === 'true') return;
        
        button.addEventListener('mouseenter', () => {
            button.style.transform = 'translateY(-1px)';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.transform = 'translateY(0)';
        });
        
        button.dataset.enhanced = 'true';
    });
    
    // Add ripple effect to buttons
    document.querySelectorAll('.sidebar [data-testid="stButton"] button').forEach(button => {
        if (button.dataset.rippleEnhanced === 'true') return;
        
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            ripple.classList.add('ripple');
            this.appendChild(ripple);
            
            const x = e.clientX - this.getBoundingClientRect().left;
            const y = e.clientY - this.getBoundingClientRect().top;
            
            ripple.style.cssText = `
                position: absolute;
                background: rgba(255, 255, 255, 0.3);
                border-radius: 50%;
                pointer-events: none;
                width: 100px;
                height: 100px;
                top: ${y - 50}px;
                left: ${x - 50}px;
                transform: scale(0);
                animation: ripple 0.6s linear;
            `;
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
        
        button.dataset.rippleEnhanced = 'true';
    });
}

/**
 * Improve accessibility
 */
function improveAccessibility() {
    // Enhance focus states
    document.querySelectorAll('a, button, input, [tabindex="0"]').forEach(element => {
        if (element.dataset.a11yEnhanced === 'true') return;
        
        element.addEventListener('focus', () => {
            element.style.outline = '2px solid var(--accent-color)';
            element.style.outlineOffset = '2px';
        });
        
        element.addEventListener('blur', () => {
            element.style.outline = '';
        });
        
        element.dataset.a11yEnhanced = 'true';
    });
    
    // Make tooltips accessible via keyboard
    document.querySelectorAll('.tooltip').forEach(tooltip => {
        if (tooltip.dataset.a11yEnhanced === 'true') return;
        
        tooltip.setAttribute('tabindex', '0');
        tooltip.setAttribute('role', 'button');
        tooltip.setAttribute('aria-expanded', 'false');
        
        tooltip.addEventListener('focus', () => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'visible';
                tooltipText.style.opacity = '1';
                tooltip.setAttribute('aria-expanded', 'true');
            }
        });
        
        tooltip.addEventListener('blur', () => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'hidden';
                tooltipText.style.opacity = '0';
                tooltip.setAttribute('aria-expanded', 'false');
            }
        });
        
        tooltip.dataset.a11yEnhanced = 'true';
    });
}

/**
 * Initialize the New Chat button functionality
 */
function initializeNewChatButton() {
    const newChatButton = document.querySelector('.new-chat-button');
    if (!newChatButton) {
        console.log("New Chat button not found, will retry later");
        setTimeout(initializeNewChatButton, 500); // Retry after 500ms
        return;
    }
    
    if (newChatButton.dataset.initialized === 'true') {
        console.log("New Chat button already initialized");
        return;
    }
    
    console.log("Initializing New Chat button");
    
    // Initialize button click handler
    newChatButton.addEventListener('click', handleNewChatClick);
    
    // Initialize container interactions
    const newChatContainer = document.querySelector('.new-chat-container');
    const arrowIcon = newChatContainer ? newChatContainer.querySelector('.arrow-icon') : null;
    
    if (newChatContainer && arrowIcon) {
        // These event listeners are only for fallback - the CSS handles most of the animation
        newChatContainer.addEventListener('mouseenter', () => {
            arrowIcon.style.transform = 'translateX(3px)';
            arrowIcon.style.color = 'var(--accent-color)';
            arrowIcon.style.opacity = '1';
        });
        
        newChatContainer.addEventListener('mouseleave', () => {
            arrowIcon.style.transform = 'translateX(0)';
            arrowIcon.style.color = '';
            arrowIcon.style.opacity = '0.8';
        });
    }
    
    // Add hover animation effect for the plus icon
    newChatButton.addEventListener('mouseenter', () => {
        const plusIcon = newChatButton.querySelector('i');
        if (plusIcon) {
            plusIcon.style.transform = 'rotate(90deg)';
            plusIcon.style.transition = 'transform 0.3s ease';
        }
    });
    
    newChatButton.addEventListener('mouseleave', () => {
        const plusIcon = newChatButton.querySelector('i');
        if (plusIcon) {
            plusIcon.style.transform = 'rotate(0deg)';
        }
    });
    
    // Mark as initialized
    newChatButton.dataset.initialized = 'true';
    console.log("New Chat button initialization complete");
}

/**
 * Handle New Chat button click
 */
function handleNewChatClick() {
    console.log("New Chat button clicked");
    
    // First approach: Try to find the reset button in the sidebar
    const resetButton = document.querySelector('[data-testid="baseButton-secondary"][key="reset_chat"]');
    
    if (resetButton) {
        console.log("Reset button found, clicking it");
        
        // Save current chat before resetting if it has content
        saveCurrentChat();
        
        // Click the button to trigger Streamlit's reset functionality
        resetButton.click();
    } else {
        console.log("Reset button not found, using alternative reset method");
        
        // Second approach: Try interacting with Streamlit's session state via a form submission
        // Create a hidden form to trigger Streamlit reset
        const resetForm = document.createElement('form');
        resetForm.method = 'POST';
        resetForm.style.display = 'none';
        
        // Add input to indicate reset action
        const resetInput = document.createElement('input');
        resetInput.type = 'hidden';
        resetInput.name = 'reset_chat';
        resetInput.value = 'true';
        resetForm.appendChild(resetInput);
        
        // Add to document, submit, then remove
        document.body.appendChild(resetForm);
        
        try {
            // Save current chat before reset
            saveCurrentChat();
            resetForm.submit();
        } catch (e) {
            console.error("Error submitting form:", e);
            
            // Third approach: Reload the page with a special parameter
            try {
                window.location.href = window.location.pathname + '?reset=true&t=' + Date.now();
            } catch (e2) {
                console.error("Error during page navigation:", e2);
                
                // Final fallback: Just reload the page
                window.location.reload();
            }
        }
        
        // Clean up form
        document.body.removeChild(resetForm);
    }
}

/**
 * Helper function to save the current chat before resetting
 */
function saveCurrentChat() {
    // Only save if there are actual chat messages
    const chatMessages = document.querySelectorAll('.user-message, .bot-message');
    if (chatMessages.length <= 1) return; // Don't save empty chats
    
    try {
        // Generate a simple title from first user message or use generic title
        let chatTitle = "New Chat";
        const firstUserMessage = document.querySelector('.user-message');
        if (firstUserMessage) {
            const text = firstUserMessage.textContent.trim();
            chatTitle = text.substring(0, 30) + (text.length > 30 ? '...' : '');
        }
        
        // Create chat history entry
        const chatData = {
            id: 'chat_' + Date.now(),
            title: chatTitle,
            time: new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'}),
            messages: Array.from(chatMessages).map(msg => ({
                role: msg.classList.contains('user-message') ? 'user' : 'assistant',
                content: msg.innerHTML
            }))
        };
        
        // Get existing history
        let chatHistory = JSON.parse(localStorage.getItem('chatHistory') || '[]');
        
        // Add new chat to history (limit to 10 recent chats)
        chatHistory.unshift(chatData);
        if (chatHistory.length > 10) {
            chatHistory = chatHistory.slice(0, 10);
        }
        
        // Save back to localStorage
        localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
        console.log("Chat saved to history");
    } catch (e) {
        console.error("Error saving chat history:", e);
    }
}

/**
 * Initialize chat history functionality
 */
function initializeChatHistory() {
    const chatHistoryContainer = document.querySelector('.chat-history-container');
    if (!chatHistoryContainer || chatHistoryContainer.dataset.initialized === 'true') return;
    
    // Handle click events on chat history items
    chatHistoryContainer.addEventListener('click', (e) => {
        const historyItem = e.target.closest('.chat-history-item');
        if (historyItem) {
            // Set all items as inactive
            document.querySelectorAll('.chat-history-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Set clicked item as active
            historyItem.classList.add('active');
            
            // Load this chat (implementation depends on backend)
            console.log('Loading chat:', historyItem.dataset.chatId);
        }
        
        // Handle delete button
        const deleteButton = e.target.closest('.chat-history-delete');
        if (deleteButton) {
            e.stopPropagation();
            const historyItem = deleteButton.closest('.chat-history-item');
            if (confirm('Delete this chat?')) {
                // Delete this chat (implementation depends on backend)
                console.log('Deleting chat:', historyItem.dataset.chatId);
                historyItem.remove();
            }
        }
    });
    
    chatHistoryContainer.dataset.initialized = 'true';
}

/**
 * Add keyboard shortcuts for enhanced user experience
 */
function addKeyboardShortcuts() {
    document.addEventListener('keydown', (e) => {
        // Ctrl+/ to focus chat input
        if (e.ctrlKey && e.key === '/') {
            e.preventDefault();
            const chatInput = document.querySelector('[data-testid="stChatInput"] input');
            if (chatInput) chatInput.focus();
        }
        
        // Esc to blur focus
        if (e.key === 'Escape') {
            document.activeElement.blur();
        }
        
        // Ctrl+N for new chat
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            const newChatButton = document.querySelector('.new-chat-button');
            if (newChatButton) newChatButton.click();
        }
        
        // Ctrl+D to toggle dark mode
        if (e.ctrlKey && e.key === 'd') {
            e.preventDefault();
            const darkModeToggle = document.getElementById('darkModeToggle');
            if (darkModeToggle) darkModeToggle.click();
        }
    });
}

/**
 * Handle chat reset after page reload
 */
function handleChatReset() {
    // Check if we need to reset the chat
    if (sessionStorage.getItem('resetChat') === 'true') {
        console.log('Handling chat reset after page reload');
        
        // Clear the reset flag
        sessionStorage.removeItem('resetChat');
        
        // Find the chat input field and clear it
        const chatInput = document.querySelector('[data-testid="stChatInput"] input');
        if (chatInput) {
            chatInput.value = '';
        }
        
        // Display welcome message if it exists
        const welcomeBanner = document.querySelector('.welcome-banner-minimal');
        if (welcomeBanner) {
            welcomeBanner.style.display = 'block';
        }
    }
}

/**
 * Set up observer to detect Streamlit re-renders
 */
function observeStreamlitApp() {
    // Create observer to detect when Streamlit adds or changes elements
    const observer = new MutationObserver((mutations) => {
        // Check if new elements were added
        const newNodesAdded = mutations.some(mutation => 
            mutation.type === 'childList' && mutation.addedNodes.length > 0);
        
        if (newNodesAdded) {
            // Re-initialize buttons and interactions
            initializeAnimations();
            
            // Specifically ensure the New Chat button is working
            initializeNewChatButton();
        }
    });
    
    // Start observing the document body for DOM changes
    observer.observe(document.body, {
        childList: true,
        subtree: true
    });
    
    console.log('Streamlit app observer initialized');
}

/**
 * Initialize or reinitialize the theme toggle button
 */
function initializeThemeToggle() {
    const themeToggle = document.getElementById('themeToggle');
    if (!themeToggle || themeToggle.dataset.initialized === 'true') return;
    
    // Add click event listener to toggle theme
    themeToggle.addEventListener('click', function() {
        toggleDarkMode();
    });
    
    // Update icon based on current theme
    const isDarkMode = document.body.classList.contains('dark-mode-forced') || 
                       (!document.body.classList.contains('light-mode-forced') && 
                        window.matchMedia('(prefers-color-scheme: dark)').matches);
    
    themeToggle.innerHTML = isDarkMode ? 
        '<i class="fas fa-sun"></i>' : 
        '<i class="fas fa-moon"></i>';
    
    themeToggle.title = isDarkMode ? 'Switch to light mode' : 'Switch to dark mode';
    themeToggle.dataset.initialized = 'true';
}

/**
 * Ensure proper alignment of New Chat button and arrow
 * This runs after page is fully loaded
 */
window.addEventListener('load', function() {
    setTimeout(function() {
        const container = document.querySelector('.new-chat-container');
        const arrow = container ? container.querySelector('.arrow-icon') : null;
        const button = container ? container.querySelector('.new-chat-button') : null;
        
        if (container && arrow && button) {
            // Ensure the container has proper flex properties
            container.style.display = 'flex';
            container.style.alignItems = 'center';
            
            // Force the arrow to be centered
            arrow.style.display = 'flex';
            arrow.style.alignItems = 'center';
            arrow.style.justifyContent = 'center';
            
            // Make sure button text is aligned
            const buttonSpan = button.querySelector('span');
            if (buttonSpan) {
                buttonSpan.style.display = 'inline-block';
                buttonSpan.style.verticalAlign = 'middle';
            }
            
            console.log('New Chat button alignment enforced');
        }
    }, 500); // Wait for 500ms after page load
});
