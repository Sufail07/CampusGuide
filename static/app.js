document.addEventListener("DOMContentLoaded", function() {
    // Get chatbox elements
    const chatbox = document.getElementById("chatbox");
    const chatboxToggle = document.getElementById("chatbox-toggle");
    const minimizeButton = document.getElementById("minimize-button");
    const maximizeButton = document.getElementById("maximize-button");
    const closeButton = document.getElementById("close-button");
    const chatInput = document.getElementById("chat-input");
    const sendButton = document.getElementById("send-button");
    const speechButton = document.getElementById("speech-button");
    const chatMessages = document.getElementById("chatbox-messages");

    // Initialize chatbox state
    let isChatboxMinimized = false;
    let isChatboxFullscreen = false;

    // Toggle chatbox visibility
    chatboxToggle.addEventListener("click", function() {
        chatbox.classList.add("show");
        chatboxToggle.style.display = "none";
        chatInput.focus();
    });

    // Minimize chatbox
    minimizeButton.addEventListener("click", function() {
        if (isChatboxFullscreen) {
            chatbox.classList.remove("fullscreen");
            isChatboxFullscreen = false;
        } else {
            chatbox.classList.toggle("minimized");
            isChatboxMinimized = !isChatboxMinimized;
        }
    });

    // Maximize chatbox
    if (maximizeButton) {
        maximizeButton.addEventListener("click", function() {
            chatbox.classList.add("fullscreen");
            chatbox.classList.remove("minimized");
            isChatboxFullscreen = true;
            isChatboxMinimized = false;
        });
    }

    // Close chatbox
    closeButton.addEventListener("click", function() {
        chatbox.classList.remove("show", "fullscreen", "minimized");
        chatboxToggle.style.display = "block";
        isChatboxFullscreen = false;
        isChatboxMinimized = false;
    });

    // Function to check if a message contains a photo link
    function isPhotoLink(message) {
        const imageKeywords = ['jpg', 'jpeg', 'png', 'gif'];
        const lowercasedMessage = message.toLowerCase();
        return imageKeywords.some(keyword => lowercasedMessage.includes(keyword));
    }

    // Function to create clickable links
    function createClickableLink(url) {
        return `<a href="${url}" target="_blank">${url}</a>`;
    }

    // Function to start speech-to-text
    function startSpeechToText() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            console.log("Speech recognition is not supported in this browser.");
            addBotMessage("Speech recognition is not supported in your browser.");
            return;
        }

        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        
        // Visual feedback that listening has started
        speechButton.textContent = "Listening...";
        speechButton.classList.add("listening");

        recognition.onresult = function(event) {
            const result = event.results[0][0].transcript;
            chatInput.value = result;
            
            // Reset button
            speechButton.textContent = "Speak";
            speechButton.classList.remove("listening");
            
            // Send the message
            sendMessage(result);
        };

        recognition.onend = function() {
            // Reset button when speech recognition ends
            speechButton.textContent = "Speak";
            speechButton.classList.remove("listening");
        };

        recognition.start();
    }

    // Function to add a user message to the chat
    function addUserMessage(message) {
        const userMessage = document.createElement('div');
        userMessage.className = 'message user-message';
        userMessage.innerHTML = message;
        chatMessages.appendChild(userMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to add a bot message to the chat
    function addBotMessage(message) {
        const botMessage = document.createElement('div');
        botMessage.className = 'message bot-message';

        if (isPhotoLink(message)) {
            const [photoUrl, ...descriptionParts] = message.split('\n');
            const description = descriptionParts.join('\n');
            botMessage.innerHTML = `
                <div class="bot-message-content">
                    <img class="chatbox__image" src="${photoUrl}" alt="Facility Photo">
                    <p>${description}</p>
                </div>
            `;
        } else {
            botMessage.innerHTML = message.replace(/(https?:\/\/[^\s]+)/g, createClickableLink('$1'));
        }
        
        chatMessages.appendChild(botMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Function to send a message to the server
    function sendMessage(message) {
        if (message.trim() === '') return;
        
        // Display user message (unless it's a credential pattern)
        const pattern = /^\d{4}, [a-zA-Z0-9]+$/;
        if (!pattern.test(message)) {
            addUserMessage('You: ' + message);
        }
        
        // Show loading indicator
        const loadingMessage = document.createElement('div');
        loadingMessage.className = 'message bot-message loading';
        loadingMessage.innerHTML = 'Bot is typing<span class="dot-animation">...</span>';
        chatMessages.appendChild(loadingMessage);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Send request to server
        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message: message })
        })
        .then(response => response.json())
        .then(data => {
            // Remove loading indicator
            chatMessages.removeChild(loadingMessage);
            
            // Add bot response
            addBotMessage('Bot: ' + data.answer);
            
            // Handle download URL if present
            if (data.download_url) {
                console.log("Download URL available:", data.download_url);
            }
        })
        .catch(error => {
            // Remove loading indicator
            chatMessages.removeChild(loadingMessage);
            console.error('Error:', error);
            addBotMessage('Bot: Sorry, there was an error processing your request.');
        });
    }

    // Send message on button click
    sendButton.addEventListener('click', function() {
        const message = chatInput.value;
        sendMessage(message);
        chatInput.value = '';
        chatInput.focus();
    });

    // Send message on Enter key press
    chatInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            const message = chatInput.value;
            sendMessage(message);
            chatInput.value = '';
        }
    });

    // Activate speech-to-text on button click
    if (speechButton) {
        speechButton.addEventListener('click', startSpeechToText);
    }

    // Handle smooth scrolling for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetElement = document.querySelector(this.getAttribute('href'));
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Animation for sections when scrolling
    window.addEventListener('scroll', function() {
        const sections = document.querySelectorAll('section');
        sections.forEach((section) => {
            const sectionTop = section.getBoundingClientRect().top;
            if (sectionTop < window.innerHeight - 100) {
                section.style.opacity = '1';
                section.style.transform = 'translateY(0)';
            }
        });
    });

    // Initialize sections with fade-in effect
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = `opacity 0.5s ease, transform 0.5s ease ${index * 0.1}s`;
    });

    // Trigger initial animations
    setTimeout(() => {
        window.dispatchEvent(new Event('scroll'));
    }, 100);
});