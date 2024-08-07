document.addEventListener('DOMContentLoaded', function() {
    var loginButton = document.getElementById('login-button');
    var modal = document.getElementById('login-modal');
    var closeButton = document.querySelector('.close-button');

    loginButton.onclick = function() {
        modal.style.display = 'block';
    }

    closeButton.onclick = function() {
        modal.style.display = 'none';
    }

    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    }
});
