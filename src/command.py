import argparse
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models import Base, User, Playlist, Song
from src.dal import UserRepository, PlaylistRepository, SongRepository
from src.bll import SpotifyService
from src.generator import generate_spotify_csv

def create_database(db_path: str):
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.drop_all(engine)  # Якщо існує — видаляємо всі таблиці
    Base.metadata.create_all(engine)  # Створюємо нові таблиці
    return engine

def generate_csv_command(args):
    print(f"CSV file generation started.")
    if args.s and not (args.m or args.l):
        generate_spotify_csv(
                filename = args.path, 
                users = 10 if not args.users else args.users, 
                playlists = 10 if not args.playlists else args.playlists, 
                songs = 10 if not args.songs else args.songs, 
                verbose = args.verbose
            )
    elif args.m and not (args.s or args.l):
        generate_spotify_csv(
                filename = args.path, 
                users = 100 if not args.users else args.users, 
                playlists = 100 if not args.playlists else args.playlists, 
                songs = 100 if not args.songs else args.songs, 
                verbose = args.verbose
            )
    elif args.l and not (args.s or args.m):
        generate_spotify_csv(
                filename = args.path, 
                users = 1000 if not args.users else args.users, 
                playlists = 1000 if not args.playlists else args.playlists, 
                songs = 1000 if not args.songs else args.songs, 
                verbose = args.verbose
            )
    else:
        generate_spotify_csv(
                filename = args.path, 
                users = 10 if not args.users else args.users, 
                playlists = 20 if not args.playlists else args.playlists, 
                songs = 20 if not args.songs else args.songs, 
                verbose = args.verbose
            )
    print(f"CSV file generated successfully.")

def import_csv_command(args):
    print(f"Starting import from CSV: {args.path_csv}")

    if os.path.exists(args.path_db):
        os.remove(args.path_db)
        if args.verbose:
            print(f"Existing database {args.path_db} removed.")

    engine = create_database(args.path_db)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Створюємо репозиторії
    user_repo = UserRepository(session)
    playlist_repo = PlaylistRepository(session)
    song_repo = SongRepository(session)

    # Створюємо сервіс
    service = SpotifyService(user_repo, playlist_repo, song_repo)

    # Імпортуємо CSV
    service.import_from_csv(args.path_csv, args.path_db, args.verbose)

    print(f"Import completed successfully into database: {args.path_db}")
