from celery import Celery

from rift.config import get_config

conf = get_config()

celery = Celery('cloudrift')

#load celery configurations from rift config and apply them
celery.conf.broker_url = conf.celery.broker_url
celery.conf.celeryd_concurrency = conf.celery.celeryd_concurrency
celery.conf.celery_task_serializer = conf.celery.celery_task_serializer
celery.conf.celeryd_hijack_root_logger = conf.celery.celeryd_hijack_root_logger
