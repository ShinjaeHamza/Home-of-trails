from django.apps import AppConfig


class AdoptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoptions'

class AdoptionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adoptions'

    def ready(self):
        import adoptions.signals  # Import the signals