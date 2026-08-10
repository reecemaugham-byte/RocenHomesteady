/*
 * auth.js — Shared authentication state for Rocen Homesteady.
 * Include this on every page to update the nav based on login state.
 * 
 * The nav must have an element with id="authArea":
 *   <span id="authArea"><a href="/login">Login</a></span>
 */

(function() {
    document.addEventListener('DOMContentLoaded', function() {
        updateAuthNav();
    });

    function updateAuthNav() {
        var authArea = document.getElementById('authArea');
        if (!authArea) return;

        var userStr = localStorage.getItem('rocen_user');
        if (!userStr) {
            authArea.innerHTML = '<a href="/login" class="nav-login-link">Login</a>';
            return;
        }

        try {
            var user = JSON.parse(userStr);
            if (user && user.username) {
                checkSession(user.username, authArea);
            } else {
                localStorage.removeItem('rocen_user');
                authArea.innerHTML = '<a href="/login" class="nav-login-link">Login</a>';
            }
        } catch(e) {
            localStorage.removeItem('rocen_user');
            authArea.innerHTML = '<a href="/login" class="nav-login-link">Login</a>';
        }
    }

    function checkSession(username, authArea) {
        authArea.innerHTML = 
            '<span class="nav-user">👤 ' + escapeHtml(username) + '</span>' +
            '<a href="#" onclick="window.logout(event)" class="nav-logout">Logout</a>';

        fetch('/api/auth/me')
            .then(function(r) { return r.json(); })
            .then(function(data) {
                if (!data.authenticated) {
                    localStorage.removeItem('rocen_user');
                    authArea.innerHTML = '<a href="/login" class="nav-login-link">Login</a>';
                }
            })
            .catch(function() {
                // Network error — keep showing logged-in state
            });
    }

    function escapeHtml(str) {
        var div = document.createElement('div');
        div.textContent = str;
        return div.innerHTML;
    }

    // ==========================================
    // LOGOUT
    // ==========================================
    window.logout = function(e) {
        if (e) e.preventDefault();
        fetch('/api/auth/logout', { method: 'POST' })
            .catch(function() {})
            .finally(function() {
                localStorage.removeItem('rocen_user');
                sessionStorage.removeItem('rocen_merged'); // Fresh merge on next login
                window.location.href = '/';
            });
    };
})();
