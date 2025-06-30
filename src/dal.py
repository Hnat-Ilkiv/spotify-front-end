from typing import Union
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from src.models import User, Playlist, Song

# Абстрактні інтерфейси
class IUserRepository(ABC):
    @abstractmethod
    def add_user(self, user_or_username: Union[User, str]):
        pass

    @abstractmethod
    def get_all_users(self):
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: str):
        pass

    @abstractmethod
    def update_user(self, user_id: str):
        pass

    @abstractmethod
    def delete_user(self, user_id: str):
        pass


class IPlaylistRepository(ABC):
    @abstractmethod
    def add_playlist(self, playlist_or_playlistname: Union[Playlist, str], user_id: str):
        pass

    @abstractmethod
    def add_song_to_playlist(self, playlist: Playlist, song: Song):
        pass

    @abstractmethod
    def get_all_playlists_by_user_id(self, user_id: str):
        pass

    @abstractmethod
    def get_playlist_by_id(self, playlist_id: str):
        pass

    @abstractmethod
    def update_playlist(self, playlist_id: str):
        pass

    @abstractmethod
    def delete_playlist(self, playlist_id: str):
        pass



class ISongRepository(ABC):
    @abstractmethod
    def add_song(self, song: Song):
        pass

    @abstractmethod
    def get_song_by_id(self, song_id: str):
        pass

    @abstractmethod
    def get_all_songs_by_playlist_id(self, playlist_id: str):
        pass

    @abstractmethod
    def get_all_songs(self):
        pass

    @abstractmethod
    def update_song(self, song_id: str):
        pass

    @abstractmethod
    def delete_song(self, song_id: str):
        pass

# Реалізація DAL через SQLAlchemy
class UserRepository(IUserRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_user(self, user_or_username: Union[User, str]):
        if isinstance(user_or_username, User):
            user = user_or_username
        elif isinstance(user_or_username, str):
            user = User(username=user_or_username)
        else:
            raise ValueError('Invalid type for add_user: expected User or str')

        self.session.add(user)
        self.session.commit()

    def get_all_users(self):
        return self.session.query(User).all()

    def get_user_by_id(self, user_id: str):
        return self.session.query(User).filter_by(id=user_id).first()

    def update_user(self, user_id: str, new_username: str):
        user = self.get_user_by_id(user_id)
        if user:
            user.username = new_username
            self.session.commit()
        return user

    def delete_user(self, user_id: str):
        user = self.get_user_by_id(user_id)
        if user:
            self.session.delete(user)
            self.session.commit()
        return user

class PlaylistRepository(IPlaylistRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_playlist(self, playlist_or_playlistname: Union[Playlist, str], user_id: str):
        if isinstance(playlist_or_playlistname, Playlist):
            playlist = playlist_or_playlistname
        elif isinstance(playlist_or_playlistname, str):
            playlist = Playlist(name=playlist_or_playlistname, user_id=user_id)
        else:
            raise ValueError('Invalid type for add_playlist: expected Playlist or str')

        self.session.add(playlist)
        self.session.commit()

    def add_song_to_playlist(self, playlist: Playlist, song: Song):
        playlist.songs.append(song)
        self.session.commit()

    def get_all_playlists_by_user_id(self, user_id: str):
        return self.session.query(Playlist).filter_by(user_id=user_id).all()

    def get_playlist_by_id(self, playlist_id: str):
        return self.session.query(Playlist).filter_by(id=playlist_id).first()

    def update_playlist(self, playlist_id: str, new_name: str):
        playlist = self.get_playlist_by_id(playlist_id)
        if playlist:
            playlist.name = new_name
            self.session.commit()
        return playlist

    def delete_playlist(self, playlist_id: str):
        playlist = self.get_playlist_by_id(playlist_id)
        if playlist:
            self.session.delete(playlist)
            self.session.commit()
        return playlist


class SongRepository(ISongRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_song(self, song: Song):
        self.session.add(song)
        self.session.commit()

    def get_song_by_id(self, song_id: str):
        return self.session.query(Song).filter_by(id=song_id).first()

    def get_all_songs_by_playlist_id(self, playlist_id: str):
        playlist = self.session.query(Playlist).filter_by(id=playlist_id).first()
        if playlist:
            return playlist.songs
        return []

    def get_all_songs(self):
        return self.session.query(Song).all()

    def update_song(self, song_id: str, new_title: str, new_artist: str):
        song = self.get_song_by_id(song_id)
        if song:
            song.title = new_title
            song.artist = new_artist
            self.session.commit()
        return song

    def delete_song(self, song_id: str):
        song = self.get_song_by_id(song_id)
        if song:
            self.session.delete(song)
            self.session.commit()
        return song

