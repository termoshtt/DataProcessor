# coding=utf-8
"""Configure manager of dataprocessor
"""

from . import utility, io
from .exception import DataProcessorError
import os.path
import argparse
import json
import ConfigParser


default_rcpath = "~/.dataprocessor.ini"


def get_run_dir(root_path):
    path = os.path.join(root_path, "Runs")
    return utility.get_directory(path)


def get_project_dir(root_path):
    path = os.path.join(root_path, "Projects")
    return utility.get_directory(path)


def get_figure_dir(root_path):
    path = os.path.join(root_path, "Figures")
    return utility.get_directory(path)


def ArgumentParser(rcpath=default_rcpath):
    """Argument parser for executables in this project.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Returns
    -------
    argparse.ArgumentParser instance

    """
    cfg = load_configure_file(rcpath)
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=cfg["root"],
                        help="data root")
    parser.add_argument("--json", default=cfg["json"],
                        help="path of data JSON")
    parser.add_argument("--debug", help="output traceback")
    return parser


def load(rcpath=default_rcpath):
    """Load node_list from default data.json.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Returns
    -------
    node_list

    """
    cfg = load_configure_file(rcpath)
    return io.load([], cfg["json"])


def update(node_list, rcpath=default_rcpath):
    """Save node_list into default data.json with update strategy.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    """
    cfg = load_configure_file(rcpath)
    with io.SyncDataHandler(cfg["json"], silent=True) as dh:
        dh.update(node_list)


def create_configure_file(rcpath=default_rcpath):
    """Create configure file.

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    """
    print("Creating " + rcpath)
    root = raw_input("Enter your Root direcotry: ")
    root_dir = utility.get_directory(root)
    default_path = os.path.join(root_dir, "data.json")
    json_path = raw_input("Enter path of your data json (default:{}): "
                          .format(default_path))
    if not json_path:
        json_path = default_path
    json_path = utility.path_expand(json_path)
    if not os.path.exists(json_path):
        print("Creating " + json_path)
        with open(json_path, "w") as f:
            f.write("[]")

    cfg = ConfigParser.RawConfigParser()
    cfg.add_section("data")
    cfg.set("data", "root", root_dir)
    cfg.set("data", "json", json_path)

    rcpath = utility.path_expand(rcpath)
    with open(rcpath, 'wb') as f:
        cfg.write(f)
    print("Your configure file: " + rcpath + " is successfully created")


def load_configure_file(rcpath=default_rcpath):
    """Load default configure.

    If the configure file does not exist, it will be created.
    (see `create_configure_file(rcpath)`)

    Parameters
    ----------
    rcpath : str, optional
        path of configure file (default=~/.dataprocessor.ini)

    Returns
    -------
    dict
        There are two keys: "root" and "json".

    Raises
    ------
    DataProcessorError
        raised when configure file does not exist.

    """
    rcpath = utility.path_expand(rcpath)
    if not os.path.exists(rcpath):
        raise DataProcessorError("Configure file does not exist")

    parser = ConfigParser.SafeConfigParser()
    parser.read(rcpath)
    return {
        "root": parser.get("data", "root"),
        "json": parser.get("data", "json"),
    }