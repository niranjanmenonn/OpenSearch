document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const executeBtn = document.getElementById('executeBtn');

    // Execute command when button is clicked
    executeBtn.addEventListener('click', function() {
        const command = searchInput.value.trim().toLowerCase();
        if (command) {
            executeCommand(command);
        }
    });

    // Execute command when Enter key is pressed
    searchInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            const command = searchInput.value.trim().toLowerCase();
            if (command) {
                executeCommand(command);
            }
        }
    });

    // Parse and execute the command
    function executeCommand(command) {
        // Web search commands
        if (command.includes('go to') && command.includes('search for')) {
            automateWebSearch(command);
        }
        // Brightness commands
        else if (command.includes('brightness')) {
            if (command.includes('increase')) {
                setBrightness('increase');
            } else if (command.includes('decrease')) {
                setBrightness('decrease');
            } else if (command.includes('max') || command.includes('maximum')) {
                setBrightness('max');
            } else if (command.includes('min') || command.includes('minimum')) {
                setBrightness('min');
            } else if (command.match(/set brightness to (\d+)%?/)) {
                const match = command.match(/set brightness to (\d+)%?/);
                const level = parseInt(match[1]);
                if (!isNaN(level) && level >= 0 && level <= 100) {
                    setBrightness('set', level);
                }
            }
        }
        // Volume commands
        else if (command.includes('volume')) {
            if (command.includes('increase')) {
                setVolume('increase');
            } else if (command.includes('decrease')) {
                setVolume('decrease');
            } else if (command.includes('max') || command.includes('maximum')) {
                setVolume('max');
            } else if (command.includes('min') || command.includes('minimum')) {
                setVolume('min');
            } else if (command.match(/set volume to (\d+)%?/)) {
                const match = command.match(/set volume to (\d+)%?/);
                const level = parseInt(match[1]);
                if (!isNaN(level) && level >= 0 && level <= 100) {
                    setVolume('set', level);
                }
            }
        } else {
            showFeedback('Command not recognized. Try "go to [website] and search for [term]" or brightness/volume commands.');
        }
    }

    // Function to automate web searches
    function automateWebSearch(command) {
        // Show a more specific feedback message based on the command
        let site = 'website';
        if (command.includes('youtube')) {
            site = 'YouTube';
        } else if (command.includes('google scholar')) {
            site = 'Google Scholar';
        } else if (command.includes('google')) {
            site = 'Google';
        } else if (command.includes('wikipedia')) {
            site = 'Wikipedia';
        } else if (command.includes('stack overflow')) {
            site = 'Stack Overflow';
        } else if (command.includes('github')) {
            site = 'GitHub';
        } else if (command.includes('research gate')) {
            site = 'ResearchGate';
        } else if (command.includes('quora')) {
            site = 'Quora';
        } else if (command.includes('amazon')) {
            site = 'Amazon';
        } else if (command.includes('reddit')) {
            site = 'Reddit';
        } else if (command.includes('flipkart')) {
            site = 'Flipkart';
        }
        
        showFeedback(`Processing your search request on ${site}...`);
        
        fetch('/automate_search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'query=' + encodeURIComponent(command)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Search response:', data);
            if (data.status === 'success') {
                showFeedback(data.message);
            } else {
                showFeedback('Error: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error automating search:', error);
            showFeedback('Error processing your search request');
        });
    }

    // Function to control brightness
    function setBrightness(action, level = null) {
        let endpoint = '/api/brightness';
        let data = {};
        
        if (action === 'set' && level !== null) {
            data.action = level.toString();
        } else if (action === 'max') {
            data.action = '100';
        } else if (action === 'min') {
            data.action = '10';
        } else {
            data.action = action;
        }
        
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Brightness updated:', data);
            showFeedback(`Brightness ${action === 'set' ? 'set to' : action + 'd to'} ${data.brightness}%`);
        })
        .catch(error => {
            console.error('Error updating brightness:', error);
            showFeedback('Error updating brightness');
        });
    }

    // Function to control volume
    function setVolume(action, level = null) {
        let endpoint = '/api/volume';
        let data = {};
        
        if (action === 'set' && level !== null) {
            data.action = level.toString();
        } else if (action === 'max') {
            data.action = '100';
        } else if (action === 'min') {
            data.action = '0';
        } else {
            data.action = action;
        }
        
        fetch(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Volume updated:', data);
            showFeedback(`Volume ${action === 'set' ? 'set to' : action + 'd to'} ${data.volume}%`);
        })
        .catch(error => {
            console.error('Error updating volume:', error);
            showFeedback('Error updating volume');
        });
    }

    // Function to show feedback to the user
    function showFeedback(message) {
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
        
        // Hide after 3 seconds
        setTimeout(() => {
            feedbackEl.style.display = 'none';
        }, 3000);
    }
});
