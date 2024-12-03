        // Функция для проверки, полностью ли элемент виден на экране
        function isElementInViewport(el) {
            const rect = el.getBoundingClientRect();
            return (
                rect.top >= 0 &&
                rect.left >= 0 &&
                rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                rect.right <= (window.innerWidth || document.documentElement.clientWidth)
            );
        }

        // Функция для раскрытия/сворачивания ответов
        function toggleAnswer(element) {
            const answerContent = element.querySelector('.answer-content');
            const isActive = element.classList.contains('active');

            if (isActive) {
                element.classList.remove('active');
                answerContent.style.maxHeight = answerContent.scrollHeight + "px"; // Устанавливаем текущее значение высоты
                requestAnimationFrame(() => {
                    answerContent.style.maxHeight = "0"; // Плавно закрываем
                    answerContent.style.paddingTop = "0"; // Убираем верхний отступ при закрытии
                    answerContent.style.paddingBottom = "0"; // Убираем нижний отступ при закрытии
                });
            } else {
                element.classList.add('active');
                answerContent.style.maxHeight = answerContent.scrollHeight + "px"; // Плавно раскрываем до полной высоты
                answerContent.style.paddingTop = "15px"; // Восстанавливаем отступы при открытии
                answerContent.style.paddingBottom = "10px"; // Восстанавливаем отступы при открытии

                // Прокручиваем страницу вниз, только если элемент не виден полностью
                setTimeout(() => {
                    if (!isElementInViewport(element)) {
                        element.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                }, 300); // Таймаут для плавного открытия перед прокруткой
            }
        }

                            // Проверка сессии пользователя
                            fetch('/check-session').then(response => response.json()).then(data => {
                        if (data.isLoggedIn) {
                            document.querySelector('.login-btn').outerHTML = `
                                <a href="profile/profile.html" class="profile-btn">Профиль</a>
                            `;
                        }
                    });