    const startButton = document.getElementById('startButton');
    const responseImage = document.getElementById('responseImage');
    const statusMessageDiv = document.getElementById('statusMessage');
    const aiResponseTextDiv = document.getElementById('aiResponseText');

    /**
     * Updates the status message displayed on the page.
     * @param {string} message - The message to display.
     * @param {boolean} isError - True if it's an error message, false otherwise.
     */
    function updateStatus(message, isError = false) {
      statusMessageDiv.textContent = message;
      statusMessageDiv.style.color = isError ? '#FF6347' : '#FFFFF0'; 
    }

    startButton.addEventListener('click', async () => {
      startButton.disabled = true;
      updateStatus('Starting AI interaction... Please listen to your computer for instructions.');
      responseImage.style.display = 'none';
      responseImage.src = '';
      aiResponseTextDiv.textContent = '';

      try {
        const response = await fetch('http://127.0.0.1:5000/start_interaction', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
        });

        const data = await response.json();

        if (response.ok) {
          updateStatus('Interaction complete. Showing last details.');
          console.log('Server response:', data);

        if (data.last_image_path) {
            const normalizedPath = data.last_image_path.replace(/\\/g, '/');

            const filename = normalizedPath.split('/').pop();

            responseImage.src = `http://127.0.0.1:5000/captured_images/${filename}`;
            responseImage.style.display = 'block';
          }          
           else {
            responseImage.style.display = 'none';
          }

          if (data.last_ai_response) {
            aiResponseTextDiv.textContent = `AI Response: "${data.last_ai_response}"`;
          }

        } else {
          updateStatus(`Error: ${data.error || 'Unknown error from server'}`, true);
          console.error('Server error:', data);
          responseImage.style.display = 'none';
          aiResponseTextDiv.textContent = '';
        }
      } catch (error) {
        updateStatus(`Network or client-side error: ${error.message}. Make sure the Flask server is running!`, true);
        console.error('Fetch error:', error);
        responseImage.style.display = 'none';
        aiResponseTextDiv.textContent = '';
      } finally {
        startButton.disabled = false;
      }
    });