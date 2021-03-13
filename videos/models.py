from django.db import models
from django.db.models import Q


# Create your models here.
class VideoQuerySet(models.query.QuerySet):
	def search(self, query):
		lookups = Q()
		for word in query.split():
			lookups |= Q(title__icontains=word) | Q(description__icontains=word)
		return self.filter(lookups).distinct()


class VideoManager(models.Manager):
	def get_queryset(self):
		return VideoQuerySet(self.model, using=self._db)

	def search(self, query):
		return self.get_queryset().search(query)


class Video(models.Model):
	videoId = models.CharField(max_length=120, unique=True)
	title = models.CharField(max_length=120, db_index=True)
	description = models.TextField(db_index=True)
	thumbnail = models.TextField()
	publishTime = models.DateTimeField(db_index=True)

	objects = VideoManager()

	def __str__(self):
		return self.title
