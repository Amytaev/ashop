document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const header = document.querySelector('header');
    const themeIcon = document.getElementById('theme-icon');
    const logo = document.getElementById('logo');
    
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        body.classList.add(savedTheme);
        header.classList.add(savedTheme);
        
        if (savedTheme === 'dark') {
            themeIcon.src = 'logo/dark.svg';
            logo.src = '/logo/Logo 2.svg';
        } else {
            themeIcon.src = 'logo/white.svg';
            logo.src = 'logo/Logo 1.svg';
        }
    }

    document.getElementById('theme-toggle-btn').addEventListener('click', function () {
        body.classList.toggle('dark');
        header.classList.toggle('dark');
        
        const currentTheme = body.classList.contains('dark') ? 'dark' : 'light';
        localStorage.setItem('theme', currentTheme);

        if (currentTheme === 'dark') {
            themeIcon.src = 'logo/dark.svg';
            logo.src = '/logo/Logo 2.svg';
        } else {
            themeIcon.src = 'logo/white.svg';
            logo.src = 'logo/Logo 1.svg';
        }
    });
});

fetch('/check-session').then(response => response.json()).then(data => {
    if (data.isLoggedIn) {
        document.querySelector('.login-btn').outerHTML = `
            <a href="profile/profile.html" class="profile-btn">
                <img src="${data.avatar}" alt="Аватар пользователя" class="profile-avatar">
            </a>
        `;
    }
}).catch(error => {
    console.error("Error fetching session:", error);
});
