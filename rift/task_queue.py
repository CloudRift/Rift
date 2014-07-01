from celery import Celery

from rift.config import get_config

conf = get_config()

celery = Celery('cloudrift')

# load celery configurations from rift config and apply them
celery.conf.BROKER_URL = conf.celery.broker_url
celery.conf.CELERYD_CONCURRENCY = conf.celery.celeryd_concurrency
celery.conf.CELERY_TASK_SERIALIZER = conf.celery.celery_task_serializer
celery.conf.CELERYD_HIJACK_ROOT_LOGGER = conf.celery.celeryd_hijack_root_logger
