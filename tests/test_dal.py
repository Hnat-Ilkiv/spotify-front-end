import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User, Playlist, Song
from src.dal import UserRepository, PlaylistRepository, SongRepository

@pytest.fixture(scope='function')
def session():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_user_repository_crud(session):
    repo = UserRepository(session)

    # Create
    user = User(username='testuser')
    repo.add_user(user)
    users = repo.get_all_users()
    assert len(users) == 1
    assert users[0].username == 'testuser'

    # Read
    fetched_user = repo.get_user_by_id(users[0].id)
    assert fetched_user.username == 'testuser'

    # Update
    repo.update_user(fetched_user.id, 'updateduser')
    updated_user = repo.get_user_by_id(fetched_user.id)
    assert updated_user.username == 'updateduser'

    # Delete
    repo.delete_user(fetched_user.id)
    assert repo.get_user_by_id(fetched_user.id) is None
    assert repo.get_all_users() == []

def test_playlist_repository_crud(session):
    user_repo = UserRepository(session)
    playlist_repo = PlaylistRepository(session)

    # Створюємо користувача для плейліста
    user = User(username='playlistuser')
    user_repo.add_user(user)

    # Create
    playlist = Playlist(name='My Playlist', user=user)
    playlist_repo.add_playlist(playlist)
    playlists = playlist_repo.get_all_playlists_by_user_id(user.id)
    assert len(playlists) == 1
    assert playlists[0].name == 'My Playlist'

    # Read
    fetched_playlist = playlist_repo.get_playlist_by_id(playlists[0].id)
    assert fetched_playlist.name == 'My Playlist'

    # Update
    playlist_repo.update_playlist(fetched_playlist.id, 'Updated Playlist')
    updated_playlist = playlist_repo.get_playlist_by_id(fetched_playlist.id)
    assert updated_playlist.name == 'Updated Playlist'

    # Delete
    playlist_repo.delete_playlist(fetched_playlist.id)
    assert playlist_repo.get_playlist_by_id(fetched_playlist.id) is None
    assert playlist_repo.get_all_playlists_by_user_id(user.id) == []

def test_song_repository_crud(session):
    song_repo = SongRepository(session)

    # Create
    song = Song(title='Test Song', artist='Test Artist')
    song_repo.add_song(song)
    songs = song_repo.get_all_songs()
    assert len(songs) == 1
    assert songs[0].title == 'Test Song'
    assert songs[0].artist == 'Test Artist'

    # Read
    fetched_song = song_repo.get_song_by_id(songs[0].id)
    assert fetched_song.title == 'Test Song'
    assert fetched_song.artist == 'Test Artist'

    # Update
    song_repo.update_song(fetched_song.id, 'Updated Song')
    updated_song = song_repo.get_song_by_id(fetched_song.id)
    assert updated_song.title == 'Updated Song'

    # Delete
    song_repo.delete_song(fetched_song.id)
    assert song_repo.get_song_by_id(fetched_song.id) is None
    assert song_repo.get_all_songs() == []

def test_add_song_to_playlist(session):
    user_repo = UserRepository(session)
    playlist_repo = PlaylistRepository(session)
    song_repo = SongRepository(session)

    # Створюємо користувача
    user = User(username='musiclover')
    user_repo.add_user(user)

    # Створюємо плейліст
    playlist = Playlist(name='Chill', user=user)
    playlist_repo.add_playlist(playlist)

    # Створюємо пісню
    song = Song(title='Relaxing Tune', artist='Chil Cat')
    song_repo.add_song(song)

    # Додаємо пісню до плейліста
    playlist_repo.add_song_to_playlist(playlist, song)

    # Перевіряємо, що пісня додана до плейліста
    fetched_playlist = playlist_repo.get_playlist_by_id(playlist.id)
    assert len(fetched_playlist.songs) == 1
    assert fetched_playlist.songs[0].title == 'Relaxing Tune'
    assert fetched_playlist.songs[0].artist == 'Chil Cat'

    # Перевіряємо отримання всіх пісень в плейлісті
    songs_in_playlist = song_repo.get_all_songs_by_playlist_id(playlist.id)
    assert len(songs_in_playlist) == 1
    assert songs_in_playlist[0].title == 'Relaxing Tune'

