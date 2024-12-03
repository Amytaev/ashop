document.querySelector('.edit-photo-btn').addEventListener('click', () => {
    document.getElementById('avatar-upload').click();
});

document.getElementById('avatar-upload').addEventListener('change', (event) => {
    const file = event.target.files[0];
    const preview = document.querySelector('.profile-avatar');
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
    };
    reader.readAsDataURL(file);
});
