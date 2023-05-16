from django.apps import AppConfig


class BakedbyalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BakedByAl'

    def ready(self):
        import BakedByAl.signals