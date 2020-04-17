import logging

from config.settings import ALLOWED_HOSTS, DEBUG, LOGGING, WEB_CONCURRENCY
from gevent import monkey
from psycogreen.gevent import patch_psycopg

bind = ":8000"
worker_class = "gevent"
workers = WEB_CONCURRENCY
logconfig_dict = LOGGING
access_log_format = '"%(r)s" %(s)s %(b)s'


def on_starting(server):
    logger = logging.getLogger(__name__)
    if DEBUG:
        logger.warning("Running in DEBUG mode")
    if "*" in ALLOWED_HOSTS:
        logger.warning("Host checking is disabled (ALLOWED_HOSTS is set to accept all)")


def post_fork(server, worker):
    monkey.patch_all()
    patch_psycopg()
