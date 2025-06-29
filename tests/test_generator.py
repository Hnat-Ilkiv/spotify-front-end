import os
import csv
import pytest
from src.generator import generate_spotify_csv

@pytest.fixture
def test_file_path():
    return 'data/test_spotify_data.csv'

def test_csv_file_is_created(test_file_path):
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    rows_written = generate_spotify_csv(filename=test_file_path, users=5, playlists=2, songs=2, verbose=False)

    assert os.path.exists(test_file_path), "CSV файл не створено."
    assert rows_written > 1, "CSV файл повинен мати хоча б заголовок і один запис."

    os.remove(test_file_path)

def test_csv_header_correct(test_file_path):
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    generate_spotify_csv(filename=test_file_path, users=1, playlists=1, songs=1, verbose=False)

    with open(test_file_path, newline='') as file:
        reader = csv.reader(file)
        header = next(reader)
        assert header == ['UserId', 'Username', 'PlaylistId', 'PlaylistName', 'SongId', 'SongTitle', 'Artist'], "Заголовок неправильний."

    os.remove(test_file_path)

def test_csv_contains_expected_number_of_rows(test_file_path):
    if os.path.exists(test_file_path):
        os.remove(test_file_path)

    users = 3
    playlists = 1
    songs = 1

    rows_written = generate_spotify_csv(filename=test_file_path, users=users, playlists=playlists, songs=songs, verbose=False)

    with open(test_file_path, newline='') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # Перевіряємо, що кількість рядків, записаних у файл, дорівнює кількості рядків, які повертає функція
    assert len(lines) == rows_written, "Кількість рядків у файлі не збігається з поверненим значенням."

    os.remove(test_file_path)

def test_csv_file_is_overwritten(test_file_path):
    # Створюємо перший файл
    generate_spotify_csv(filename=test_file_path, users=1, playlists=1, songs=1, verbose=False)

    with open(test_file_path, newline='') as file:
        reader = csv.reader(file)
        initial_lines = list(reader)

    # Створюємо другий файл з іншою кількістю користувачів
    generate_spotify_csv(filename=test_file_path, users=3, playlists=1, songs=1, verbose=False)

    with open(test_file_path, newline='') as file:
        reader = csv.reader(file)
        new_lines = list(reader)

    assert len(new_lines) > len(initial_lines), "Файл не було перезаписано з новими даними."

    os.remove(test_file_path)

