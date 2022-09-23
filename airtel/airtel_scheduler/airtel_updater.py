from apscheduler.schedulers.background import BackgroundScheduler
from airtel.views import AirtelViewSet

def start():
    scheduler = BackgroundScheduler()
    airtel = AirtelViewSet()
    scheduler.add_job(airtel.save_data, "interval", minutes=10, id="airtel_001", replace_existing=True)
    scheduler.start()