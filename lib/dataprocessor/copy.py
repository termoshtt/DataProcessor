# -*- coding: utf-8 -*-

from logging import getLogger, DEBUG
logger = getLogger(__name__)
logger.setLevel(DEBUG)

from .utility import check_file, path_expand
from .exception import DataProcessorError as dpError
import os.path
import shutil


def resolve_dest_path(from_path, to_path):
    from_path = check_file(from_path)
    to_path = path_expand(to_path)
    if os.path.exists(to_path) and os.path.isdir(to_path):
        to_dir = to_path
        to_name = os.path.basename(from_path)
    else:
        to_dir = os.path.dirname(to_path)
        to_name = os.path.basename(to_path)
    if not os.path.exists(to_dir):
        os.makedirs(to_dir)
    return (to_dir, to_name)


def _check_same_file(from_path, dest_path):
    from_con = open(from_path, 'r').read()
    dest_con = open(dest_path, 'r').read()
    return from_con == dest_con


def copy_file(from_path, to_path, strategy="replace"):
    """ Copy a file.

    If `to_path` already exist, check whether it is same file.
    When there are same file, skip.
    When there are different, replace the file or change file name.

    Moreover, when destination directory does not exist, create the direcotry.

    Parameters
    ----------
    from_path : str
    to_path : str
    strategy : str, optional, {"interactive", "replace", "skip", "error"}
        This specify the action when `to_path` already exists.
          + "replace" : `to_path` file will be replaced.
          + "skip" : do nothing.
          + "error" : raise DataProcessorError.

    Raises
    ------
    DataProcessorError
        Occur in two cases
            + Invalid `strategy` keyword is specified.
            + `to_path` already exists and the `strategy` is "error".

    """
    from_path = check_file(from_path)
    to_dir, to_name = resolve_dest_path(from_path, to_path)
    dest_path = os.path.join(to_dir, to_name)
    if not os.path.exists(dest_path):
        shutil.copy2(from_path, dest_path)
        return
    # already exists
    logger.info("A file already exists in %s" % dest_path)
    if _check_same_file(from_path, dest_path):
        logger.info("They are same contents. Skip copy.")
        return

    def _sent_error():
        raise dpError("%s already exist." % dest_path)
    strategies = {
        "replace": lambda: shutil.copy2(from_path, dest_path),
        "skip": lambda: logger.info("%s already exist. Skip copy." % dest_path),
        "error": _sent_error,
    }
    if strategy not in strategies:
        raise dpError("Invalid strategy: %s" % strategy)
    strategies[strategy]()
