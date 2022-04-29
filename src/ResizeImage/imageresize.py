"""Main module."""

# Future Implementations
from __future__ import annotations

# Standard Library
from collections.abc import Generator
from contextlib import contextmanager
from os import chdir, system
from pathlib import Path
from typing import Literal, Optional

# Thirdparty Library
import cv2
import numpy as np

from PIL import Image
from cv2 import INTER_AREA, imdecode, imwrite, resize
from termcolor import cprint


system("color")
cv2.IMWRITE_JPEG_OPTIMIZE = 1
cv2.IMWRITE_JPEG_QUALITY = 100
cv2.IMWRITE_JPEG_LUMA_QUALITY = 100
cv2.IMWRITE_JPEG_CHROMA_QUALITY = 100


@contextmanager
def set_directory(path: Path) -> Generator[None, None, None]:
    """Change the working directory temporarily.

    Parameters
    ----------
    path : Path
        Directory to which to change.

    Yields
    ------
    Generator[None, None, None]
        New working directory.
    """

    origin = Path().absolute()
    try:
        chdir(path)
        yield
    finally:
        chdir(origin)


class ImageResize:
    """Resize image to square format."""

    def __init__(
        self,
        generate_ico: bool = False,
        replace_ini: bool = False,
        verbose: bool = False,
        include_subdir: bool = False,
        image_type: Literal["jpg", "png"] = "jpg",
    ) -> None:
        """Create ImageResize instance.

        Parameters
        ----------
        generate_ico : bool, optional
            Create folder icon, by default False.
        replace_ini : bool, optional
            Replace the desktop.ini file of the folder, by default False.
        include_subdir : bool, optional
            Apply the function recursively, by default False.
        verbose : bool, optional
            Print additional information to the terminal, by default False.
        """
        self.generate_ico = generate_ico
        self.replace_ini = replace_ini
        self.include_subdir = include_subdir
        self.verbose = verbose
        self.image_type = image_type

    def resize_image(self, image_path: str) -> None:
        """Resize image to a square format.

        Parameters
        ----------
        image_path : str
            Path to the image to be resized.

        Returns
        -------
        None.
        """
        path_image = Path(image_path)
        folder_path = path_image.parents[0]
        desk_path = folder_path / "desktop.ini"
        ico_path = folder_path / (path_image.stem + ".ico")
        np_image = np.fromfile(image_path, np.uint8)  # type: ignore

        input_img = imdecode(
            buf=np_image,
            flags=cv2.IMREAD_UNCHANGED
            + cv2.IMREAD_ANYDEPTH
            + cv2.IMREAD_ANYCOLOR,
        )

        if not isinstance(input_img, np.ndarray):
            return

        img_shape = np.array(input_img.shape[0:2])  # type: ignore

        shape_min = img_shape.min()
        shape_max = img_shape.max()
        if shape_min != shape_max:
            output_img = resize(
                input_img,
                dsize=(shape_min, shape_min),
                interpolation=INTER_AREA,
            )
            with set_directory(folder_path):
                imwrite(
                    filename=path_image.name,
                    img=output_img,
                    params=(
                        cv2.IMWRITE_JPEG_QUALITY,
                        cv2.IMWRITE_JPEG_LUMA_QUALITY,
                        cv2.IMWRITE_JPEG_CHROMA_QUALITY,
                        cv2.IMWRITE_JPEG_OPTIMIZE,
                    ),
                )
            cprint(
                f"Scaling {path_image.as_posix()} to {shape_min}, {shape_min}.",
                color="green",
            )
        elif self.verbose:
            cprint(
                f"{path_image.as_posix()} is already in a square format.\r\n",
                color="red",
            )

        if self.generate_ico:
            if path_image.stem == "folder":
                cprint(f"Generate {ico_path.as_posix()}.")
                img = Image.open(image_path)
                img.save(ico_path.as_posix())
            elif self.verbose:
                cprint(
                    f"{path_image.as_posix()} not the main folder image. Skipping...",
                    color="red",
                )

            folder_infotip = "InfoTip=" + path_image.parent.name + "\n"

            if any([not desk_path.exists(), self.replace_ini]):
                print(f"Generating {desk_path.as_posix()}.")
                with open(desk_path.as_posix(), "w") as f:
                    f.write("[ViewState]\n")
                    f.write("Mode=\n")
                    f.write("Vid=\n")
                    f.write("FolderType=Music\n")
                    f.write("[.ShellClassInfo]\n")
                    f.write("ConfirmFileOp=0\n")
                    f.write("IconFile=folder.ico\n")
                    f.write("IconIndex=0\n")
                    f.write(folder_infotip)
            elif self.verbose:
                print(f"{desk_path.as_posix()} already exists. Skipping...")

    def __call__(self, image_path: Optional[str] = None) -> None:
        """Batch resize images.

        Parameters
        ----------
        image_path : str, optional
            Path to the image to be resized, by default None.

        Returns
        -------
        None.
        """
        img_ext = f"*.{self.image_type}"
        if image_path is not None:
            self.resize_image(image_path)
        else:
            p = Path(".")

            if self.include_subdir:
                p_list = list(p.rglob(img_ext))
                webp_list = list(p.rglob("*.webp"))
            else:
                p_list = list(p.glob(img_ext))
                webp_list = list(p.glob("*.webp"))

            if webp_list:
                for webp_path in webp_list:
                    # Path to the converted webp file (now as a jpg).
                    conv_path = webp_path.parent / (webp_path.stem + ".jpg")
                    im = Image.open(webp_path.as_posix()).convert("RGB")
                    im.save(conv_path.as_posix(), "jpeg")

            if p_list:
                for p_path in p_list:
                    try:
                        self.resize_image(p_path.as_posix())
                    except UnicodeEncodeError:
                        print(
                            f"There was a unicode error for {p_path.as_posix()}."
                        )
                    except OSError:
                        Image.open(p_path.as_posix()).convert(
                            mode="RGB", colors=16777216
                        ).save(p_path.as_posix())
                        self.resize_image(p_path.as_posix())

            else:
                print("I didn't find any images in this directory.")
