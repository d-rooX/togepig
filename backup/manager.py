import time
from loguru import logger
import os
from config import ROOT_DIR


class BackupManager:
    def __init__(self, settings):
        self.db_name = settings["db_name"]
        self.db_user = settings["db_user"]
        self.db_host = settings["db_host"]
        self.db_port = settings["db_port"]

        self._backup_path = settings["backup_path"]
        self._filename = settings["filename"]

        self._table_names = None  # None = all tables

        self.db_password = settings.get("db_password")

    @property
    def credentials(self):
        return " -h" + str(self.db_host) + " -p " + str(self.db_port) + " -d " + self.db_name + " -U " + self.db_user

    @property
    def filename(self) -> str:
        return self.filename + "-" + time.strftime("%d%m%Y%H%M%S") + ".backup"

    @filename.setter
    def filename(self, value: str):
        self._filename = value

    @property
    def backup_path(self):
        return ROOT_DIR + '/' + self._backup_path

    @backup_path.setter
    def backup_path(self, value):
        self._backup_path = value

    def backup_database(self, table_names=None):
        command_str = "pg_dump" + self.credentials

        if not os.path.exists(self.backup_path):
            os.mkdir(self.backup_path)

        if table_names is not None:
            for table in table_names:
                command_str = command_str + " -t " + table

        command_str = f'{command_str} -F c -b -v -f "{self.backup_path}/{self.filename}"'
        try:
            os.system(command_str)
            logger.info("Backup completed")
        except Exception as e:
            logger.error("Error while doing backup")
            logger.error(f'{e.__class__.__name__}: {e}')

    def restore_database(self, backup_name, table_names=None):
        command_str = "pg_restore" + self.credentials

        if table_names is not None:
            for x in table_names:
                command_str = command_str + " -t " + x

        command_str = f'command_str -v "{self.backup_path}/{backup_name}"'

        try:
            os.system(command_str)
            logger.info("Restore completed")
        except Exception as e:
            logger.error("Error while restore")
            logger.error(f'{e.__class__.__name__}: {e}')

    def get_databases(self):
        command_str = 'psql -lt' + self.credentials

        databases = []
        for row in os.popen(command_str).readlines():
            db_name = row.strip().split('|', maxsplit=1)[0].strip()
            if db_name and db_name != 'postgres' and not db_name.startswith('template'):
                databases.append(db_name)

        return databases

    def get_tables(self, db_name=None):
        command_str = 'psql -c "\dt" -t' + self.credentials
        if db_name:
            command_str += " -d " + db_name

        tables = []
        for row in os.popen(command_str).readlines():
            r = tuple(
                map(lambda x: x.strip(), row.strip().split('|'))
            )
            if len(r) == 4:
                schema, table_name, type, user = r
                if schema == 'public' and (
                        type == 'table' or
                        type == 'таблица'
                ):
                    tables.append(table_name)

        return tables

