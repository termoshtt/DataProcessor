# coding=utf-8
import argparse
import sys

from . import pipes
from . import rc


def dpmanip():
    try:
        parser = rc.ArgumentParser()
    except rc.DataProcessorRcError:
        print("Please create configure file by dpinit")
        sys.exit(1)

    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Ask whether REPLACE JSON file")
    parser.add_argument("-i", "--input", action="store_true",
                        help="Use stdin as data JSON")
    parser.add_argument("-o", "--output", action="store_true",
                        help="Output result node_list")
    parser.add_argument("-r", "--replace", action="store_true",
                        help="Use replace strategy for saving JSON")
    sub_psr = parser.add_subparsers(title="subcommands", metavar="pipes")
    for name, val in pipes.pipes_dics.items():
        pipe_psr = sub_psr.add_parser(name, help=val["desc"])
        for name, attr in val["args"]:
            pipe_psr.add_argument(name, **attr)
        if "kwds" in val:
            for kwd, attr in val["kwds"]:
                pipe_psr.add_argument("--" + kwd, **attr)
        pipe_psr.set_defaults(val=val)
    return parser


def dpstart():
    try:
        parser = rc.ArgumentParser()
    except rc.DataProcessorRcError:
        print("Please create configure file by dpinit")
        sys.exit(1)

    parser.add_argument("args", nargs='+', help="exec")
    parser.add_argument("-r", "--require", nargs='+', default=[],
                        help="required files")
    parser.add_argument("-n", "--name", help="run name")
    parser.add_argument("-p", "--project", nargs='+', default=[],
                        help="project name")
    parser.add_argument("-N", "--nocheck", action="store_true",
                        help="Do not check git status")
    parser.add_argument("--nocheck_untracked", action="store_true",
                        help="Do not check untracked files")
    parser.add_argument("--nocheck_modified", action="store_true",
                        help="Do not check modified files")
    parser.add_argument("--runner", action="store", default="sync",
                        help="Select runner (default=sync)")
    parser.add_argument("--remote", action="store", help="Remote hostname")
    parser.add_argument("--remote_tmpdir", action="store",
                        help="tmpdir in which run is executed")
    return parser


def dpgenzshcomp():
    parser = argparse.ArgumentParser()
    executable_names = [
        "dpmanip",
        "dpstart",
        "dpgenzshcomp",
        "dataprocessor",
        "register_figure"
    ]
    parser.add_argument("EXECUTABLE", choices=executable_names)
    return parser


def dataprocessor():
    parser = argparse.ArgumentParser(description="""
                command line interface for DataProcessor pipeline""")
    parser.add_argument('manip_json')
    parser.add_argument(
        '-d', "--data", nargs="?", help="The path of data JSON")
    return parser


def register_figure():
    parser = argparse.ArgumentParser(description="""
                Register generated figures into DataProcessor.
                The options -R and -g must be specified after ususal arguments.
                """)
    parser.add_argument("figure_directory",
                        help="The directory for saving figures")
    parser.add_argument("json_file",
                        help="The path of JSON file containing nodes")
    parser.add_argument("figures", nargs="+",
                        help="Paths of the figures that you want to register")
    parser.add_argument("-R", "--runs", dest="runs", nargs="+",
                        help="Paths of runs related to figures")
    parser.add_argument("-g", "--generators", dest="generators",
                        nargs="+", default=[],
                        help="Paths of generator files (s.t. fig.gp, fig.py)")
    return parser
