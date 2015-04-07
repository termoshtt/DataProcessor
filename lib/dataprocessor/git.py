# coding:utf-8

import os
import subprocess
from .exception import DataProcessorError as dpError


def modified():
    """Check whether modified file exists in current project.

    Return
    ------
    Bool:
        - True  : if there is/are modified file(s)
        - False : otherwise

    """
    FNULL = open(os.devnull, "w")
    result = subprocess.call(["git", "diff", "--exit-code"], stdout=FNULL)
    return bool(result)


def untracked():
    """Check whether untracked file exists in current project.

    Return
    ------
    Bool:
        - True  : if there is/are untracked file(s)
        - False : otherwise

    """
    result = subprocess.check_output(["git", "clean", "--dry-run"])
    return bool(result)


def get_hash():
    """Get the hash of current commit

    Return
    ------
    str : hash string

    """
    hash_val = subprocess.check_output(['git', 'rev-parse', "HEAD"])
    return hash_val.strip("\n")


def get_valid_hash(check_modified=True, check_untracked=True):
    """ Get valid hash

    Parameters
    ----------
    check_modified : bool, optional
        check modified file (default=True)
    check_untracked : bool, optional
        check untracked file (default=True)

    Raises
    ------
    DataProcessorError
        if the repository is not clean (has modified and/or untracked file)

    Return
    ------
    str : hash string

    """
    if check_modified and modified():
        raise dpError("There is modified file")
    if check_untracked and untracked():
        raise dpError("There is untracked file")
    return get_hash()
