from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from pytz import utc

from funcs import backup_database

jobstores = {'default': RedisJobStore()}
executors = {'default': ThreadPoolExecutor()}

backuper = BackgroundScheduler(jobstores=jobstores, executors=executors, timezone=utc)


@backuper.scheduled_job(id='do_backup', trigger=IntervalTrigger(hours=1))
def do_backup():
    backup_database()


backuper.start()
