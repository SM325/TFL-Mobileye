import os
import glob
import numpy as np
from PIL import Image

default_base = './data/data1'
flist = glob.glob(os.path.join(default_base,  '*_leftImg8bit.png'))
image_path = flist[0]
color_image = np.array(Image.open(image_path))
image = np.array(Image.open(image_path).convert("L"), dtype=float)