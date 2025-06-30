# Spotify CRUD Web App

Це простий CRUD веб-додаток для управління користувачами, плейлистами та піснями у стилі Spotify. Додаток побудований на основі Flask, SQLAlchemy та Jinja2.

## 📚 Функціонал
- Управління користувачами (створення, редагування, видалення)
- Управління плейлистами користувачів
- Управління піснями у плейлистах
- Інтуїтивний веб-інтерфейс

---

## ⚙️ Технології
- Python 3
- Flask
- SQLAlchemy
- SQLite
- Jinja2 (HTML шаблони)

---

## 📂 Структура проєкту

spotify_crud/
├── src/
│ ├── app.py # Головний Flask додаток
│ ├── models.py # SQLAlchemy моделі
│ ├── dal.py # Рівень доступу до даних
│ ├── bll.py # Бізнес логіка
│ ├── templates/ # HTML шаблони
│ │ ├── index.html
│ │ ├── users.html
│ │ ├── edit_user.html
│ │ ├── playlists.html
│ │ ├── edit_playlist.html
│ │ ├── songs.html
│ │ └── edit_song.html
│ └── static/ # Статичні файли (favicon, css, тощо)
│ └── favicon.ico
├── data/
│ └── spotify_data.db # SQLite база даних
├── README.md
└── requirements.txt


---

## 🚀 Запуск проєкту

1. **Клонувати репозиторій:**
```bash
git clone https://github.com/your_username/spotify_crud.git
cd spotify_crud
```

2. **Запуск робочого середовища:**
```bash
nix-shell
```
> **Примітка!** При запуску середовища виконуються тести є ймовірність що вони видасть помилку через специфіку роботи функції генерації CSV. Спробуйте кілька разів виконати тести, ймовірність невдачі не велика.

3. **Генерація CSV файлу з даними:**
```bash
main gen-csv --verbose
```

4. **Імпортування даних з CSV файлу в базу даних:**
```bash
main import-csv --verbose
```

5. **Запуск Web-застосунка:**
```bash
flask run
```

6. **Запуск в одну команду:**
```bash
nix-shell --run "pytest ; pytest ; pytest ; python -m src.main gen_csv --verbose && python -m src.main import_csv --verbose && flask run"
```
