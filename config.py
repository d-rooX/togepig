import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SETTINGS = {
    "db_name": "test",
    "db_user": "postgres",
    "db_password": "qwerty",
    "db_host": "localhost",
    "db_port": 5432,
    "backup_path": "backup_files",
    "filename": "testback"
}
