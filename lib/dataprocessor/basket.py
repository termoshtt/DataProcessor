# -*- coding: utf-8 -*-

from . import rc, utility
from .exception import DataProcessorError as dpError

import os
import os.path as op
from datetime import datetime
from contextlib import contextmanager
from logging import getLogger, INFO
logger = getLogger(__name__)
logger.setLevel(INFO)


def _ready_basket(root, basket_name):
    if not root:
        root = rc.get_configure(rc.rc_section, "root")
    root = utility.check_directory(root)
    return utility.get_directory(op.join(root, basket_name))


def default_run_basket():
    return rc.get_configure_safe(rc.rc_section, "run_basket", "Runs")


def default_project_basket():
    return rc.get_configure_safe(rc.rc_section, "project_basket", "Projects")


def new_run_dir(name=datetime.now().strftime("%FT%T"), root=None,
                basket_name=default_run_basket()):
    """ Create a new run directory.

    Parameters
    ----------
    name : str, optional
        name of the new run directory (default=formatted time)
    root : str, optional
        new run directory is made in `${root}/${basket_name}/`.
        If not specified, "root" value of the setting file is used.
    basket_name : str, optional
        new run directory is made in `${root}/${basket_name}/`.
        (default="Runs")

    Raises
    ------
    DataProcessorRcError
        occurs when `root` is not specified and it cannot be loaded
        from the setting file.
    DataProcessorError
        occures when already the run dir exists.

    """
    basket = _ready_basket(root, basket_name)
    path = os.path.join(basket, name)
    if os.path.exists(path):
        raise dpError("Already exists: " + path)
    return utility.get_directory(path)


@contextmanager
def new_run(name=datetime.now().strftime("%FT%T"), root=None,
            basket_name=default_run_basket()):
    """ Create a new run directory

    A wrapper for new_run_dir to remove directory if something goes bad.

    """
    new_dir = new_run_dir(name, root, basket_name)
    try:
        yield new_dir
    except Exception:
        os.rmdir(new_dir)
        raise


def resolve_project_path(name_or_path, create_dir, root=None,
                         basket_name=default_project_basket()):
    """ Resolve project path from its path or name.

    Parameters
    ----------
    name_or_path : str
        Project identifier.
        If name (i.e. basename(name_or_path) == name_or_path),
        abspath of `root/basket_name/name` is returned.
        If path (otherwise case), returns its abspath.
    create_dir : boolean
        This flag determine the behavior occured when there is no directory at
        the resolved path as follows:
        - if create_dir is True: create new directory
        - if create_dir is False: raise DataProcessorError
    root : str, optional
        The root path of baskets. (default=None)
        If None, the path is read from the configure file.
    basket_name : str, optional
        The name of the project basket.
        If "project_basket" is specified in the configure file,
        default value is it. Otherwise, default is "Projects".

    Returns
    -------
    path : str
        existing project path

    Raises
    ------
    DataProcessorRcError
        occurs when `root` is not specified and it cannot be loaded
        from the setting file.

    DataProcessorError
        occurs when create_dir is False and a path is not resolved.

    """
    def _is_name(s):
        if "/" in s:  # path
            return False
        if s[0] is ".":  # relative path
            return False
        return True
    if _is_name(name_or_path):
        logger.info("regarded as name: {}".format(name_or_path))
        name = name_or_path
        basket = _ready_basket(root, basket_name)
        path = os.path.join(basket, name)
    else:
        logger.info("regarded as path: {}".format(name_or_path))
        path = utility.path_expand(name_or_path)
    if create_dir:
        return utility.get_directory(path)
    else:
        return utility.check_directory(path)
