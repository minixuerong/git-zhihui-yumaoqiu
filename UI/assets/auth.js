function checkAuth(requiredRole) {
    const isLoggedIn = localStorage.getItem('isLoggedIn');
    const role = localStorage.getItem('role');
    const username = localStorage.getItem('username');
    
    if (isLoggedIn !== 'true') {
        window.location.href = 'login.html';
        return false;
    }
    
    if (requiredRole && role !== requiredRole) {
        if (role === 'admin') {
            window.location.href = 'admin.html';
        } else {
            window.location.href = 'index.html';
        }
        return false;
    }
    
    return { isLoggedIn: true, role, username };
}

function logout() {
    localStorage.removeItem('isLoggedIn');
    localStorage.removeItem('username');
    localStorage.removeItem('role');
    window.location.href = 'login.html';
}

function getUsername() {
    return localStorage.getItem('username') || '用户';
}

function getUserAvatar() {
    const username = getUsername();
    return username.charAt(0).toUpperCase();
}

function isAdmin() {
    return localStorage.getItem('role') === 'admin';
}

function isUser() {
    return localStorage.getItem('role') === 'user';
}

function getUserRoleText() {
    return isAdmin() ? '管理员' : '普通用户';
}

function initSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (!sidebar) return;
    
    const footer = sidebar.querySelector('.sidebar-footer');
    if (!footer) {
        const footerHTML = `
            <div class="sidebar-footer">
                <div class="user-info">
                    <div class="user-avatar" id="sidebarAvatar">U</div>
                    <div class="user-detail">
                        <div class="user-name" id="sidebarUsername">用户</div>
                        <div class="user-role" id="sidebarRole">普通用户</div>
                    </div>
                </div>
                <button class="logout-btn" onclick="logout()"><span>退出登录</span></button>
            </div>
        `;
        sidebar.insertAdjacentHTML('beforeend', footerHTML);
    }
    
    document.getElementById('sidebarAvatar').textContent = getUserAvatar();
    document.getElementById('sidebarUsername').textContent = getUsername();
    document.getElementById('sidebarRole').textContent = getUserRoleText();
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.classList.toggle('collapsed');
    }
}