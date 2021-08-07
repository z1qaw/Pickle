from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    # def ready(self) -> None:
    #     from backend.services.youtube import YoutubeApi
    #     YoutubeApi.authenticate()
