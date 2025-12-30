const canvas = document.getElementById("canvas");
const ctx = canvas.getContext("2d");

function resize() {
  canvas.width = innerWidth;
  canvas.height = innerHeight;
}
resize();
addEventListener("resize", resize);

let audioStarted = false;
const bgMusic = new Audio("goodnight.mp3");
bgMusic.loop = false;
bgMusic.volume = 1.0;

const boomSound = new Audio("sound.mp3.mp3");
boomSound.volume = 1.0;

function startAudio() {
  if (audioStarted) return;
  bgMusic.play();
  audioStarted = true;
  document.getElementById("hint").style.display = "none";
}
addEventListener("click", startAudio);
addEventListener("touchstart", startAudio);

const bgText = document.getElementById("bgText");
const texts = [
  " Goodbyee 2025 ",
  " Welcome 2026 ",
  " Celebrate the Night ",
  " Make Every Moment Shine "
];

let textIndex = 0;

function changeText() {
  bgText.style.opacity = 0;
  bgText.style.transform = "scale(0.9)";
  bgText.style.filter = "blur(10px)";
  setTimeout(() => {
    bgText.textContent = texts[textIndex];
    textIndex = (textIndex + 1) % texts.length;
    bgText.style.opacity = 1;
    bgText.style.transform = "scale(1)";
    bgText.style.filter = "blur(0)";
  }, 1200);
}

setInterval(changeText, 4000);

class Firework {
  constructor(x, y, targetY) {
    this.x = x;
    this.y = y;
    this.targetY = targetY;
    this.speed = Math.random() * 3 + 6;
    this.exploded = false;
  }
  update() {
    this.y -= this.speed;
    this.speed *= 0.99;
    if (this.y <= this.targetY && !this.exploded) {
      this.exploded = true;
      explode(this.x, this.y);
    }
  }
  draw() {
    ctx.fillStyle = "white";
    ctx.beginPath();
    ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
    ctx.fill();
  }
}

class Particle {
  constructor(x, y, color) {
    const a = Math.random() * Math.PI * 2;
    const s = Math.random() * 6 + 2;
    this.x = x;
    this.y = y;
    this.vx = Math.cos(a) * s;
    this.vy = Math.sin(a) * s;
    this.alpha = 1;
    this.decay = Math.random() * 0.015 + 0.01;
    this.color = color;
  }
  update() {
    this.vy += 0.05;
    this.x += this.vx;
    this.y += this.vy;
    this.alpha -= this.decay;
  }
  draw() {
    ctx.save();
    ctx.globalAlpha = this.alpha;
    ctx.shadowBlur = 15;
    ctx.shadowColor = this.color;
    ctx.fillStyle = this.color;
    ctx.beginPath();
    ctx.arc(this.x, this.y, 2, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
  }
}

let fireworks = [];
let particles = [];

function explode(x, y) {
  if (audioStarted) {
    boomSound.currentTime = 0;
    boomSound.play();
  }
  const color = `hsl(${Math.random() * 360},100%,60%)`;
  for (let i = 0; i < 120; i++) {
    particles.push(new Particle(x, y, color));
  }
}

function launchFirework() {
  fireworks.push(
    new Firework(
      Math.random() * canvas.width,
      canvas.height,
      Math.random() * canvas.height * 0.5 + 100
    )
  );
}

function animate() {
  requestAnimationFrame(animate);
  ctx.fillStyle = "rgba(0,0,0,0.2)";
  ctx.fillRect(0, 0, canvas.width, canvas.height);

  fireworks = fireworks.filter(f => !f.exploded);
  particles = particles.filter(p => p.alpha > 0);

  fireworks.forEach(f => { f.update(); f.draw(); });
  particles.forEach(p => { p.update(); p.draw(); });
}

setInterval(launchFirework, 500);
animate();
