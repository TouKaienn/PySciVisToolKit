from .utils import *
import tifffile
import argparse
from dataclasses import dataclass
import tyro
from typing import Any, List, Literal, Optional, Tuple, Type

@dataclass
class Config:
    """Transfer .tiff file to .raw file for easier processing"""

    tiffPath: tyro.conf.Positional[str]
    """The dir path of images"""

    outPath: Optional[str] = None
    """Output volume path, if None, generate within "filePath" dir with name "OutputVol.raw"""

def main(args: Config):
    tifPath = args.tiffPath
    tiff_stack = tifffile.imread(tifPath)
    
    volume = np.array(tiff_stack)
    volume = volume.flatten("F")
    saveDat(volume,"./output.raw")
    print(volume.dtype)
    print(volume.shape)

def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)