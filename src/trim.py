from .utils import *
import argparse
from PIL import ImageChops
import os
from dataclasses import dataclass
import tyro
from typing import Any, List, Literal, Optional, Tuple, Type

@dataclass
class Config:
    """Auto detect the boarder bbox from a batch of images and trim them based on the bbox"""

    Path: tyro.conf.Positional[List[str]]
    """The img paths of image dir, can be multiple dirs separated by space or can be several img file path"""

    ref: Optional[str] = None
    """One reference image path or dir"""

    log: bool = False
    """log the bbox info to bbox.txt"""


def ImgTrim(Path,log=False,ref=None):
    img_paths = []
    ref_img_paths = []
    input_dir = True
    if os.path.isfile(Path[0]): # check whether the input is a dir or a file
        input_dir = False
    
    if input_dir:
        for img_dir in Path:
            img_paths.extend(getFilePathsInDir(img_dir))
    else:
        img_paths = Path
    global_bbox = (np.inf,np.inf,0,0)
    if ref is None: # no reference image for bbox
        for img_p in img_paths:
            if 'txt' in img_p:
                continue
            img = Image.open(img_p)
            bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
            diff = ImageChops.difference(img, bg)
            diff = ImageChops.add(diff, diff, 2.0, -100)
            bbox = diff.getbbox()
            global_bbox = (min(global_bbox[0],bbox[0]),min(global_bbox[1],bbox[1]),max(global_bbox[2],bbox[2]),max(global_bbox[3],bbox[3]))
    else:
        if os.path.isfile(ref):
            ref_img = Image.open(ref)
            ref_bg = Image.new(ref_img.mode, ref_img.size, ref_img.getpixel((0,0)))
            ref_diff = ImageChops.difference(ref_img, ref_bg)
            ref_diff = ImageChops.add(ref_diff, ref_diff, 2.0, -100)
            global_bbox = ref_diff.getbbox()
        else:
            ref_img_paths = getFilePathsInDir(ref)
            for ref_p in ref_img_paths:
                if 'txt' in ref_p:
                    continue
                img = Image.open(ref_p)
                bg = Image.new(img.mode, img.size, img.getpixel((0,0)))
                diff = ImageChops.difference(img, bg)
                diff = ImageChops.add(diff, diff, 2.0, -100)
                bbox = diff.getbbox()
                global_bbox = (min(global_bbox[0],bbox[0]),min(global_bbox[1],bbox[1]),max(global_bbox[2],bbox[2]),max(global_bbox[3],bbox[3]))
            
    pos = (global_bbox[0],global_bbox[1])
    size = (global_bbox[2]-global_bbox[0],global_bbox[3]-global_bbox[1])
    size = sizeCanDivideby2(size) # make sure the size can be divided by 2
    if log:
        with open(os.path.join('bbox.txt'),'w') as f:
            f.write("bbox: "+str(global_bbox)+'\n')
            f.write("size: "+str(size)+'\n')
            f.write("pos: "+str(pos))
    print("bbox: "+str(global_bbox)+'\n')
    print("size: "+str(size)+'\n')
    print("pos: "+str(pos))
    if input_dir:
        for img_dir in Path:
            ImgCrop(img_dir,'png',size,pos)
    else:
        CropOneImg(Path,size,pos)

def sizeCanDivideby2(size):
    import math
    size = (math.ceil(size[0]/2)*2,math.ceil(size[1]/2)*2)
    return size

def CropOneImg(ImgPaths,size,pos):
    """
    Description:
    Batch operation to crop all images (with img_type) in the ImgDir folder

    Args:
        ImgDir (str): the Image Dir path to be cropped
        size (list): The crop region size
        pos (list): The crop region position (left-up corner)
    Returns:
        None
    """
    i1 = ImgPaths
    for i in range(0,len(i1)):
        #print(i1[i])
        cmd = 'convert '+i1[i]+' -crop '+str(size[0])+'x'+str(size[1])+'+'+str(pos[0])+'+'+str(pos[1])+' '+i1[i]
        #print(cmd)
        subprocess.call(cmd,shell=True)
        
def main(args: Config):
    Path = args.Path
    log = args.log
    ref=args.ref
    ImgTrim(Path,log=log,ref=ref)

def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)
