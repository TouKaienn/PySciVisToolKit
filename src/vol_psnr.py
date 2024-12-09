from .utils import *
import argparse
import os
from dataclasses import dataclass
import tyro
from typing import Any, List, Literal, Optional, Tuple, Type

@dataclass
class Config:
    """calculate the psnr of volumes, the parameter "eval" and "GT" can either be both file path or dir (but not one file path and one dir). The ext of file name can be anything including .raw or .iw"""

    GT: tyro.conf.Positional[str]
    """The path of the gt dir/file"""

    Eval: tyro.conf.Positional[str]
    """The path of the eval dir/file"""

    n: bool = False
    """whether norm the data to [-1,1] before calculating psnr"""

def main(args: Config):
    eval_path = args.Eval
    GT_path = args.GT
    eval_is_dir = os.path.isdir(eval_path)
    GT_is_dir = os.path.isdir(GT_path)
    if eval_is_dir and GT_is_dir:
        o = VolumeMetrics(GT_dirPath=GT_path, eval_dirPath=eval_path, verbose=True, normBeforeHand=args.n)
        MeanPSNR, PSNR = o.getBatchPSNR()
        for i in range(len(PSNR)):
            print(f"PSNR of {i+1} timestep is {PSNR[i]}")
        print(f"Mean PSNR is {MeanPSNR}")
        print(f"array:\n {PSNR}")
    elif (not eval_is_dir) and (not GT_is_dir):
        o = VolumeMetrics(normBeforeHand=args.n)
        PSNR = o.getPSNRFromFile(GT_path,eval_path)
        print(f"PSNR is {PSNR}")
    else:
        raise ValueError(f"eval and GT should be both dir or both file, but got {eval_path} is dir as {eval_is_dir} and {GT_path} is dir as {GT_is_dir}")


def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)