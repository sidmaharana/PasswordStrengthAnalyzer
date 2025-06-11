// This function updates just the breach count text using the correct ID
function updateBreachCount(count) {
    // Find the element with ID "breachCount"
    const breachCountElement = document.getElementById('breachCount');
    
    if (breachCountElement) {
        // Update the text to show the actual number of breaches
        breachCountElement.textContent = `${count} breaches`;
    }
}

// Your existing analyzePassword function with the fix
function analyzePassword() {
    const passwordInput = document.getElementById('passwordInput');
    const resultsDiv = document.getElementById('results');
    const timeToCrackElement = document.getElementById('timeToCrack');
    const strengthFeaturesElement = document.getElementById('strengthFeatures');
    const suggestedPasswordElement = document.getElementById('suggestedPassword');
    const breachStatusElement = document.getElementById('breachStatus');

    const password = passwordInput.value;

    // Validate input
    if (!password) {
        alert('Please enter a password');
        return;
    }

    // Send request to backend
    fetch('/analyze_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {
        // Format time-to-crack values dynamically
        const timeToCrackHTML = Object.entries(data.time_to_crack || {})
            .map(([method, time]) => `<strong>${method}:</strong> ${time}`)
            .join('<br>');
        timeToCrackElement.innerHTML = `Time to Crack:<br>${timeToCrackHTML}`;

        // Format strength features
        const featuresHTML = Object.entries(data.strength_features || {})
            .map(([key, value]) => `<strong>${key}:</strong> ${value}`)
            .join('<br>');
        strengthFeaturesElement.innerHTML = `Strength Features:<br>${featuresHTML}`;

        // Display suggested password
        suggestedPasswordElement.innerHTML = `Suggested Password: ${data.suggested_password || 'N/A'}`;

        // Display Breach Status with proper formatting
        if (data.breach_status) {
            if (data.breach_status.breached) {
                breachStatusElement.innerHTML = `⚠️ <strong>Password found in ${data.breach_status.breach_count} breaches!</strong> Consider changing it.`;
                breachStatusElement.style.color = 'red';
                
                // Update the breach count text using the correct ID
                updateBreachCount(data.breach_status.breach_count);
                
                // Update the breach strength bar
                updateBreachStrengthBar(data.breach_status.breach_count);
            } else {
                breachStatusElement.innerHTML = `✅ <strong>Good news!</strong> Your password was not found in any breaches.`;
                breachStatusElement.style.color = 'green';
                
                // Set breach count to 0
                updateBreachCount(0);
                
                // Update strength bar
                updateBreachStrengthBar(0);
            }
            breachStatusElement.classList.remove('hidden'); // Show breach status
        } else {
            breachStatusElement.classList.add('hidden'); // Hide if not available
        }

        // Show results
        resultsDiv.classList.remove('hidden');
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to analyze password');
    });
}

// Also update your existing updateBreachStrengthBar function
function updateBreachStrengthBar(breachCount) {
    // Get the breach strength bar element
    const strengthBar = document.getElementById('breachStrengthBar');
    
    // Calculate the percentage width and color based on breach count
    let width = 0;
    let color = 'green';
    
    // Determine the category based on breach count
    if (breachCount === 0) {
        // Safe (0)
        width = 0;
        color = 'green';
    } else if (breachCount >= 1 && breachCount <= 10) {
        // Low (1-10)
        width = 20;
        color = '#4CAF50'; // lighter green
    } else if (breachCount >= 11 && breachCount <= 100) {
        // Risk (11-100)
        width = 40;
        color = 'orange';
    } else if (breachCount >= 101 && breachCount <= 1000) {
        // High Risk (101-1000)
        width = 70;
        color = '#ff9800'; // orange-red
    } else if (breachCount > 1000) {
        // Critical (1000+)
        width = 100;
        color = 'red';
    }
    
    // Update the bar
    strengthBar.style.width = `${width}%`;
    strengthBar.style.backgroundColor = color;
    
    // We don't need to update the breach count here anymore
    // as we have a dedicated function for that
}