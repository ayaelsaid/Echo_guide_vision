/**
 * Submits the selected language and username to the backend.
 *
 * Flow:
 * 1. Reads the user's name and selected language from input fields.
 * 2. Sends a POST request to the `/add_user` endpoint with the data.
 * 3. Handles the server response:
 *    - If successful, logs the confirmation message.
 *    - If failed, displays an error message in the "output" element.
 *
 * Expected Backend Payload:
 * {
 *   "language_code": "<selected language>",
 *   "name": "<username>"
 * }
 *
 * Notes:
 * - Make sure the input fields have IDs: "username" and "language".
 * - The backend should return a JSON response with a "message" field.
 * - Error messages are shown in the element with ID "output".
 */
function submitLanguage() {
  const name = document.getElementById("username").value;
  const language = document.getElementById("language").value;

  fetch('/add_user', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      language_code: language,
      name: name
    })
  })
  .then(response => {
    if (!response.ok) throw new Error('Language selection failed.');
    return response.json();
  })
  .then(data => {
    console.log(data.message);
  })
  .catch(error => {
    document.getElementById("output").innerText =
      `Error: ${error.message}`;
  });
}  
  
  // function submitLanguage() {
  //   const name = document.getElementById("username").value;
  //   const language = document.getElementById("language").value;

  //   fetch('/add_user', {
  //     method: 'POST',
  //     headers: { 'Content-Type': 'application/json' },
  //     body: JSON.stringify({
  //       language_code: language,
  //       name: name
  //     })
  //   })
  //   .then(response => {
  //     if (!response.ok) throw new Error('Language selection failed.');
  //     return response.json();
  //   })
  //   .then(data => {
  //     console.log(data.message);
  //   })
  //   .catch(error => {
  //     document.getElementById("output").innerText =
  //       `Error: ${error.message}`;
  //   });
  // }
