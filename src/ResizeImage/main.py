# Future Implementations
from __future__ import annotations

# Standard Library
from typing import Literal, Optional

# Package Library
from ResizeImage.imageresize import ImageResize
from ResizeImage.linkartists import LinkArtists


def main(
    image_path: Optional[str] = None,
    generate_ico: bool = False,
    replace_ini: bool = False,
    verbose: bool = False,
    include_subdir: bool = False,
    image_type: Literal["jpg", "png"] = "jpg",
) -> None:
    """Resize image to a square format.

    Parameters
    ----------
    image_path: str, optional
        Path to the image to be resize, by default None.
    generate_ico : bool, optional
        Create folder icon, by default False.
    replace_ini : bool, optional
        Replace the desktop.ini file of the folder, by default False.
    include_subdir : bool, optional
        Apply the function recursively, by default False.
    verbose : bool, optional
        Print additional information to the terminal, by default False.

    Returns
    -------
    None.
    """
    image_inst = ImageResize(
        generate_ico, replace_ini, verbose, include_subdir, image_type
    )
    try:
        image_inst(image_path)
    except KeyboardInterrupt:
        print("User interrupt.")


def util(
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
    linkartist_inst = LinkArtists(artist_path, folder_dir)
    linkartist_inst()
