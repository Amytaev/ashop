# admin.py
from django.contrib import admin
from .models import Post, CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.register(CustomUser, CustomUserAdmin)

class PostAdmin(admin.ModelAdmin):
    list_display = ('content', 'created_at', 'user', 'is_deleted')  # Поля для отображения
    list_filter = ('is_deleted', 'created_at')  # Фильтры по статусу и дате
    search_fields = ('content', 'user__username')  # Поля поиска
    actions = ['delete_posts']  # Кастомное действие

    @admin.action(description='Удалить выбранные посты')
    def delete_posts(self, request, queryset):
        queryset.update(is_deleted=True)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(Post, PostAdmin)