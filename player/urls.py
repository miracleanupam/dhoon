from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login_user'),
    url(r'^(?P<album_id>[0-9]+)/$', views.interface, name='interface'),
    url(r'^logout/$', views.logout_user, name='logout_user'),
    url(r'^(?P<album_id>[0-9]+)/delete_album/$', views.delete_album, name='delete_album'),
    url(r'^(?P<album_id>[0-9]+)/delete_song/(?P<song_id>[0-9]+)/$', views.delete_song, name='delete_song'),
    url(r'^(?P<album_id>[0-9]+)/create_song/$', views.create_song, name='create_song'),
    url(r'^create_album/$', views.create_album, name='create_album'),
    url(r'^songs/(?P<filter_by>[a-zA_Z]+)/$', views.songs, name='songs'),
    url(r'^test/$', views.test, name='test'),
]
