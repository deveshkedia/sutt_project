from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"
    
    def ready(self):
        """
        Import signals when app is ready.
        This ensures signal handlers are registered.
        """
        import users.signals
