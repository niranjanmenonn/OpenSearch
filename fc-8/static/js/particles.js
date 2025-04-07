class ParticleNetwork {
    constructor() {
        this.canvas = document.getElementById('particle-canvas');
        this.ctx = this.canvas.getContext('2d');
        this.particles = [];
        this.numberOfParticles = 50;
        this.connectDistance = 150;
        this.init();
        this.animate();
        this.handleResize();
    }

    init() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        
        for (let i = 0; i < this.numberOfParticles; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: Math.random() * 0.5 - 0.25,
                vy: Math.random() * 0.5 - 0.25,
                radius: Math.random() * 1.5 + 0.5
            });
        }
    }

    animate() {
        requestAnimationFrame(() => this.animate());
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            this.updateParticle(particle);
            this.drawParticle(particle);
        });
        this.drawConnections();
    }

    updateParticle(particle) {
        particle.x += particle.vx;
        particle.y += particle.vy;
        if (particle.x < 0 || particle.x > this.canvas.width) particle.vx *= -1;
        if (particle.y < 0 || particle.y > this.canvas.height) particle.vy *= -1;
    }

    drawParticle(particle) {
        this.ctx.beginPath();
        this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
        this.ctx.fillStyle = 'rgba(52, 152, 219, 0.6)';
        this.ctx.fill();
    }

    drawConnections() {
        this.particles.forEach((particle1, i) => {
            this.particles.slice(i + 1).forEach(particle2 => {
                const dx = particle1.x - particle2.x;
                const dy = particle1.y - particle2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);

                if (distance < this.connectDistance) {
                    this.ctx.beginPath();
                    this.ctx.moveTo(particle1.x, particle1.y);
                    this.ctx.lineTo(particle2.x, particle2.y);
                    this.ctx.strokeStyle = `rgba(52, 152, 219, ${0.2 - distance/this.connectDistance * 0.2})`;
                    this.ctx.stroke();
                }
            });
        });
    }

    handleResize() {
        window.addEventListener('resize', () => {
            this.canvas.width = window.innerWidth;
            this.canvas.height = window.innerHeight;
        });
    }
}
