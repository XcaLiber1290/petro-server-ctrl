document.getElementById('startBtn').addEventListener('click', function() {
    fetch('/start-server', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Server Started:', data);
            updateServerStatus();
        });
});

document.getElementById('stopBtn').addEventListener('click', function() {
    fetch('/stop-server', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Server Stopped:', data);
            updateServerStatus();
        });
});

document.getElementById('restartBtn').addEventListener('click', function() {
    fetch('/restart-server', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            console.log('Server Restarted:', data);
            updateServerStatus();
        });
});

// Fetch server status
function updateServerStatus() {
    fetch('/server-status')
        .then(response => response.json())
        .then(data => {
            document.getElementById('serverStatus').innerText = data.online ? 'Server is Online' : 'Server is Offline';
            document.getElementById('playerCount').innerText = `Players Online: ${data.players_online}`;
        });
}

// Initial update
updateServerStatus();
