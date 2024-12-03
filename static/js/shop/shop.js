// Когда страница загружается, делаем один запрос для получения данных профиля
document.addEventListener('DOMContentLoaded', function() {
    // Проверка сессии пользователя и загрузка профиля
    fetch('/check-session')
        .then(response => response.json())
        .then(data => {
            if (data.isLoggedIn) {
                // Обновляем имя пользователя
                document.getElementById('username').textContent = data.username;
                // Обновляем аватар пользователя
                document.getElementById('profile-avatar').src = data.avatar ? data.avatar : '/path/to/default-avatar.png';
            } else {
                // Если пользователь не авторизован, перенаправляем на страницу авторизации
                window.location.href = '/autorization/login.html';
            }
        })
        .catch(error => console.error('Ошибка при проверке сессии:', error));
});

// Логика выхода из аккаунта
document.getElementById('logout-btn').addEventListener('click', function(e) {
    e.preventDefault(); // Предотвращаем стандартное действие кнопки
    fetch('/logout')
        .then(response => {
            if (response.ok) {
                window.location.href = '../autorization/login.html'; // Перенаправление на страницу входа после выхода
            } else {
                alert('Ошибка при выходе');
            }
        })
        .catch(err => console.error('Ошибка выхода:', err));
});

// Логика для загрузки аватара
document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Предотвращаем стандартное поведение формы

    const formData = new FormData();
    const fileField = document.getElementById('avatar'); // Выбранный файл аватара

    formData.append('avatar', fileField.files[0]);

    // Отправка файла на сервер
    fetch('/upload-avatar', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.filePath) {
            // Обновляем аватар в правом верхнем углу
            document.getElementById('profile-avatar').src = data.filePath;
            document.getElementById('upload-status').textContent = 'Аватар успешно загружен!';
        } else {
            document.getElementById('upload-status').textContent = 'Ошибка при загрузке аватара.';
        }
    })
    .catch(error => {
        console.error('Ошибка при загрузке аватара:', error);
        document.getElementById('upload-status').textContent = 'Ошибка при загрузке аватара.';
    });
});

// Логика поиска товаров
document.getElementById('search-form').addEventListener('submit', function(e) {
    e.preventDefault(); // Предотвращаем стандартное поведение формы

    const query = document.getElementById('search-input').value;

    // Отправка запроса на сервер для поиска товаров
    fetch(`/search?q=${query}`)
        .then(response => response.json())
        .then(products => {
            const productsContainer = document.getElementById('products-container');
            productsContainer.innerHTML = ''; // Очищаем предыдущие результаты

            if (products.length === 0) {
                productsContainer.innerHTML = '<p>Ничего не найдено</p>';
            } else {
                products.forEach(product => {
                    const productBox = `
                        <div class="product-box">
                            <img src="${product.image_url}" alt="${product.name}">
                            <h3>${product.name}</h3>
                            <p class="product-price">${product.price} KZT</p>
                        </div>
                    `;
                    productsContainer.innerHTML += productBox;
                });
            }
        })
        .catch(error => console.error('Ошибка поиска:', error));
});

// Логика для загрузки товаров по категориям
document.querySelectorAll('.sidebar a').forEach(link => {
    link.addEventListener('click', function(event) {
        event.preventDefault();  // Предотвращаем переход по ссылке

        const category = event.currentTarget.getAttribute('data-category');
        if (category) {
            loadProductsByCategory(category); // Загрузка товаров по выбранной категории
        }
    });
});

function loadProductsByCategory(category) {
    // Запрос на сервер для получения товаров по категории
    fetch(`/category?cat=${category}`)
        .then(response => response.json())
        .then(products => {
            const productsContainer = document.getElementById('products-container');
            productsContainer.innerHTML = '';  // Очищаем контейнер с товарами

            // Добавляем товары на страницу
            products.forEach(product => {
                const imageUrl = product.image_url ? `/images/${product.image_url}` : '/images/default.jpg';

                const productBox = `
                    <div class="product-box">
                        <img src="${imageUrl}" alt="${product.name}">
                        <p class="product-price">${product.price} ₸</p>
                        <div class="product-info">
                            <span class="supplier">${product.supplier || 'Неизвестный поставщик'}</span>
                            <span class="product-name">${product.name}</span>
                        </div>
                    </div>
                `;
                productsContainer.innerHTML += productBox;
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки товаров:', error);
        });
}

document.addEventListener('DOMContentLoaded', () => {
    const productsContainer = document.getElementById('products-container');
    const products = Array.from(productsContainer.children); // Получаем все элементы товаров

    // Функция для перемешивания массива
    function shuffleArray(array) {
        for (let i = array.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [array[i], array[j]] = [array[j], array[i]]; // Меняем местами
        }
    }

    // Перемешиваем массив товаров
    shuffleArray(products);

    // Очищаем контейнер и добавляем перемешанные товары обратно
    productsContainer.innerHTML = '';
    products.forEach(product => productsContainer.appendChild(product));
});
