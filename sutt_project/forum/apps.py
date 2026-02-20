from django.apps import AppConfig


class ForumConfig(AppConfig):
    name = "forum"
    
    def ready(self):
        """
        Import signals when app is ready.
        This ensures signal handlers are registered.
        """
        import forum.signals
