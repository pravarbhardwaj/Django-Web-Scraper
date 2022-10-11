from django.apps import AppConfig


class AirtelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airtel'

    def ready(self):
        print('Fetching and saving data on first run for airtel plans')
        from airtel.views import AirtelViewSet
        airtel = AirtelViewSet()
        airtel.save_data()
        print('Initialising scheduler')
        from .scheduler import updater
        updater.start()
