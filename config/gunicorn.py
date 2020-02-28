import logging
import multiprocessing
import os

from config.settings import ALLOWED_HOSTS, DEBUG
from gevent import monkey
from psycogreen.gevent import patch_psycopg

bind = ":8000"
worker_class = "gevent"
if "WEB_CONCURRENCY" in os.environ:
    workers = int(os.getenv("WEB_CONCURRENCY"))
else:
    workers = multiprocessing.cpu_count() * 2 + 1


def on_starting(server):
    logger = logging.getLogger(__name__)
    if DEBUG:
        logger.warning("Running in DEBUG mode")
    if "*" in ALLOWED_HOSTS:
        logger.warning("Host checking is disabled (ALLOWED_HOSTS is set to accept all)")


def post_fork(server, worker):
    monkey.patch_all()
    patch_psycopg()
