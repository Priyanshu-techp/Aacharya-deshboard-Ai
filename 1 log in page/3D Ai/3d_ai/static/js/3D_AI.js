// Canvas setup
const canvas = document.querySelector("canvas");
const ctx = canvas.getContext("2d");

// Animation settings
const frameCount = 300;
const targetFPS = 60;
const forwardSpeed = .7;
const reverseSpeed = .7;

// Animation variables
const images = new Array(frameCount).fill(null); // Pre-fill array
let currentFrame = 0;
let animationId = null;
let lastTimestamp = 0;
let lastRenderedFrame = -1;
let isReversing = false;

// Set canvas to full window size
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    if (images[Math.floor(currentFrame)]) {
        render(); // Redraw on resize
    }
}
resizeCanvas();
window.addEventListener('resize', resizeCanvas);

// Load all images silently
function loadImages() {
    for (let i = 0; i < frameCount; i++) {
        const img = new Image();
        const num = (i + 1).toString().padStart(4, '0');
        img.src = `../static/images/male${num}.png`;
        
        img.onload = () => {
            images[i] = img;
            // Start rendering when first image loads
            if (i === 0) {
                render();
                animate(performance.now());
            }
        };
    }
}

// Full-screen rendering with aspect ratio preservation
function render() {
    const frame = Math.floor(currentFrame);
    const img = images[frame];
    if (!img) return;
    
    // Clear only if frame changed
    if (frame !== lastRenderedFrame) {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        lastRenderedFrame = frame;
    }
    
    // Calculate dimensions to fill screen while preserving aspect ratio
    const scale = Math.max(
        canvas.width / img.width,
        canvas.height / img.height
    );
    
    // Center the image
    const width = img.width * scale;
    const height = img.height * scale;
    const x = (canvas.width - width) / 2;
    const y = (canvas.height - height) / 2;
    
    // Draw image edge-to-edge
    ctx.imageSmoothingEnabled = true;
    ctx.drawImage(img, x, y, width, height);
}

// Animation loop
function animate(timestamp) {
    if (!lastTimestamp) lastTimestamp = timestamp;
    
    const deltaTime = timestamp - lastTimestamp;
    const targetDelta = 1000 / targetFPS;
    
    if (deltaTime >= targetDelta) {
        const speed = isReversing ? -reverseSpeed : forwardSpeed;
        currentFrame += (deltaTime / 1000) * targetFPS * speed;
        
        // Reverse direction at ends
        if (currentFrame >= frameCount - 1) {
            currentFrame = frameCount - 1;
            isReversing = true;
        } else if (currentFrame <= 0) {
            currentFrame = 0;
            isReversing = false;
        }
        
        lastTimestamp = timestamp;
        render();
    }
    
    animationId = requestAnimationFrame(animate);
}

// Start loading images immediately
loadImages();

// Prevent context menu
canvas.addEventListener('contextmenu', (e) => e.preventDefault());