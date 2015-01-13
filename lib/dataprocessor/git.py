# coding:utf-8

import os
import subprocess


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
