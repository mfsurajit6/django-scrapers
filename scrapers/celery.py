import os

from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scrapers.settings')

app = Celery('scrapers')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')

app.conf.beat_schedule = {
    'scrap_data_everyday_at_12':{
        'task': 'webscraper.tasks.scheduled_scraper',
        'schedule': crontab(hour=2),
    }
}


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
