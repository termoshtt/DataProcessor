# -*- coding: utf-8 -*-

""" Start run in any host
"""

from .exception import DataProcessorError
from .utility import chdir
from subprocess import check_call, CalledProcessError


class DataProcessorRunnerError(DataProcessorError):

    """ Exception about starting run """

    def __init__(self, runner, args, work_dir, **other_info):
        msg = "runner {} failed. args={}, work_dir={}".format(runner, args, work_dir)
        DataProcessorError.__init__(self, msg)
        self.runner = runner
        self.args = args
        self.work_dir = work_dir
        self.info = other_info


def sync(args, work_dir, host=None):
    if host:
        raise NotImplementedError("Cannot start in another host in this version")
    with chdir(work_dir):
        try:
            check_call(args)
        except CalledProcessError as e:
            raise DataProcessorRunnerError("sync", args, work_dir, exception=e)


runners = {
    "sync": sync,
}
