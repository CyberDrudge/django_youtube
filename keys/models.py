from django.db import models


# Create your models here.
class ApiKeysQuerySet(models.query.QuerySet):
	def get_key(self):
		return self.filter(is_active=True).order_by('last_used').first()


class ApiKeysManager(models.Manager):
	def get_queryset(self):
		return ApiKeysQuerySet(self.model, using=self._db)

	def get_key(self):
		return self.get_queryset().get_key()


class ApiKeys(models.Model):
	# XNOTE: is directly saving key in db safe? Maybe encrypt it.
	key = models.CharField(max_length=120, unique=True)
	is_active = models.BooleanField(default=True)
	last_used = models.DateTimeField(auto_now_add=True)

	objects = ApiKeysManager()
