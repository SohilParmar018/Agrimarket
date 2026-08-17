// Real-time notification updates
document.addEventListener('DOMContentLoaded', function() {
    // Update notification count
    function updateNotificationCount() {
        fetch('/notifications/unread-count')
            .then(response => response.json())
            .then(data => {
                const badge = document.getElementById('notificationCount');
                if (data.count > 0) {
                    badge.textContent = data.count;
                    badge.style.display = 'inline';
                } else {
                    badge.style.display = 'none';
                }
            })
            .catch(error => console.error('Error fetching notification count:', error));
    }
    
    // Update count on page load
    if (document.getElementById('notificationCount')) {
        updateNotificationCount();
        
        // Update every 30 seconds
        setInterval(updateNotificationCount, 30000);
    }
});
