import csv
import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base
from src.dal import UserRepository, PlaylistRepository, SongRepository
from src.bll import SpotifyService
from src.generator import generate_spotify_csv


@pytest.fixture
def service():
    engine = create_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    user_repo = UserRepository(session)
    playlist_repo = PlaylistRepository(session)
    song_repo = SongRepository(session)

    return SpotifyService(user_repo, playlist_repo, song_repo)


def test_import_single_user(service):
    csv_path = 'data/test_spotify_data.csv'
    generate_spotify_csv(filename=csv_path, users=1, playlists=1, songs=20)

    service.import_from_csv(csv_path)
    users = service.get_all_users()

    assert len(users) == 1
    assert len(users[0].playlists) >= 1
    assert len(users[0].playlists[0].songs) >= 2

    # Перевіряємо, чи пісні імпортовані коректно
    song_titles = [song.title for song in users[0].playlists[0].songs]
    assert all(isinstance(title, str) and len(title) > 0 for title in song_titles)

    os.remove(csv_path)


def test_import_multiple_users(service):
    csv_path = 'data/test_spotify_multi.csv'
    generate_spotify_csv(filename=csv_path, users=5, playlists=20, songs=40)

    service.import_from_csv(csv_path)
    users = service.get_all_users()

    assert len(users) == 5
    for user in users:
        assert len(user.playlists) >= 2
        for playlist in user.playlists:
            assert len(playlist.songs) >= 1

    os.remove(csv_path)


def test_import_empty_csv(service):
    csv_path = 'data/empty.csv'
    os.makedirs(os.path.dirname(csv_path), exist_ok=True)
    with open(csv_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['UserId', 'Username', 'PlaylistId', 'PlaylistName', 'SongId', 'SongTitle', 'Artist'])  # headers only

    service.import_from_csv(csv_path)
    users = service.get_all_users()
    assert len(users) == 0

    os.remove(csv_path)


def test_import_invalid_file(service):
    with pytest.raises(FileNotFoundError):
        service.import_from_csv('data/non_existent_file.csv')


def test_user_playlist_song_relationship(service):
    csv_path = 'data/test_relationship.csv'
    generate_spotify_csv(filename=csv_path, users=1, playlists=1, songs=30)

    service.import_from_csv(csv_path)
    users = service.get_all_users()

    user = users[0]
    assert len(user.playlists) == 1
    playlist = user.playlists[0]
    assert len(playlist.songs) >= 2

    os.remove(csv_path)

