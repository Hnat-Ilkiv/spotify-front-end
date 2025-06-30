import uuid
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

playlist_song = Table(
    'playlist_song',
    Base.metadata,
    Column('playlist_id', String, ForeignKey('playlists.id'), primary_key=True),
    Column('song_id', String, ForeignKey('songs.id'), primary_key=True)
)

class User(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)

    playlists = relationship('Playlist', back_populates='user', cascade="all, delete-orphan")

    def __init__(self, username, id=None):
        self.username = username
        if id:
            self.id = id

    def __repr__(self):
        return f"User(id={self.id}, username='{self.username}')"

class Playlist(Base):
    __tablename__ = 'playlists'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    user_id = Column(String, ForeignKey('users.id'))

    user = relationship('User', back_populates='playlists')
    
    songs = relationship('Song', secondary=playlist_song, back_populates='playlists')

    def __init__(self, name: str, user: User, user_id: str, id=None):
        self.name = name
        self.user_id = user_id
        self.user = user
        if id:
            self.id = id

    def __repr__(self):
        return f"Playlist(id={self.id}, name='{self.name}', user_id={self.user_id})"

class Song(Base):
    __tablename__ = 'songs'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)

    playlists = relationship('Playlist', secondary=playlist_song, back_populates='songs')

    def __init__(self, title, artist, playlists=None, id=None):
        self.title = title
        self.artist = artist
        if playlists:
            self.playlists = playlists
        if id:
            self.id = id

    def __repr__(self):
        return f"Song(id={self.id}, title='{self.title}', artist='{self.artist}')"

