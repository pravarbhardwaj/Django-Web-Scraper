from django.apps import AppConfig


class AirtelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'airtel'

    def ready(self):
        print('Fetching and saving data on first run')
        from airtel.views import AirtelViewSet
        airtel = AirtelViewSet()
        airtel.save_data()
        print('Initialising scheduler')
        from .airtel_scheduler import airtel_updater
        airtel_updater.start()
