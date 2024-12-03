# apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'mainapp'

    def ready(self):
        import mainapp.signals  # Подключаем сигналы
