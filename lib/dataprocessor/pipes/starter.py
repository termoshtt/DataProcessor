# coding: utf-8

from .. import starter, utility, pipe
from ..runner import runners


def start(node_list, args, requirements=[],
          name=utility.now_str(), projects=[],
          runner="sync", host=None):
    starter.start(node_list, args, requirements, name, projects, runner, host)
    return node_list


def dispatch(node_list, host, args, requirements=[],
             name=utility.now_str(), projects=[]):
    runner = "sync_local"
    starter.start(node_list, args, requirements, name, projects, runner, host)
    return node_list


@pipe.type("run")
def fetch(node):
    if "host" not in node or "work_dir" not in node:
        return node
    host = node["host"]
    wpath = node["work_dir"]
    path = node["path"]
    utility.check_call(["rsync", "-auv", "{host}:{wpath}/".format(host=host, wpath=wpath), path])
    return node


def register(pipes_dics):
    args = ("args", {
        "nargs": "+",
        "help": "arguments to execute"
    })
    requirements = ("requirements", {
        "nargs": "+",
        "help": "section parameters are written"
    })
    name = ("name", {
        "help": "name of new run"
    })
    projects = ("projects", {
        "nargs": "+",
        "help": "projects of new run"
    })
    runner = ("runner", {
        "choices": runners,
        "help": "runner"
    })
    host = ("host", {
        "help": "host in which run is executed"
    })

    pipes_dics["starter"] = {
        "func": start,
        "args": [args],
        "kwds": [requirements, name, projects, runner, host],
        "desc": "Start new run",
    }

    pipes_dics["dispatch"] = {
        "func": start,
        "args": [host, args],
        "kwds": [requirements, name, projects],
        "desc": "Start new run in remote host",
    }
    pipes_dics["fetch"] = {
        "func": fetch,
        "args": [],
        "kwds": [],
        "desc": "Fetch results of dispatched runs"
    }
