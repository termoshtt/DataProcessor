# -*- coding: utf-8 -*-

""" Start run in any host
"""

from . import utility
from .exception import DataProcessorError
from subprocess import check_call, CalledProcessError


class DataProcessorRunnerError(DataProcessorError):

    """ Exception about starting run """

    def __init__(self, runner, args, work_dir, host, **other_info):
        msg = "runner {} failed. args={}, work_dir={}".format(runner, args, work_dir)
        DataProcessorError.__init__(self, msg)
        self.runner = runner
        self.arguments = args
        self.work_dir = work_dir
        self.host = host
        self.info = other_info


def sync(args, work_dir, host=None):
    def _check_call(a):
        try:
            check_call(a)
        except CalledProcessError as e:
            raise DataProcessorRunnerError("sync", args, work_dir, host, exception=e)

    if host:
        args = ["ssh", host, "cd", work_dir, "&&"] + args
        _check_call(args)
    else:
        with utility.chdir(work_dir):
            _check_call(args)


runners = {
    "sync": sync,
}
