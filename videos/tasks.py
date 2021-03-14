from celery.utils.log import get_task_logger
from celery import task
from datetime import datetime, timedelta
import requests
from django.db import IntegrityError
logger = get_task_logger(__name__)

# XNOTE: How should we scale Query to multiple queries? Maybe create a list and use a value randomly.
QUERY = "cricket"
FIELDS = 'items(id,snippet(title,description, publishTime, thumbnails))'


@task()
def fetch_videos_data_from_youtube():
	logger.info("Executing Fetch Videos Data from Youtube Task")
	# Get least frequently used key from database
	from keys.models import ApiKeys
	api_key_object = ApiKeys.objects.get_key()
	api_key_object.last_used = datetime.now()
	api_key_object.save()
	api_key = api_key_object.key

	# XNOTE: Can we improve last fetched time? Maybe use publishTime from last stored entry in database.
	last_fetched_time = datetime.now() - timedelta(seconds=10)
	last_fetched_time = last_fetched_time.isoformat('T') + "Z"
	url = f'https://www.googleapis.com/youtube/v3/search?key={api_key}&part=snippet&q={QUERY}&type=video&order=date&fields={FIELDS}&publishedAfter={last_fetched_time}'
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
