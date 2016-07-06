from django.contrib.auth.models import Permission, User
from django.db import models

# Create your models here.
class Album(models.Model):
	user = models.ForeignKey(User, default=1)
	album_title = models.CharField(max_length=50)
	artist = models.CharField(max_length=50)
	genre = models.CharField(max_length=50)
	album_art = models.FileField()


	def __str__(self):
		return self.album_title+"-"+self.artist


class Song(models.Model):
	album = models.ForeignKey(Album, on_delete=models.CASCADE)
	name = models.CharField(max_length=50)#None=False, Blank=False)
	audio = models.FileField()

	def __str__(self):
		return self.name
