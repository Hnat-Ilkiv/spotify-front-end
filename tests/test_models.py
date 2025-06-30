import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base, User, Playlist, Song

@pytest.fixture
def session():
    # Створюємо тимчасову базу в пам'яті
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()

def test_create_user(session):
    user = User(username='test_user')
    session.add(user)
    session.commit()

    assert session.query(User).count() == 1
    assert session.query(User).first().username == 'test_user'

def test_create_song_without_playlist(session):
    song = Song(title='Song A', artist='Artist A')
    session.add(song)
    session.commit()

    assert session.query(Song).count() == 1
    assert session.query(Song).first().title == 'Song A'

def test_add_songs_to_playlist(session):
    user = User(username='playlist_owner')
    session.add(user)
    session.commit()

    playlist = Playlist(name='Test Playlist', user=user, user_id=user.id)
    song1 = Song(title='Song 1', artist='Artist 1')
    song2 = Song(title='Song 2', artist='Artist 2')

    playlist.songs.append(song1)
    playlist.songs.append(song2)

    session.add(playlist)
    session.commit()

    # Перевіряємо, що плейлист має дві пісні
    playlist_from_db = session.query(Playlist).first()
    assert len(playlist_from_db.songs) == 2

    titles = {song.title for song in playlist_from_db.songs}
    assert 'Song 1' in titles
    assert 'Song 2' in titles
    assert len(titles) == 2

def test_song_can_exist_in_multiple_playlists(session):
    user = User(username='multi_playlist_user')
    session.add(user)
    session.commit()

    playlist1 = Playlist(name='Playlist 1', user=user, user_id=user.id)
    playlist2 = Playlist(name='Playlist 2', user=user, user_id=user.id)
    song = Song(title='Common Song', artist='Artist X')

    playlist1.songs.append(song)
    playlist2.songs.append(song)

    session.add_all([playlist1, playlist2])
    session.commit()

    playlists = session.query(Playlist).all()
    assert len(playlists) == 2

    # Перевіряємо, що пісня присутня в обох плейлистах
    assert song in playlists[0].songs
    assert song in playlists[1].songs

