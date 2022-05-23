from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc
from backup.manager import BackupManager
from config import SETTINGS

jobstores = {'default': RedisJobStore()}
executors = {'default': ThreadPoolExecutor()}

backup_scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=utc)
backup_manager = BackupManager(SETTINGS)


@backup_scheduler.scheduled_job(id='do_backup', trigger=IntervalTrigger(hours=6))
def do_backup():
    backup_manager.backup_database()


backup_scheduler.start()
