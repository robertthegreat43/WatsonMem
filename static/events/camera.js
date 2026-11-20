async function startRecording() {
    const status = document.getElementById("cameraStatus");
    try {
        const response = await fetch("/api/start_recording/", { method: "POST" });
        const data = await response.json();
        if (!response.ok) {
            throw new Error(data.detail || "The server could not start recording.");
        }
        status.textContent = `Recording started: ${data.file}`;
        document.getElementById("startRecordingButton").disabled = true;
        document.getElementById("stopRecordingButton").disabled = false;
    } catch (error) {
        console.error("Start recording failed:", error);
        status.textContent = error.message;
    }
}

async function stopRecording() {
    const status = document.getElementById("cameraStatus");
    try {
        const response = await fetch("/api/stop_recording/", { method: "POST" });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Could not stop recording.");
        status.textContent = data.status || "Recording stopped.";
        document.getElementById("startRecordingButton").disabled = false;
        document.getElementById("stopRecordingButton").disabled = true;
    } catch (error) {
        console.error("Stop recording failed:", error);
        status.textContent = error.message;
    }
}

async function listVideos() {
    const container = document.getElementById("videoList");
    container.replaceChildren();
    try {
        const response = await fetch("/api/videos/");
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail || "Could not list recordings.");

        if (!data.videos.length) {
            container.textContent = "No recordings found.";
            return;
        }

        for (const filename of data.videos) {
            const link = document.createElement("a");
            link.href = `/api/download/${encodeURIComponent(filename)}/`;
            link.textContent = `Download ${filename}`;
            link.style.display = "block";
            container.appendChild(link);
        }
    } catch (error) {
        console.error("List recordings failed:", error);
        container.textContent = error.message;
    }
}
