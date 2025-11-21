from django.apps import AppConfig

class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "api"

    def ready(self):
        # optional: run seeder on app ready in development
        try:
            from .seed import seed_database
            seed_database()
        except Exception:
            pass
