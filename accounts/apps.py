# accounts/apps.py

from django.apps import AppConfig

class AccountsConfig(AppConfig):  # Rename based on your app's name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'  # use your app's actual name

    def ready(self):
        import accounts.signals
