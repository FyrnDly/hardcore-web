const menuItems = document.querySelectorAll('.nav-link'); // Pilih semua elemen dengan kelas .nav-link

menuItems.forEach((item) => {
    item.addEventListener('click', (e) => {
        // Hapus kelas "active" dari semua elemen
        menuItems.forEach((el) => el.classList.remove('active'));

        // Tambahkan kelas "active" pada elemen yang diklik
        e.target.classList.add('active');
    });
});