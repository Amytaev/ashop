from django.urls import path
from . import views
from django.urls import path
from .views import admin_panel, techsupport_view, user_posts, delete_post

urlpatterns = [

    path('', views.home, name='aashop'),

    path('admin_panel/', admin_panel, name='admin_panel'),
    path('admin_panel/user/<int:user_id>/posts/', user_posts, name='user_posts'),
    path('admin_panel/post/<int:post_id>/delete/', delete_post, name='delete_post'),
    
    # Авторизация
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('reset-password/', views.reset_password_view, name='reset_password'),
    path('adminis/', views.adminis_view, name='adminis'),
    path('logout/', views.logout_view, name='logout'),

    # Информация
    path('info/delivery/', views.delivery_view, name='delivery'),
    path('info/guide/', views.guide_view, name='guide'),
    path('info/stock/', views.stock_view, name='stock'),
    path('techsupport/', views.techsupport_view, name='techsupport'),
    path('shop/', views.shop_view, name='shop'),

    path('profile/', views.profile_view, name='profile'),
    path('aboutuser/', views.aboutuser_view, name='aboutuser')

]


