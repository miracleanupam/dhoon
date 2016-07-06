from django.contrib import admin

# Register your models here.
from .models import Song, Album

admin.site.register(Album)
admin.site.register(Song)