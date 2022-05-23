import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = {
    "db_user": "postgres",
    # "db_password": "qwerty",
    "db_host": "localhost",
    "db_port": 5432,
    # ________________
    "db_name": "test",
    "backup_path": "backup_files",
    "filename": "testback"
}
TOKEN = "123:123"
