let cameraStream = null;
let mediaRecorder = null;
let recordingChunks = [];
let recordingUrl = null;

function setCameraStatus(message) {
    const status = document.getElementById("cameraStatus");
    if (status) status.textContent = message;
}

async function startCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        setCameraStatus("Camera access is unavailable. Open this page over HTTPS in a supported browser.");
        return;
    }

    try {
        cameraStream = await navigator.mediaDevices.getUserMedia({
            video: true,
            audio: false
        });
        document.getElementById("cameraPreview").srcObject = cameraStream;
        document.getElementById("startCameraButton").disabled = true;
        document.getElementById("startRecordingButton").disabled = false;
        setCameraStatus("Camera is on.");
    } catch (error) {
        console.error("Could not access camera:", error);
        if (error.name === "NotAllowedError" || error.name === "PermissionDeniedError") {
            setCameraStatus("Camera permission was denied. Allow camera access in your browser settings, then try again.");
        } else if (error.name === "NotFoundError" || error.name === "DevicesNotFoundError") {
            setCameraStatus("No camera was found on this device. Connect or enable a camera, then try again.");
        } else if (error.name === "NotReadableError" || error.name === "TrackStartError") {
            setCameraStatus("The camera is busy or unavailable. Close other apps using it and try again.");
        } else {
            setCameraStatus(`Could not start camera: ${error.message || error.name}`);
        }
    }
}

function startRecording() {
    if (!cameraStream) {
        setCameraStatus("Start the camera before recording.");
        return;
    }
    if (!window.MediaRecorder) {
        setCameraStatus("This browser does not support video recording.");
        return;
    }

    try {
        const mimeType = ["video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"]
            .find(type => MediaRecorder.isTypeSupported(type));
        mediaRecorder = mimeType
            ? new MediaRecorder(cameraStream, { mimeType })
            : new MediaRecorder(cameraStream);
        recordingChunks = [];
        mediaRecorder.addEventListener("dataavailable", event => {
            if (event.data && event.data.size > 0) recordingChunks.push(event.data);
        });
        mediaRecorder.addEventListener("stop", saveRecording, { once: true });
        mediaRecorder.start();

        document.getElementById("startRecordingButton").disabled = true;
        document.getElementById("stopRecordingButton").disabled = false;
        const link = document.getElementById("downloadRecording");
        link.hidden = true;
        if (recordingUrl) {
            URL.revokeObjectURL(recordingUrl);
            recordingUrl = null;
        }
        setCameraStatus("Recording…");
    } catch (error) {
        console.error("Could not start recording:", error);
        setCameraStatus(`Could not start recording: ${error.message || error.name}`);
    }
}

function stopRecording() {
    if (!mediaRecorder || mediaRecorder.state === "inactive") return;
    mediaRecorder.stop();
    document.getElementById("stopRecordingButton").disabled = true;
    document.getElementById("startRecordingButton").disabled = false;
    setCameraStatus("Recording stopped. Your video is ready to download.");
}

function saveRecording() {
    if (recordingChunks.length === 0) {
        setCameraStatus("No video data was captured. Please try recording again.");
        return;
    }

    const blob = new Blob(recordingChunks, {
        type: mediaRecorder.mimeType || "video/webm"
    });
    recordingUrl = URL.createObjectURL(blob);
    const link = document.getElementById("downloadRecording");
    link.href = recordingUrl;
    link.download = `recording-${new Date().toISOString().replaceAll(":", "-")}.webm`;
    link.textContent = "Download recording";
    link.hidden = false;
}

window.addEventListener("beforeunload", () => {
    if (cameraStream) cameraStream.getTracks().forEach(track => track.stop());
    if (recordingUrl) URL.revokeObjectURL(recordingUrl);
});
