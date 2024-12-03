// Variables pour suivre les interactions
let startTime = Date.now();
let buttonClicks = 0;

// Mettre à jour le temps passé sur la page
setInterval(() => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);
    document.getElementById('time-spent').innerText = timeSpent;
}, 1000);

// Suivre les clics sur le bouton
document.getElementById('cta-button').addEventListener('click', () => {
    buttonClicks++;
    document.getElementById('button-clicks').innerText = buttonClicks;

    // Envoyer les données au backend Flask
    fetch('/track-event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            event: 'button_click',
            product: 'T-shirt',
            price: 20,
            timestamp: new Date().toISOString()
        }),
    })
    .then(response => response.json())
    .then(data => console.log('Button click sent:', data))
    .catch(error => console.error('Error:', error));
});

// Envoyer le temps passé sur la page avant de quitter
window.addEventListener('beforeunload', () => {
    const timeSpent = Math.floor((Date.now() - startTime) / 1000);

    fetch('/track-event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            event: 'page_view',
            timeSpent: timeSpent,
            timestamp: new Date().toISOString()
        }),
    })
    .then(response => response.json())
    .then(data => console.log('Page view event sent:', data))
    .catch(error => console.error('Error:', error));
});
