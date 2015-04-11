# coding: utf-8

from .. import starter, utility, runner


def start(node_list, args, requirements=[],
          name=utility.now_str(), projects=[],
          runner="sync", host=None):
    starter.start(node_list, args, requirements, name, projects, runner, host)
    return node_list


def register(pipes_dics):
    pipes_dics["start_run"] = {
        "func": start,
        "args": [("args", {"nargs": "+", "help": "arguments to execute"})],
        "kwds": [
            ("requirements", {"nargs": "+", "help": "section parameters are written"}),
            ("name", {"help": "name of new run"}),
            ("projects", {"nargs": "+", "help": "projects of new run"}),
            ("runner", {"choices": runner.runners, "help": "runner"}),
            ("host", {"help": "host in which run is executed"}),
        ],
        "desc": "Start new run",
    }
