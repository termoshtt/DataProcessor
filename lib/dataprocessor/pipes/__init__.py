# coding=utf-8
"""@pipes
"""
import sys
import glob
import os.path


__all__ = [os.path.basename(f)[:-3]
           for f in glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
           if os.path.basename(f) != "__init__.py"]

for mod in __all__:
    __import__(__package__ + "." + mod)

mod_list = [sys.modules[__package__ + "." + mod] for mod in __all__]

pipes_dics = {}
for mod in mod_list:
    try:
        register = getattr(mod, "register")
    except:
        continue
    register(pipes_dics)
