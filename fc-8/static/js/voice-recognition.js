document.addEventListener('DOMContentLoaded', function() {
    // Check if browser supports SpeechRecognition
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    
    if (!SpeechRecognition) {
        console.error("Speech recognition not supported by this browser");
        // Show feedback to user
        showFeedback("Speech recognition not supported by this browser. Try using Chrome.");
        return;
    }
    
    const recognition = new SpeechRecognition();
    const micButton = document.getElementById('micButton');
    const searchInput = document.getElementById('searchInput');
    const executeBtn = document.getElementById('executeBtn');
    
    // Configure speech recognition
    recognition.continuous = false;
    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;
    
    // Add event listeners
    micButton.addEventListener('click', startListening);
    
    let isListening = false;
    
    function startListening() {
        try {
            // If already listening, stop
            if (isListening) {
                recognition.stop();
                resetMicButton();
                return;
            }
            
            // Start listening
            recognition.start();
            micButton.classList.add('listening');
            micButton.innerHTML = '<i class="fas fa-microphone-slash"></i>';
            showFeedback("Listening... Speak your command");
            isListening = true;
        } catch (error) {
            console.error("Speech recognition error:", error);
            showFeedback("Error starting speech recognition. Please try again.");
            resetMicButton();
        }
    }
    
    function resetMicButton() {
        micButton.innerHTML = '<i class="fas fa-microphone"></i>';
        micButton.classList.remove('listening');
        isListening = false;
    }
    
    // Handle speech recognition results
    recognition.onresult = function(event) {
        try {
            const speechResult = event.results[0][0].transcript;
            searchInput.value = speechResult;
            showFeedback(`Recognized: "${speechResult}". Executing command...`);
            
            // Auto-execute the command after a short delay
            setTimeout(() => {
                executeBtn.click();
            }, 1000);
        } catch (error) {
            console.error("Error processing speech result:", error);
            showFeedback("Error processing speech. Please try again.");
        }
    };
    
    // Handle speech recognition errors
    recognition.onerror = function(event) {
        console.error("Speech Recognition Error", event.error);
        
        let errorMessage = "Error occurred in speech recognition. Please try again.";
        
        // Provide more specific error messages
        switch(event.error) {
            case 'no-speech':
                errorMessage = "No speech was detected. Please try again.";
                break;
            case 'aborted':
                errorMessage = "Speech recognition was aborted.";
                break;
            case 'audio-capture':
                errorMessage = "No microphone was found. Ensure it is plugged in and allowed.";
                break;
            case 'network':
                errorMessage = "Network error occurred. Try using the text input instead.";
                break;
            case 'not-allowed':
                errorMessage = "Microphone access was not allowed. Please enable it in your browser settings.";
                break;
            case 'service-not-allowed':
                errorMessage = "Speech recognition service is not allowed. Try using Chrome.";
                break;
        }
        
        showFeedback(errorMessage);
    };
    
    // Handle end of speech recognition
    recognition.onend = function() {
        resetMicButton();
    };
    
    // Reuse the existing showFeedback function if available, otherwise define it
    if (typeof window.showFeedback !== 'function') {
        window.showFeedback = function(message) {
            // Check if feedback element exists
            let feedbackEl = document.querySelector('.command-feedback');
            
            // If not, create it
            if (!feedbackEl) {
                feedbackEl = document.createElement('div');
                feedbackEl.className = 'command-feedback';
                feedbackEl.style.position = 'absolute';
                feedbackEl.style.top = '80px';
                feedbackEl.style.left = '50%';
                feedbackEl.style.transform = 'translateX(-50%)';
                feedbackEl.style.backgroundColor = 'rgba(0, 0, 0, 0.7)';
                feedbackEl.style.color = 'white';
                feedbackEl.style.padding = '10px 20px';
                feedbackEl.style.borderRadius = '5px';
                feedbackEl.style.zIndex = '100';
                document.querySelector('.app-container').appendChild(feedbackEl);
            }
            
            // Update message and show
            feedbackEl.textContent = message;
            feedbackEl.style.display = 'block';
            
            // Hide after 5 seconds (increased from 3)
            setTimeout(() => {
                feedbackEl.style.display = 'none';
            }, 5000);
        };
    }
});
