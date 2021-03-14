from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from videos.tasks import fetch_videos_data_from_youtube

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_youtube.settings')
app = Celery('django_youtube')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs after every 10 seconds
    sender.add_periodic_task(10.0, fetch_videos_data_from_youtube, name='Fetch Data from Youtube API')
