# -*- coding: utf-8 -*-


from . import utility, basket, nodes, rc
from .runner import runners
from .exception import DataProcessorError as dpError
import os.path


def copy_requirements(path, requirements, host=None):
    utility.check_dir(path, host)
    for req in requirements:
        utility.check_file(req)
        utility.check_copy(req, path, host)


def ready_projects(node_list, projects):
    projects = [basket.resolve_project_path(p) for p in projects]
    for project_path in projects:
        if nodes.get(node_list, project_path):  # already exists
            continue
        # create new project node
        utility.check_or_create_dir(project_path)
        node = nodes.normalize({
            "path": project_path,
            "name": os.path.basename(project_path),
            "type": "project",
        })
        nodes.add(node_list, node)
    return projects


def _create_remote_tmp_dir(host):
    tmp_root = rc.get_configure_safe("remote_tmp_dir", "dp_tmp")
    remote_tmp_dir = os.path.join(tmp_root, utility.now_str())
    utility.check_call(["ssh", host, "mkdir", "-p", remote_tmp_dir])
    return remote_tmp_dir


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

    Return
    ------
    dict
        new node
    """
    path = basket.get_new_run_abspath(name)
    if os.path.exists(path):
        raise dpError("Already exists: {}".format(path))
    with utility.mkdir(path):
        if host:
            work_dir = _create_remote_tmp_dir(host)
            copy_requirements(work_dir, requirements, host)
        else:
            copy_requirements(path, requirements)
        detail = runners[runner](args, path, host)
    projects = ready_projects(node_list, projects)
    new_node = nodes.normalize({
        "path": path,
        "name": name,
        "type": "run",
        "parents": projects,
        "children": [],
        "runner": detail,
    })
    if host:
        new_node["host"] = host
        new_node["work_dir"] = work_dir
    nodes.add(node_list, new_node)
    return new_node
