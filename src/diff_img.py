from .utils import getDiffImgFromDir, getDiffImgDir
from dataclasses import dataclass
import tyro

@dataclass
class Config:
    """Configuration of diff image"""
    
    dirPath: tyro.conf.Positional[str]
    """The dir path of images"""
    dirPathGT: str = "None"
    """The dir path of GT images, if assign, will compute diff image in dirPath and dirPathGT file-wisely"""
    DiffSaveDir: str = "None"
    """The dir path to save the diff images, must be assigned if dirPathGT is assigned"""
    GTFileName: str = 'GT.png'
    """The ground truth image name in dirPath"""


def main(config: Config):
    if config.dirPathGT == "None":
        getDiffImgFromDir(config.dirPath,GTFileName=config.GTFileName)
    else:
        getDiffImgDir(config.dirPath,config.dirPathGT,config.DiffSaveDir)

def entrypoint():
    """Entrypoint for use with pyproject scripts."""
    tyro.extras.set_accent_color("bright_yellow")
    args = tyro.cli(Config)
    main(args)

if __name__ == "__main__":
    entrypoint()
