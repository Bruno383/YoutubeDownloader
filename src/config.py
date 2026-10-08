import os


# Pasta principal do projeto
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


# Pastas de download
DOWNLOADS_DIR = os.path.join(
    BASE_DIR,
    "downloads"
)


MP4_DIR = os.path.join(
    DOWNLOADS_DIR,
    "mp4"
)


MP3_DIR = os.path.join(
    DOWNLOADS_DIR,
    "mp3"
)


# Criar pastas automaticamente
os.makedirs(MP4_DIR, exist_ok=True)
os.makedirs(MP3_DIR, exist_ok=True)