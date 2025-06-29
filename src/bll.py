import csv
import time
from src.models import User, Playlist, Song
from src.dal import IUserRepository, IPlaylistRepository, ISongRepository
from abc import ABC, abstractmethod
from src.progress_bar import print_progress_bar
from src.file_size import lines_in_csv, file_size

class ISpotifyService(ABC):
    @abstractmethod
    def import_from_csv(self, csv_path: str):
        pass

    @abstractmethod
    def list_users(self):
        pass

class SpotifyService(ISpotifyService):
    def __init__(self, user_repo: IUserRepository, playlist_repo: IPlaylistRepository, song_repo: ISongRepository):
        self.user_repo = user_repo
        self.playlist_repo = playlist_repo
        self.song_repo = song_repo

    def import_from_csv(self, csv_path: str = 'data/spotify_data.csv', db_path: str = 'data/spoty_data.csv', verbose=False):
        progress_now = 0
        total_progress = lines_in_csv(csv_path) - 1
        update_progress = max(1, total_progress // 1000)
        start_time = time.time()

        # Initial call to print 0% progress
        if verbose : print_progress_bar(0, total_progress, prefix = '- Progress', suffix = 'Complere', length = 50)

        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            user_ids = {}
            playlist_ids = {}
            song_ids = {}

            for row in reader:
                progress_now += 1

                user_id = row['UserId']
                username = row['Username']
                playlist_id = row['PlaylistId']
                playlist_name = row['PlaylistName']
                song_id = row['SongId']
                song_title = row['SongTitle']
                song_artist = row['Artist']

                if user_id not in user_ids:
                    user = User(username=username, id=user_id)
                    self.user_repo.add_user(user)
                    user_ids[user_id] = user
                else:
                    user = user_ids[user_id]

                if playlist_id not in playlist_ids:
                    playlist = Playlist(name=playlist_name, user=user, id=playlist_id)
                    self.playlist_repo.add_playlist(playlist)
                    playlist_ids[playlist_id] = playlist
                else:
                    playlist = playlist_ids[playlist_id]

                if song_id not in song_ids:
                    song = Song(title=song_title, artist=song_artist, id=song_id)
                    self.song_repo.add_song(song)
                    song_ids[song_id] = song
                else:
                    song = song_ids[song_id]
                
                playlist.songs.append(song)

                # Update Progress Bar
                if verbose and (progress_now % update_progress == 0):
                    print_progress_bar(
                            progress_now, 
                            total_progress, 
                            prefix = '- Progress', 
                            suffix = 'Complere', 
                            length = 50
                        )

            if verbose: 
                print_progress_bar(progress_now, total_progress, prefix = '- Progress', suffix = 'Complere', length = 50)

            end_time = time.time()
            str_time = time.strftime("%H:%M:%S",time.gmtime(end_time - start_time))
            
            if verbose:
                print(f"Result CSV file import:")
                print(f"- Users:          {len(user_ids)}")
                print(f"- Playlists:      {len(playlist_ids)}")
                print(f"- Songs:          {len(song_ids)}")
                print(f"- DB size:        {file_size(db_path)}")
                print(f"- Importing time: {str_time}")

    def list_users(self):
        return self.user_repo.get_all_users()

