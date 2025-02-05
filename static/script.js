async function uploadAudio() {
    window.alert("Start Transcription")
    const fileInput = document.getElementById('audioFile');
    const file = fileInput.files[0];

    if (!file) {
        alert('Please select an audio file.');
        return;
    }

    const formData = new FormData();
    formData.append('audio', file);

    try {
        const response = await fetch('http://127.0.0.1:5500/transcribe', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const data = await response.json();
        document.getElementById('output').textContent = data.transcription;
    } catch (error) {
        console.error('There was a problem with the fetch operation:', error);
    }
}

// Copy text
function copyToClipboard() {
    var copyText = document.getElementById("output");

    navigator.clipboard.writeText(copyText.innerText)
        .then(() => {
            alert("Copied to clipboard!");
        })
        .catch(err => {
            console.error("Failed to copy:", err);
        });
}

// Clear text
function clearOutput() {
    const element = document.getElementById("output");
    if (element) {
        element.textContent = "";
    }
}
