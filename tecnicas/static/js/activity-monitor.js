const MONITOR_CONFIG = {
    heartbeatInterval: 30000, // 30 seconds
    inactivityThreshold: 600000, // 10 minutes
    apiEndpoint: '/cata/testers/api/activity',
    csrfToken: document.querySelector('[name=csrfmiddlewaretoken]')?.value
};

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function sendActivitySignal(action) {
    const sessionCode = document.querySelector('.code-sesion')?.textContent

    if (!sessionCode) {
        console.warn('Session code not found for activity monitor');
        return;
    }

    const data = new FormData();
    data.append('action', action);
    data.append('session_code', sessionCode);
    const csrfToken = getCookie('csrftoken');

    if (action === 'exit') {
        data.append('csrfmiddlewaretoken', csrfToken);
        navigator.sendBeacon(MONITOR_CONFIG.apiEndpoint, data);
    } else {
        fetch(MONITOR_CONFIG.apiEndpoint, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken
            },
            body: data,
            keepalive: true // Redundant if not 'exit' effectively, but good practice
        }).catch(err => console.error('Heartbeat error:', err));
    }
}

setInterval(() => {
    sendActivitySignal('heartbeat');
}, MONITOR_CONFIG.heartbeatInterval);

sendActivitySignal('heartbeat');

document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
        // User might be switching tabs OR closing.
        // We can treat this as potential 'exit' OR just rely on heartbeat.
        // If we send 'exit' here, the user returning to the tab might be considered 'inactive' 
        // until the next heartbeat. 
        // Given the requirement is "leave the session", closing the tab is the main one.
        // "visibilityState === hidden" fires on tab switch too. We probably DON'T want to kill session on tab switch.
        // ONLY on unload.
    }
});

window.addEventListener('beforeunload', (event) => {
    sendActivitySignal('exit');
});
