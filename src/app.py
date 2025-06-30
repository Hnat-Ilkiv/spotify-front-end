from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.dal import UserRepository, PlaylistRepository, SongRepository
from src.bll import SpotifyService

app = Flask(__name__, static_folder='../static')

# Налаштування БД
engine = create_engine('sqlite:///data/spotify_data.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Репозиторії та сервіс
user_repo = UserRepository(session)
playlist_repo = PlaylistRepository(session)
song_repo = SongRepository(session)
spotify_service = SpotifyService(user_repo, playlist_repo, song_repo)


# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

# Список користувачів
@app.route('/users')
def list_users():
    users = spotify_service.get_all_users()
    return render_template('users.html', users=users)

# Додати користувача
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        spotify_service.add_user(username)
        return redirect(url_for('list_users'))
    return render_template('edit_user.html', user=None)

# Редагувати користувача
@app.route('/users/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = spotify_service.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        new_username = request.form['username']
        spotify_service.update_user(user_id, new_username)
        return redirect(url_for('list_users'))

    return render_template('edit_user.html', user=user)

# Видалити користувача
@app.route('/users/delete/<user_id>', methods=['POST'])
def delete_user(user_id):
    spotify_service.delete_user(user_id)
    return redirect(url_for('list_users'))

# Список плейлистів користувача
@app.route('/users/<user_id>/playlists')
def list_playlists(user_id):
    user = spotify_service.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    playlists = spotify_service.get_all_playlists_by_user_id(user_id)
    return render_template('playlists.html', user=user, playlists=playlists)

# Додати плейлист
@app.route('/users/<user_id>/playlists/add', methods=['GET', 'POST'])
def add_playlist(user_id):
    user = spotify_service.get_user_by_id(user_id)
    if not user:
        return "User not found", 404

    if request.method == 'POST':
        playlist_name = request.form['name']
        spotify_service.add_playlist(user_id, playlist_name)
        return redirect(url_for('list_playlists', user_id=user_id))

    return render_template('edit_playlist.html', user=user, playlist=None)

# Редагувати плейлист
@app.route('/playlists/edit/<playlist_id>', methods=['GET', 'POST'])
def edit_playlist(playlist_id):
    playlist = spotify_service.get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    if request.method == 'POST':
        new_name = request.form['name']
        spotify_service.update_playlist(playlist_id, new_name)
        return redirect(url_for('list_playlists', user_id=playlist.user_id))

    return render_template('edit_playlist.html', user=playlist.user, playlist=playlist)

# Видалити плейлист
@app.route('/playlists/delete/<playlist_id>', methods=['POST'])
def delete_playlist(playlist_id):
    playlist = spotify_service.get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    user_id = playlist.user_id
    spotify_service.delete_playlist(playlist_id)
    return redirect(url_for('list_playlists', user_id=user_id))

# Список пісень у плейлисті
@app.route('/playlists/<playlist_id>/songs')
def list_songs(playlist_id):
    playlist = spotify_service.get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    songs = spotify_service.get_all_songs_by_playlist_id(playlist_id)
    return render_template('songs.html', playlist=playlist, songs=songs)

# Додати пісню
@app.route('/playlists/<playlist_id>/songs/add', methods=['GET', 'POST'])
def add_song(playlist_id):
    playlist = spotify_service.get_playlist_by_id(playlist_id)
    if not playlist:
        return "Playlist not found", 404

    if request.method == 'POST':
        title = request.form['title']
        artist = request.form['artist']
        spotify_service.add_song_to_playlist(playlist_id, title, artist)
        return redirect(url_for('list_songs', playlist_id=playlist_id))

    return render_template('edit_song.html', playlist=playlist, song=None)

# Редагувати пісню
@app.route('/songs/edit/<song_id>', methods=['GET', 'POST'])
def edit_song(song_id):
    song = spotify_service.get_song_by_id(song_id)
    if not song:
        return "Song not found", 404

    if request.method == 'POST':
        new_title = request.form['title']
        new_artist = request.form['artist']
        spotify_service.update_song(song_id, new_title, new_artist)
        return redirect(url_for('list_songs', playlist_id=song.playlists[0].id))

    return render_template('edit_song.html', playlist=song.playlists[0], song=song)

# Видалити пісню
@app.route('/songs/delete/<song_id>', methods=['POST'])
def delete_song(song_id):
    song = spotify_service.get_song_by_id(song_id)
    if not song:
        return "Song not found", 404

    playlist_id = song.playlists[0].id
    spotify_service.delete_song(song_id)
    return redirect(url_for('list_songs', playlist_id=playlist_id))

if __name__ == '__main__':
    app.run()

