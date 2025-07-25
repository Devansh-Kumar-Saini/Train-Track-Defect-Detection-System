function evaluateAudio() {
    document.getElementById("emotion-output").innerText = "Analyzing...";
    setTimeout(() => {
        document.getElementById("emotion-output").innerText = "Happy 😃";
    }, 2000);
}

document.getElementById("audio-upload").addEventListener("change", function() {
    const file = this.files[0]; 
    if (file) {
        document.getElementById("emotion-output").innerText = "File uploaded: " + file.name;
    }
});

function evaluateAudio() {
    const file = document.getElementById("audio-upload").files[0];

    if (!file) {
        alert("Please upload an audio file first.");
        return;
    }

    const formData = new FormData();
    formData.append("audio", file);

    fetch("http://localhost:5000/analyze", {  // Replace with your backend URL
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("emotion-output").innerText = "Detected Emotion: " + data.emotion;
    })
    .catch(error => {
        console.error("Error:", error);
        document.getElementById("emotion-output").innerText = "Error processing file.";
    });
}