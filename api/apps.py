from django.apps import AppConfig
class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'
    def ready(self):
        try:
            from .seed import run_seed
            run_seed()
        except Exception:
            pass
