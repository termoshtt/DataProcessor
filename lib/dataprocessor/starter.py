# -*- coding: utf-8 -*-


from . import utility, basket, nodes
from .runner import runners
from .exception import DataProcessorError as dpError
import os.path
import shutil


def copy_requirements(path, requirements, host=None):
    if host:
        raise NotImplementedError("Cannot copy into another hosts")
    for req in requirements:
        utility.check_file(req)
        shutil.copy2(req, path)


def start(node_list, args, requirements,
          name=utility.now_str(), projects=[], runner="sync", host=None):
    """ Start run and register it into node_list

    Parameters
    ----------
    args : list of str
        arguments of run
    requirements : list of str
        list of paths which need to start run
    name : str, optional
        name of new run
    projects : list of str, optional
        tags or paths of projects (default=[])
    host : str, optional
        hostname in which run start
        `None` means localhost (default=None)
    """
    path = basket.get_new_run_abspath(name)
    if os.path.exists(path):
        raise dpError("Already exists: {}".format(path))
    with utility.mkdir(path):
        copy_requirements(path, requirements)
        detail = runners[runner](args, path, host)
    new_node = nodes.normalize({
        "path": path,
        "name": name,
        "type": "run",
        "parents": [basket.resolve_project_path(p) for p in projects],
        "children": [],
        "runner": detail,
    })
    nodes.add(node_list, new_node)
