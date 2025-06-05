class FacialRecognition {
    constructor(containerId, options = {}) {
        this.container = document.getElementById(containerId);
        if (!this.container) {
            throw new Error(`Container with id ${containerId} not found`);
        }

        // Opciones por defecto
        this.options = {
            onVideoRecorded: null,  // Callback cuando se complete la grabación
            onError: null,          // Callback para manejar errores
            autoStart: false,       // Si debe iniciar la cámara automáticamente
            ...options
        };

        // Crear elementos UI
        this.createElements();

        // Variables de grabación
        this.mediaRecorder = null;
        this.recordedChunks = [];
        this.startTime = null;
        this.isRecording = false;
        this.recordingInterval = null;

        // Bind de métodos
        this.startRecording = this.startRecording.bind(this);
        this.stopRecording = this.stopRecording.bind(this);
        this.updateRecordingTime = this.updateRecordingTime.bind(this);

        // Event listeners
        this.addEventListeners();

        // Iniciar cámara si autoStart está habilitado
        if (this.options.autoStart) {
            this.initCamera();
        }
    }

    createElements() {
        this.container.innerHTML = `
            <div class="facial-recognition">
                <video id="videoElement" autoplay playsinline></video>
                <div class="controls">
                    <button class="btn btn-primary" id="startBtn">Grabar</button>
                    <button class="btn btn-danger" id="stopBtn" style="display: none;">Detener</button>
                    <div class="recording-indicator" style="display: none;">
                        <span class="indicator"></span>
                        <span class="time">0s</span>
                    </div>
                </div>
            </div>
        `;

        // Guardar referencias a elementos
        this.videoElement = this.container.querySelector('#videoElement');
        this.startBtn = this.container.querySelector('#startBtn');
        this.stopBtn = this.container.querySelector('#stopBtn');
        this.recordingIndicator = this.container.querySelector('.recording-indicator');
        this.recordingTime = this.container.querySelector('.time');
    }

    addEventListeners() {
        this.startBtn.addEventListener('click', this.startRecording);
        this.stopBtn.addEventListener('click', this.stopRecording);
    }

    async initCamera() {
        try {
            const stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1280 },
                    height: { ideal: 720 }
                }
            });
            this.videoElement.srcObject = stream;
            await this.videoElement.play();
            return true;
        } catch (error) {
            console.error('Error accessing camera:', error);
            if (this.options.onError) {
                this.options.onError(error);
            }
            return false;
        }
    }

    startRecording() {
        if (this.isRecording) return;

        navigator.mediaDevices.getUserMedia({ video: true })
            .then(stream => {
                this.videoElement.srcObject = stream;

                const options = { mimeType: 'video/webm;codecs=vp9' };
                this.mediaRecorder = new MediaRecorder(stream, options);

                this.mediaRecorder.ondataavailable = (event) => {
                    if (event.data.size > 0) {
                        this.recordedChunks.push(event.data);
                    }
                };

                this.recordedChunks = [];
                this.mediaRecorder.start();
                this.startTime = Date.now();
                this.isRecording = true;

                // Actualizar UI
                this.startBtn.style.display = 'none';
                this.stopBtn.style.display = 'inline-block';
                this.recordingIndicator.style.display = 'block';

                // Iniciar contador
                if (this.recordingInterval) {
                    clearInterval(this.recordingInterval);
                }
                this.recordingInterval = setInterval(this.updateRecordingTime, 1000);
            })
            .catch(error => {
                console.error('Error starting recording:', error);
                if (this.options.onError) {
                    this.options.onError(error);
                }
            });
    }

    stopRecording() {
        if (!this.isRecording) return;

        this.mediaRecorder.stop();
        this.isRecording = false;

        // Detener todas las tracks
        const stream = this.videoElement.srcObject;
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }
        this.videoElement.srcObject = null;

        // Actualizar UI
        this.startBtn.style.display = 'inline-block';
        this.stopBtn.style.display = 'none';
        this.recordingIndicator.style.display = 'none';

        // Detener contador
        if (this.recordingInterval) {
            clearInterval(this.recordingInterval);
        }

        // Crear blob y llamar callback
        const videoBlob = new Blob(this.recordedChunks, { type: 'video/webm' });
        if (this.options.onVideoRecorded) {
            this.options.onVideoRecorded(videoBlob);
        }
    }

    updateRecordingTime() {
        if (this.isRecording) {
            const elapsedTime = Math.round((Date.now() - this.startTime) / 1000);
            this.recordingTime.textContent = `${elapsedTime}s`;
        }
    }

    // Método para limpiar recursos
    destroy() {
        if (this.recordingInterval) {
            clearInterval(this.recordingInterval);
        }

        const stream = this.videoElement.srcObject;
        if (stream) {
            stream.getTracks().forEach(track => track.stop());
        }

        this.startBtn.removeEventListener('click', this.startRecording);
        this.stopBtn.removeEventListener('click', this.stopRecording);
    }
} 