# Future Implementations
from __future__ import annotations

# Standard Library
import os
import shutil

from pathlib import Path
from typing import NamedTuple

# Thirdparty Library
import pandas as pd
import regex as re

from prettytable import PrettyTable


class MergeTuple(NamedTuple):
    folder_artist_path: str
    artist_name: str
    image_artist_path: str


class LinkArtists:
    """Link artist images to the respective folders."""

    def __init__(
        self,
        artist_path: str = "D:/Music/Artist Pictures/Thumb",
        folder_dir: str = "D:/Music/Music",
    ) -> None:
        """Link artist image to the respective artist folder.

        Parameters
        ----------
        artist_path : str, optional
            Path to the image folder, by default "D:/Music/Artist Pictures/Thumb".
        folder_dir : str, optional
            Path to the track folder, by default "D:/Music/Music".
        """
        self.artist_path = Path(artist_path)
        self.folder_dir = Path(folder_dir)
        self.pat_dot = re.compile(r"\.")

    def get_artist_name(self, pd_artist: pd.DataFrame) -> list[str]:
        """Extract artist name from path.

        Parameters
        ----------
        pd_artist : pd.DataFrame
            DataFrame containing artist paths.

        Returns
        -------
        list[str]
            List with artist names.
        """
        return_list: list[str] = []
        for dir_ in pd_artist["path"]:
            path_ = Path(dir_).name.lower()
            path_ = path_.replace(".jpg", "")
            path_ = path_.replace(".png", "")
            path_sub = self.pat_dot.sub("", path_)
            return_list.append(path_sub)

        return return_list

    def __call__(self) -> None:
        """Call the class as a function."""
        # ---------- Gather Directories Containing Album Artists --------- #
        folder_artist_path: set[str] = set()
        for rootdir, dirs, _ in os.walk(self.folder_dir):
            if not dirs:
                artist_dir_ = Path(rootdir).parent.as_posix()
                folder_artist_path.add(artist_dir_)

        folder_pd = pd.DataFrame({"path": sorted(folder_artist_path)}).assign(
            artist_name=self.get_artist_name
        )

        # ------ Gather Image Paths Of The Associated Album Artists ------ #
        picture_artist_path: set[str] = set()

        for artist_ in self.artist_path.rglob("*.jpg"):
            picture_artist_path.add(artist_.as_posix().lower())

        image_pd = pd.DataFrame(
            {
                "path": sorted(picture_artist_path),
            }
        ).assign(artist_name=self.get_artist_name)

        # ----------------------- Merge Both Tables ---------------------- #

        pd_merge = pd.merge(
            folder_pd,
            image_pd,
            on="artist_name",
            how="outer",
            indicator=True,
            suffixes=("_folder", "_image"),
        ).query("_merge!='right_only'")

        pd_merge_final = pd_merge.query("_merge=='both'").drop(
            columns="_merge"
        )

        # ---------- Copy Artist Thumbnails To The Artist Folder --------- #
        for dir_ in pd_merge_final.itertuples(index=False):
            pd_ = MergeTuple(*dir_)
            folder_ico_path = pd_.folder_artist_path + "/folder.jpg"
            image_name = Path(pd_.image_artist_path).name
            shutil.copy(pd_.image_artist_path, folder_ico_path)
            print(f"Copying {image_name} --> {folder_ico_path}")

        # ------------------- Report Missing Thumbnails ------------------ #
        list_missing = (
            pd_merge.query("_merge=='left_only'")
            .set_index("artist_name")
            .drop(index=["outside mb", "albums", "compilations"])
            .reset_index()["artist_name"]
            .tolist()
        )

        list_missing.sort()

        pt = PrettyTable()
        pt.field_names = [
            f"Scene Covers Dismatch = Missing {len(list_missing)} scenes"
        ]

        for i in list_missing:
            pt.add_row([i])

        pt.align = "l"

        print(pt)
