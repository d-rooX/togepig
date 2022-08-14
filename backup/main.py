from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc
from backup.manager import BackupManager
from config import SETTINGS
from settings import backup_databases, interval

# jobstores = {'default': RedisJobStore()}
# executors = {'default': ThreadPoolExecutor()}

backup_scheduler = BackgroundScheduler(timezone=utc) #jobstores=jobstores, executors=executors, timezone=utc)
backup_manager = BackupManager(SETTINGS)


@backup_scheduler.scheduled_job(id='do_backup', trigger=IntervalTrigger(hours=interval))
def do_backup():
    backup_manager.backup_database(backup_databases)


backup_scheduler.start()
