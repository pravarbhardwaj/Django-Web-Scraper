from django.apps import AppConfig


class JioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'jio'

    def ready(self):
        print('Fetching and saving data on first run for jio plans')
        from jio.views import JioViewSet
        jio = JioViewSet()
        jio.save_data()
        print('Initialising scheduler')
        from .scheduler import updater
        updater.start()