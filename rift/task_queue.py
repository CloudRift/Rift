from celery import Celery

from rift.config import get_config

conf = get_config()

celery = Celery('cloudrift')

#load celery configurations from rift config and apply them
celery.conf.BROKER_URL = conf.celery.BROKER_URL
celery.conf.CELERYD_CONCURRENCY = conf.celery.CELERYD_CONCURRENCY
celery.conf.CELERY_TASK_SERIALIZER = conf.celery.CELERY_TASK_SERIALIZER
celery.conf.CELERYD_HIJACK_ROOT_LOGGER = conf.celery.CELERYD_HIJACK_ROOT_LOGGER