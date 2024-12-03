from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import logout
from .forms import AvatarUploadForm
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib import messages
from .models import CustomUser, Post
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max

def home(request):
    return render(request, 'aashop.html')  # Главная страница

# Авторизация
def login_view(request):
    return render(request, 'autorization/login.html', {'active_page': 'login'})

def register_view(request):
    return render(request, 'autorization/register.html', {'active_page': 'register'})

def reset_password_view(request):
    return render(request, 'autorization/reset-password.html', {'active_page': 'reset-password'})

def adminis_view(request):
    return render(request, 'administration/adminis.html')

# Информация
def delivery_view(request):
    return render(request, 'information/delivery.html')

def guide_view(request):
    return render(request, 'information/guide.html')

def stock_view(request):
    return render(request, 'information/stock.html')

def techsupport_view(request):
    return render(request, 'information/techsupport.html')

def shop_view(request):
    return render(request, 'shop/shop.html')

from django.shortcuts import render

def profile_view(request):
    return render(request, 'profile/profile.html', {
        'show_sidebar': True
    })

def aboutuser_view(request):
    return render(request, 'profile/aboutuser.html', {
        'show_sidebar': False
    })




# Авторизация.

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # Если введен email, ищем пользователя по email
            if '@' in username_or_email:
                user = authenticate(request, email=username_or_email, password=password)
            else:
                user = authenticate(request, username=username_or_email, password=password)

            if user is not None:
                login(request, user)

                # Проверка роли
                if user.role in ['Модератор', 'Админ']:  # Замените на точные значения, используемые в вашей модели
                    return redirect('adminis')  # Перенаправление для модераторов и админов
                else:
                    return redirect('aashop')  # Перенаправление для обычных пользователей

            else:
                form.add_error(None, 'Неверные данные для входа.')
    else:
        form = LoginForm()

    return render(request, 'autorization/login.html', {'form': form, 'active_page': 'login'})

# Регистрация
def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Не сохраняем пользователя сразу
            user.set_password(form.cleaned_data['password'])  # Хешируем пароль
            user.save()  # Сохраняем пользователя с хешированным паролем
            login(request, user)  # Авторизуем пользователя сразу после регистрации
            return redirect('aashop')  # Перенаправляем на главную страницу после успешной регистрации
        else:
            # Если форма не валидна, возвращаем с ошибками
            return render(request, 'autorization/register.html', {'form': form, 'active_page': 'register'})
    else:
        form = RegistrationForm()  # Инициализируем пустую форму

    return render(request, 'autorization/register.html', {'form': form, 'active_page': 'register'})


# Выход из аккаунта
def logout_view(request):
    logout(request)
    return redirect('aashop')  # перенаправление после выхода

# Загрузка фото в профиль.

def profile_view(request):
    if request.method == 'POST':
        form = AvatarUploadForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = AvatarUploadForm(instance=request.user)

    return render(request, 'profile/profile.html', {'form': form})



# Модель постов.

def techsupport_view(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        if title and content:
            try:
                Post.objects.create(title=title, content=content, user=request.user)
                messages.success(request, 'Пост был успешно создан!')
            except Exception as e:
                messages.error(request, f'Ошибка: {e}')
            return redirect('techsupport')

    # Получаем параметр сортировки из URL
    sort_order = request.GET.get('sort', 'asc')  # По умолчанию сортировка по возрастанию

    # Выбираем сортировку и учитываем только не удаленные посты
    if sort_order == 'desc':
        user_posts = Post.objects.filter(user=request.user, is_deleted=False).order_by('-created_at')
    else:
        user_posts = Post.objects.filter(user=request.user, is_deleted=False).order_by('created_at')

    # Отправляем данные в шаблон
    return render(request, 'information/techsupport.html', {
        'user_posts': user_posts,
        'sort_order': sort_order  # Передаем параметр сортировки в шаблон
    })


def admin_check(user):
    return user.is_superuser  # Ограничиваем доступ только для суперпользователей

@user_passes_test(admin_check)
def admin_panel(request):
    sort_order = request.GET.get('sort', 'desc')  # Получаем параметр сортировки (по умолчанию 'desc')
    users = CustomUser.objects.annotate(last_post_date=Max('post__created_at'))

    # Сортировка в зависимости от параметра
    if sort_order == 'asc':
        users = users.order_by('last_post_date')  # Сортировка по возрастанию
    else:
        users = users.order_by('-last_post_date')  # Сортировка по убыванию

    return render(request, 'administration/admin_panel.html', {'users': users, 'sort_order': sort_order})



@user_passes_test(admin_check)
def user_posts(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    posts = Post.objects.filter(user=user, is_deleted=False)
    return render(request, 'administration/user_posts.html', {'user': user, 'posts': posts})


@user_passes_test(admin_check)
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.is_deleted = True
    post.save()
    # Перенаправляем на страницу со списком постов пользователя
    return redirect('user_posts', user_id=post.user.id)


