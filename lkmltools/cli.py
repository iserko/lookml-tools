import argparse
import logging
import os
import subprocess

from lkmltools.config import config
from lkmltools.grapher.graph_animator import GraphAnimator
from lkmltools.grapher.lookml_grapher import LookMlGrapher
from lkmltools.linter.lookml_linter import LookMlLinter
from lkmltools.updater.lookml_modifier import LookMlModifier


def git_clone(args):

    url = config["git"]["url"]
    folder = config["git"]["folder"]

    cmd = ["git", "clone", url, folder]

    if "use_hub" in config and config["use_hub"]:
        logging.info("Using hub instead of git")
        cmd = ["hub", "clone", url, folder]

    logging.info("About to run %s", " ".join(cmd))

    try:
        output = subprocess.check_output(
            cmd,
            stderr=subprocess.STDOUT,
            shell=False,
            timeout=3,
            universal_newlines=True,
        )
    except subprocess.CalledProcessError as exc:
        logging.error("%s %s" % (exc.returncode, exc.output))
    else:
        logging.info("Output: %s", output)


def grapher(args):
    if args.image_height:
        config["grapher"]["options"]["image_height"] = args.image_height
    if args.image_width:
        config["grapher"]["options"]["image_width"] = args.image_width
    if args.node_size:
        config["grapher"]["options"]["node_size"] = args.node_size
    LookMlGrapher().run()


def graph_animator(args):

    branch = args.branch if args.branch else "master"

    if not os.path.exists(args.image_directory):
        os.makedirs(args.image_directory)

    animator = GraphAnimator()
    animator.create_gif(
        args.path_to_repo, branch, args.image_directory, args.gif_filename
    )


def linter(args):
    LookMlLinter().run()


def updater(args):
    modifier = LookMlModifier()
    modifier.modify(args.infile, args.outfile)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="output more verbose information"
    )
    parser.add_argument(
        "--glob",
        action="append",
        help="specify custom glob, can be specified multiple times",
    )
    subparsers = parser.add_subparsers()

    git_clone_parser = subparsers.add_parser("git-clone")
    git_clone_parser.set_defaults(func=git_clone)

    grapher_parser = subparsers.add_parser("grapher")
    grapher_parser.add_argument("--image-width", type=int)
    grapher_parser.add_argument("--image-height", type=int)
    grapher_parser.add_argument("--node-size", type=int)
    grapher_parser.set_defaults(func=grapher)

    graph_animator_parser = subparsers.add_parser("graph-animator")
    graph_animator_parser.add_argument(
        "--path-to-repo", dest="path_to_repo", help="Path to repo", required=True
    )
    graph_animator_parser.add_argument(
        "--branch", help="Git repo branch", required=False
    )
    graph_animator_parser.add_argument(
        "--image-directory",
        dest="image_directory",
        help="Directory to save images to. Will be created if does not exist",
        required=True,
    )
    graph_animator_parser.add_argument(
        "--gif-filename",
        dest="gif_filename",
        help="filepath of output GIF",
        required=True,
    )
    graph_animator_parser.set_defaults(func=graph_animator)

    linter_parser = subparsers.add_parser("linter")
    linter_parser.set_defaults(func=linter)

    updater_parser = subparsers.add_parser("updater")
    updater_parser.add_argument(
        "--infile", help="Filepath of input LookML file", required=True
    )
    updater_parser.add_argument(
        "--outfile", help="Filepath of output LookML file", required=True
    )
    updater_parser.set_defaults(func=updater)

    args = parser.parse_args()
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    logging.basicConfig(
        format="%(asctime)s %(levelname)s %(filename)s %(funcName)s: %(message)s",
        level=logging.INFO,
    )
    if args.glob:
        config["infile_globs"] = args.glob
    logger = logging.getLogger("lkmltools")
    logger.setLevel(log_level)
    args.func(args)


if __name__ == "__main__":
    main()
