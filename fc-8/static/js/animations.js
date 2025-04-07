document.addEventListener('DOMContentLoaded', () => {
    const background = createSecureBackground();
    document.body.insertBefore(background, document.body.firstChild);

    function createSecureBackground() {
        const container = document.createElement('div');
        container.className = 'luxury-secure-background';

        container.appendChild(createElement('privacy-layer'));
        container.appendChild(createElement('encryption-lines'));

        for (let i = 0; i < 3; i++) {
            const glow = createElement('secure-glow');
            glow.style.left = `${Math.random() * 100}%`;
            glow.style.top = `${Math.random() * 100}%`;
            glow.style.animationDelay = `${i * -5}s`;
            container.appendChild(glow);
        }

        createDataStreams(container);
        return container;
    }

    function createDataStreams(container) {
        const characters = '01';
        for (let i = 0; i < 20; i++) {
            const stream = createElement('data-stream');
            stream.style.left = `${i * 5}%`;
            stream.style.animationDelay = `${i * -0.5}s`;
            stream.textContent = Array(20).fill(0)
                .map(() => characters[Math.floor(Math.random() * characters.length)])
                .join('');
            container.appendChild(stream);
        }
    }

    function createElement(className) {
        const element = document.createElement('div');
        element.className = className;
        return element;
    }
});
