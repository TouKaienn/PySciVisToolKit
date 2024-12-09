from .utils import *
import argparse
import os
from dataclasses import dataclass
import tyro
from typing import Any, List, Literal, Optional, Tuple, Type

@dataclass
class Config:
    """calculate the lpips and ssim of images, the parameter "eval" and "GT" can either be both file path or dir (but not one file path and one dir). The ext of file name can be anything including .raw or .iw"""

    GT: tyro.conf.Positional[str]
    """The path of the gt dir/file"""

    Eval: tyro.conf.Positional[str]
    """The path of the eval dir/file"""

    verbose: bool = False
    """Whether to print the verbose information """
    
def main(args: Config):
    eval_path = args.eval
    GT_path = args.GT
    eval_is_dir = os.path.isdir(eval_path)
    GT_is_dir = os.path.isdir(GT_path)
    if eval_is_dir and GT_is_dir:
        o = ImageMetrics(GT_dirPath=GT_path, eval_dirPath=eval_path, verbose=True)
        MeanSSIM, SSIM = o.getBatchSSIM()
        for i in range(len(SSIM)):
           print(f"SSIM of {i+1} timestep is {SSIM[i]}")
        print(f"Mean SSIM is {MeanSSIM}")
        print('\n')
        if args.verbose:
            print(f"array:\n {SSIM}")
    elif (not eval_is_dir) and (not GT_is_dir):
        o = ImageMetrics()
        SSIM = o.getSSIMFromFile(GT_path,eval_path)
        print(f"SSIM is {SSIM}")
    else:
        raise ValueError(f"eval and GT should be both dir or both file, but got {eval_path} is dir as {eval_is_dir} and {GT_path} is dir as {GT_is_dir}")

def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)