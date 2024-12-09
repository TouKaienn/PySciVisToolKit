from utils import *
import argparse
import os
from icecream import ic
from PIL import Image
import cv2
import imageio
from dataclasses import dataclass
import tyro
from typing import Any, List, Literal, Optional, Tuple, Type

@dataclass
class Config:
    """Convert a set of images into one video"""

    imgsDir: tyro.conf.Positional[str]
    """The path of the images dir"""

    outPath: Optional[str] = None
    """The path of the output mp4 video file"""

    fps: int = 25
    """The fps of the output video"""
    
def main(args: Config):
    imgsDir = args.imgsDir
    outPath = args.outPath
    fps = args.fps
    
    imgW, imgH = None, None
    imgs = []
    imgPaths = getFilePathsInDir(imgsDir)
    for i in range(len(imgPaths)):
        img = Image.open(imgPaths[i])
        imgs.append(np.array(img))
        if i == 0:
            imgW, imgH = img.size
    if outPath is None:
        outPath = os.path.join(imgsDir,'video.mp4')
    imageio.mimwrite(outPath, imgs, fps=fps, quality=8, macro_block_size=1)
    
def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)