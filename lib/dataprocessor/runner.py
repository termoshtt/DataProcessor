# -*- coding: utf-8 -*-

""" Start run in any host
"""

from . import utility
from .exception import DataProcessorError

import functools
from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)


class DataProcessorRunnerError(DataProcessorError):

    """ Exception about starting run """

    def __init__(self, runner, args, work_dir, host, exception):
        msg = "runner {} failed. args={}, work_dir={}".format(runner, args, work_dir)
        DataProcessorError.__init__(self, msg)
        self.runner = runner
        self.arguments = args
        self.work_dir = work_dir
        self.host = host
        self.exception = exception


runners = {}


def runner(func):
    @functools.wraps(func)
    def wrapper(args, work_dir, host=None):
        try:
            func(args, work_dir, host)
        except Exception as e:
            logger.error(str(e))
            raise DataProcessorRunnerError(func.__name__, args, work_dir, host)
    runners[func.__name__] = wrapper
    return wrapper


@runner
def echo(args, work_dir, host=None):
    """ echo infomations, and not start run (start manually) """
    if host:
        print("{}:{}".format(host, work_dir))
    else:
        print(work_dir)


@runner
def sync_local(args, work_dir, host=None):
    """ execute command in localhost """
    if host:
        logger.info("Command is executed not in '{}' but in localhost".format(host))
    with utility.chdir(work_dir):
        utility.check_call(args)


@runner
def sync_remote(args, work_dir, host=None):
    """ execute command in remote host """
    if not host:
        logger.error("sync_remote must be called with valid hostname (host={})".format(host))
        raise DataProcessorError("sync_remote is called with invalid hostname")
    args = ["ssh", host, "cd", work_dir, "&&"] + args
    utility.check_call(args)


@runner
def sync(args, work_dir, host=None):
    """ execute command in local or remote host """
    if host:
        sync_remote(args, work_dir, host)
    else:
        sync_local(args, work_dir, host)
