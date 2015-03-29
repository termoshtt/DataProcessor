# -*- coding: utf-8 -*-

from .. import pipe
from subprocess import check_call


@pipe.type("run")
def sync(node):
    if "host" not in node or "work_dir" not in node:
        return node
    host = node["host"]
    wpath = node["work_dir"]
    path = node["path"]
    check_call(["rsync", "-auv", "{host}:{wpath}/".format(host=host, wpath=wpath), path])
    return node


def register(pipe_dics):
    pipe_dics["sync"] = {
        "func": sync,
        "args": [],
        "desc": "Sync results in remote hosts",
    }
