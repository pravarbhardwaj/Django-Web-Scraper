from apscheduler.schedulers.background import BackgroundScheduler
from jio.views import JioViewSet

def start():
    scheduler = BackgroundScheduler()
    jio = JioViewSet()
    scheduler.add_job(jio.save_data, "interval", minutes=10, id="jio_001", replace_existing=True)
    scheduler.start()