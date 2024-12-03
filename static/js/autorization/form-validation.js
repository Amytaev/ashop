$(document).ready(function(){
    // Проверка никнейма в реальном времени
    $("input[name='username']").on("input", function(){
        let username = $(this).val();
        $.ajax({
            url: "{% url 'check_username' %}",
            data: { 'username': username },
            success: function(data) {
                if (data.available) {
                    $("input[name='username']").removeClass("error");
                    $(".username-error").text("");
                } else {
                    $("input[name='username']").addClass("error");
                    $(".username-error").text("Этот никнейм уже занят.");
                }
            }
        });
    });

    // Проверка номера телефона в реальном времени
    $("input[name='phone']").on("input", function(){
        let phone = $(this).val();
        $.ajax({
            url: "{% url 'check_phone' %}",
            data: { 'phone': phone },
            success: function(data) {
                if (data.available) {
                    $("input[name='phone']").removeClass("error");
                    $(".phone-error").text("");
                } else {
                    $("input[name='phone']").addClass("error");
                    $(".phone-error").text("Этот номер телефона уже занят.");
                }
            }
        });
    });

    // Проверка email на занятость в реальном времени
    $("input[name='email']").on("input", function(){
        let email = $(this).val();
        $.ajax({
            url: "{% url 'check_email' %}",
            data: { 'email': email },
            success: function(data) {
                if (data.available) {
                    $("input[name='email']").removeClass("error");
                    $(".email-error").text("");
                } else {
                    $("input[name='email']").addClass("error");
                    $(".email-error").text("Этот email уже занят.");
                }
            }
        });
    });

    // Валидация пароля
    $("input[name='password']").on("input", function(){
        let password = $(this).val();
        let passwordError = $(".password-error");

        // Проверка на длину пароля
        if (password.length < 8) {
            passwordError.text("Пароль должен содержать хотя бы 8 символов.");
            $(this).addClass("error");
        } 
        // Проверка на наличие цифры
        else if (!/\d/.test(password)) {
            passwordError.text("Пароль должен содержать хотя бы одну цифру.");
            $(this).addClass("error");
        }
        // Если пароль проходит валидацию
        else {
            passwordError.text("");
            $(this).removeClass("error");
        }
    });

    // Валидация подтверждения пароля
    $("input[name='confirm_password']").on("input", function(){
        let password = $("input[name='password']").val();
        let confirmPassword = $(this).val();
        let confirmPasswordError = $(".confirm-password-error");

        if (password !== confirmPassword) {
            confirmPasswordError.text("Пароли не совпадают.");
            $(this).addClass("error");
        } else {
            confirmPasswordError.text("");
            $(this).removeClass("error");
        }
    });
});
