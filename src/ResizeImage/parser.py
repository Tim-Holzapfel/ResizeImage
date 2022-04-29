"""Command line parser."""

# Future Implementations
from __future__ import annotations

# Standard Library
import argparse
import sys

from collections.abc import Callable
from typing import Optional

# Package Library
from ResizeImage.main import main, util


def main_parser() -> argparse.ArgumentParser:
    """Command line parser."""
    # ---------------------------------------------------------------------- #
    #                               Main Parser                              #
    # ---------------------------------------------------------------------- #
    # %% Main Parser
    parser = argparse.ArgumentParser(
        prog="ResizeImage",
        description="""
        Main parser.
        """.replace(
            "\n", " "
        ),
    )

    parser.add_argument(
        "image_path",
        type=str,
        nargs="?",
        default=None,
        help="""Path to image.""".replace("\n", " "),
    )

    parser.add_argument(
        "-d",
        "--dir",
        action="store_true",
        dest="include_subdir",
        help="""Parse the directories recursively.""".replace("\n", " "),
    )

    parser.add_argument(
        "-i",
        "--ico",
        action="store_true",
        dest="generate_ico",
        help="""Generate icons from the folder image.""".replace("\n", " "),
    )

    parser.add_argument(
        "--replace",
        action="store_true",
        dest="replace_ini",
        help="""Replace the desktop.ini file of the folder (Folder cannot be
             'Read Only').""".replace(
            "\n", " "
        ),
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        help="""Print additional information to the terminal.""".replace(
            "\n", " "
        ),
    )

    parser.add_argument(
        "--png",
        action="store_const",
        const="png",
        default="jpg",
        dest="image_type",
        help="""Specifies the type of image to look for.""".replace(
            "\n", " "
        ),
    )

    parser.set_defaults(func=main)

    return parser


def sub_parser() -> argparse.ArgumentParser:
    """Command line parser."""
    # ---------------------------------------------------------------------- #
    #                               Main Parser                              #
    # ---------------------------------------------------------------------- #
    # %% Main Parser
    parser = argparse.ArgumentParser(
        prog="LinkArtistsToImage",
        description="""
        Main parser.
        """.replace(
            "\n", " "
        ),
    )

    parser.add_argument(
        "artist_path",
        type=str,
        nargs="?",
        default="D:/Music/Artist Pictures/Thumb",
        help="""Path to image folder.""".replace("\n", " "),
    )

    parser.add_argument(
        "folder_dir",
        type=str,
        nargs="?",
        default="D:/Music/Music",
        help="""Path to track folder.""".replace("\n", " "),
    )

    parser.set_defaults(func=util)

    return parser


def parse_main(args: Optional[list[str]] = None) -> int:
    """Command line function."""
    if args is None:
        args = sys.argv[1:]
    parser = main_parser()
    parsed_args = parser.parse_args()

    # Extract argument key values from parser
    args_key = vars(parsed_args)

    # Extract function from parser
    args_func: Callable[..., None] = args_key.pop("func", None)

    args_func(**args_key)
    return 0


def parse_sub(args: Optional[list[str]] = None) -> int:
    """Command line function."""
    if args is None:
        args = sys.argv[1:]
    parser = sub_parser()
    parsed_args = parser.parse_args()

    # Extract argument key values from parser
    args_key = vars(parsed_args)

    # Extract function from parser
    args_func: Callable[..., None] = args_key.pop("func", None)

    args_func(**args_key)
    return 0
