from django.apps import AppConfig


class MochatsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "mochats"

    def ready(self):
        import mochats.signals
