import time
from loguru import logger
import os
from config import SETTINGS, ROOT_DIR


def create_essentials():
    db_name = SETTINGS["db_name"]
    db_user = SETTINGS["db_user"]
    db_password = SETTINGS["db_password"]
    db_host = SETTINGS["db_host"]
    db_port = SETTINGS["db_port"]

    backup_path = SETTINGS["backup_path"]
    filename = SETTINGS["filename"]
    filename = filename + "-" + time.strftime("%d%m%Y%H%M%S") + ".backup"

    command_str = str(db_host) + " -p " + str(db_port) + " -d " + db_name + " -U " + db_user
    return command_str, backup_path, filename


def backup_database(table_names=None):
    command_str, backup_path, filename = create_essentials()
    command_str = "pg_dump -h " + command_str
    backup_path = ROOT_DIR + '/' + backup_path

    if not os.path.exists(backup_path):
        os.mkdir(backup_path)

    if table_names is not None:
        for x in table_names:
            command_str = command_str + " -t " + x

    command_str = command_str + " -F c -b -v -f '" + backup_path + "/" + filename + "'"
    try:
        os.system(command_str)
        logger.info("Backup completed")
    except Exception as e:
        logger.error("Error while doing backup")
        logger.error(f'{e.__class__.__name__}: {e}')


def restore_database(backup_name, table_names=None):
    command_str, backup_path, filename = create_essentials()
    command_str = "pg_restore -h " + command_str
    backup_path = ROOT_DIR + '/' + backup_path

    if table_names is not None:
        for x in table_names:
            command_str = command_str + " -t " + x

    command_str = command_str + " -v '" + backup_path + "/" + backup_name + "'"

    try:
        os.system(command_str)
        logger.info("Restore completed")
    except Exception as e:
        logger.error("Error while restore")
        logger.error(f'{e.__class__.__name__}: {e}')

