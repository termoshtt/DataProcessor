# coding:utf-8

import os
import subprocess


def no_modified():
    """Check whether modified file exists in current project.

    Return
    ------
    Bool:
        - True  : if there is no modified file
        - False : otherwise

    """
    FNULL = open(os.devnull, "w")
    result = subprocess.call(["git", "diff", "--exit-code"], stdout=FNULL)
    if result:
        return False
    else:
        return True


def no_untracked():
    """Check whether untracked file exists in current project.

    Return
    ------
    Bool:
        - True  : if there is no untracked file
        - False : otherwise

    """
    result = subprocess.check_output(["git", "clean", "--dry-run"])
    if not result:
        return True
    else:
        return False


def get_hash():
    """Get the hash of current commit

    Return
    ------
    str : hash string

    """
    hash_val = subprocess.check_output(['git', 'rev-parse', "HEAD"])
    return hash_val.strip("\n")
