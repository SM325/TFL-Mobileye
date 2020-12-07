try:
    print("Elementary imports: ")
    import os
    import json
    import glob
    import argparse

    print("numpy/scipy imports:")
    import numpy as np
    from scipy import signal as sg
    import scipy.ndimage as ndimage
    from scipy.ndimage.filters import maximum_filter

    print("PIL imports:")
    from PIL import Image

    print("matplotlib imports:")
    import matplotlib.pyplot as plt
except ImportError:
    print("Need to fix the installation")
    raise


def show_image(image, fig_num=None):
    plt.figure(fig_num).clf()
    plt.imshow(image)
    plt.show(block=True)

def test_conv():
    url = './data\\cologne_000057_000019_leftImg8bit.png'
    image = np.array(Image.open(url).convert("L"))

    k = np.array([[-1/9, -1/9, -1/9],
                  [-1/9, 8/9, -1/9],
                  [-1/9, -1/9, -1/9]])
    image1 = ndimage.filters.convolve(image, k, mode='constant', cval=0.0)

    show_image(image)
    show_image(image1)


if __name__ == '__main__':
    test_conv()