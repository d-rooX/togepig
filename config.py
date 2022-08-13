import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = {
    "db_user": "postgres",
    "db_password": "postgres",
    "db_host": "localhost",
    "db_port": 5432,
    "backup_path": "backup_files",
    "filename": "testback"
}
TOKEN = os.environ.get('BOT_TOKEN')
