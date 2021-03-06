# coding=utf-8
from ..nodes import get, add
from ..utility import abspath, check_or_create_dir
from ..exception import DataProcessorError as dpError
from ..basket import resolve_project_path

import os.path


def add_tag(node_list, node_path, project_id):
    """ Make the node belong to the project specified by project id.

    We realize "tagging" feature by project nodes.

    Parameters
    ----------
    node_path : str
        This path specify the unique node.
    project_id: str
        the name or path of project.
        The path is resolved by resolve_project_path.

    """
    path = abspath(node_path)
    node = get(node_list, path)
    if not node:
        raise dpError("There is no node (path=%s)." % path)
    project_path = resolve_project_path(project_id)
    check_or_create_dir(project_path)
    if project_path == path:
        raise dpError("Cannot tag itself")
    project_node = get(node_list, project_path)
    if not project_node:
        add(node_list, {
            "path": project_path,
            "type": "project",
            "name": os.path.basename(project_path),
            "children": [path],
            "parents": [],
        })
    else:
        if path not in project_node["children"]:
            project_node["children"].append(path)
    if project_path not in node["parents"]:
        node["parents"].append(project_path)
    return node_list


def register(pipe_dics):
    pipe_dics["add_tag"] = {
        "func": add_tag,
        "args": ["path", "project_id"],
        "desc": "Add a tag into the node",
    }
