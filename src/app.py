from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base
from src.dal import UserRepository, PlaylistRepository, SongRepository
from src.services import SpotifyService

app = Flask(__name__)

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
    return render_template('edit_user.html')

# Редагування та видалення аналогічно

if __name__ == '__main__':
    app.run()

