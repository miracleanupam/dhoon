from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from .forms import UserForm, SongForm, AlbumForm
from .models import Song, Album

# Create your views here.

AUDIO_FILE_TYPES = ['wav', 'mp3', 'ogg']
IMG_TYPES = ['png', 'jpg', 'jpeg']

def index(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		albums = Album.objects.filter(user=request.user)
		song_results = Song.objects.all()
		query = request.GET.get("q")
		if query:
			albums = albums.filter(
				Q(album_title__icontains=query) |
				Q(artist__icontains=query)
			).distinct()
			song_results = song_results.filter(
				Q(name__icontains=query)
			).distinct()
			return render(request, 'home.html', {
				'albums':albums,
				'songs':song_results,
			})
		else:
			return render(request, 'home.html', {'albums': albums})

def create_album(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		form = AlbumForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			album = form.save(commit=False)
			album.user = request.user
			album.album_art = request.FILES['album_art']
			file_type = album.album_art.url.split('.')[-1]
			file_type = file_type.lower()
			if file_type not in IMG_TYPES:
				context = {
					'album':album,
					'form':form,
					'error_message':'Image is not in required format.',
				}
				return render(request, 'create_album.html', context)
			album.save()
			return redirect('interface', album_id=album.pk)
		context = {
			'form':form,
		}
		return render(request, 'create_album.html', context)


def create_song(request, album_id):
	form = SongForm(request.POST or None, request.FILES or None)
	album = get_object_or_404(Album, pk=album_id)
	if form.is_valid():
		album_songs = album.song_set.all()
		for sng in album_songs:
			if sng.name == form.cleaned_data.get("name"):
				context = {
					'album':album,
					'form':form,
					'error_message': 'Song Already Added.',
				}
				return render(request, 'create_song.html', context)
		song = form.save(commit=False)
		song.album = album
		song.audio = request.FILES['audio']
		file_type = song.audio.url.split('.')[-1]
		file_type = file_type.lower()
		if file_type not in AUDIO_FILE_TYPES:
			context = {
				'album':album,
				'form':form,
				'error_message':'Audio file is not of required format.',				
				}
			return render(request, 'create_song.html', context)

		song.save()
		return redirect('interface', album_id=album.pk)
	context = {
		'album':album,
		'form':form,
		}
	return render(request, 'create_song.html', context)

def delete_album(request, album_id):
	album = Album.objects.get(pk=album_id)
	album.delete()
	#albums = Album.objects.filter(user=request.user)
	return redirect('index')

def delete_song(request, album_id, song_id):
	album = get_object_or_404(Album, pk=album_id)
	song = Song.objects.get(pk=song_id)
	song.delete()
	return redirect('interface', album_id=album.pk)


def logout_user(request):
	logout(request)
	form = UserForm(request.POST or None)
	context = {
		'form':form
	}
	#return render(request, 'login.html', context)
	return redirect('index')

def interface(request, album_id):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		user = request.user
		album = get_object_or_404(Album, pk=album_id)
		return render(request, 'interface.html', {'album':album, 'user':user})

def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				#albums = Album.objects.filter(user=request.user)
				#return render(request, 'home.html', {'albums':albums})
				return redirect('index')
			else:
				return render(request, 'login.html', {'error_message':'Account Deactivaated'})
		else:
			return render(request, 'login.html', {'error_message':'Invalid Login'})
	return render(request, 'login.html')

def register(request):
	form = UserForm(request.POST or None)
	if form.is_valid():
		user = form.save(commit=False)
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user.set_password(password)
		user.save()
		user = authenticate(username = username, password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				albums = Album.objets.filter(user=request.user)
				return render(request, 'home.html', {'album':album})
	context = {'form':form}
	return render(request, 'register.html', context)


def songs(request, filter_by):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		try:
			song_ids = []
			for album in Album.objects.filter(user=request.user):
				for song in album.song_set.all():
					song_ids.append(song.pk)
			users_songs = Song.objects.filter(pk__in=song_ids)	
		except Album.DoesNotExist:
			users_songs = []
		return render(request, 'songs.html', {
				'song_list':users_songs,
				'filter_by':filter_by,
			})


def test(request):
	if not request.user.is_authenticated():
		return render(request, 'login.html')
	else:
		songs_are=[]
		for album in Album.objects.filter(user=request.user):
			for song in album.song_set.all():
				songs_are.append(song)

		context = {
			'songs_are':songs_are,
		}
		return render(request, 'test.html', context)