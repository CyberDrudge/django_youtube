from celery.utils.log import get_task_logger
from celery import task
from datetime import datetime, timedelta
import requests
from django.db import IntegrityError
logger = get_task_logger(__name__)

# XNOTE: Store all keys in env before deploying to production.
API_KEY = "AIzaSyBOqu1Rz7uxL0pPj9vbaLG_bXGH8lXDQa0"
# XNOTE: How should we scale Query to multiple queries? Maybe create a list and use a value randomly.
QUERY = "cricket"
FIELDS = 'items(id,snippet(title,description, publishTime, thumbnails))'


@task()
def fetch_videos_data_from_youtube():
	logger.info("Executing Fetch Videos Data from Youtube Task")
	# XNOTE: Can we improve last fetched time? Maybe use publishTime from last stored entry in database.
	last_fetched_time = datetime.now() - timedelta(seconds=10)
	last_fetched_time = last_fetched_time.isoformat('T') + "Z"
	url = f'https://www.googleapis.com/youtube/v3/search?key={API_KEY}&part=snippet&q={QUERY}&type=video&order=date&fields={FIELDS}&publishedAfter={last_fetched_time}'
	response = requests.get(url)
	data = response.json()
	items = data.get('items', [])
	from .models import Video
	for item in items:
		try:
			videoId = item.get('id', {}).get('videoId', "")
			snippet = item.get('snippet', {})
			title = snippet.get('title', "")
			description = snippet.get('description', "")
			thumbnail = snippet.get('thumbnails', {}).get('default', {}).get('url', "")
			publishTime = snippet.get('publishTime', {})
			Video.objects.create(
				videoId=videoId,
				title=title,
				description=description,
				thumbnail=thumbnail,
				publishTime=publishTime
			)
		except IntegrityError:
			# Occurs when the video is already in the database
			pass
		except Exception as e:
			logger.error(e)
	logger.info("Fetch Videos Data from Youtube Task Completed")
	return "TASK COMPLETED"
