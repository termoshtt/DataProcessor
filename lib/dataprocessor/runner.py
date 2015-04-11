# -*- coding: utf-8 -*-

""" Start run in any host
"""

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
    args = ["cd", work_dir, "&&"] + args
    if host:
        args = ["ssh", host] + args
    try:
        check_call(args)
    except CalledProcessError as e:
        raise DataProcessorRunnerError("sync", args, work_dir, host, exception=e)


runners = {
    "sync": sync,
}
