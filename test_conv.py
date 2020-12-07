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
    # plt.figure(fig_num).clf()
    plt.imshow(image, cmap="gray")
    plt.show(block=True)

def test_conv():
    url = './data\\frankfurt_000000_002963_leftImg8bit.png'
    image = np.array(Image.open(url).convert("L"))

    k = np.array([[118, 122, 121, 121, 117, 117, 122, 126, 124, 130, 130, 125, 133,
        136, 145, 170, 191],
       [ 92,  93,  93,  93,  94,  95,  97, 100, 105, 117, 124, 125, 127,
        126, 145, 191, 215],
       [ 80,  79,  85,  99, 101, 108, 121, 125, 127, 130, 129, 126, 124,
        123, 137, 184, 212],
       [ 88,  90, 103, 118, 126, 136, 149, 159, 164, 162, 154, 137, 127,
        118, 121, 156, 190],
       [105, 113, 125, 144, 168, 194, 201, 204, 206, 209, 204, 180, 155,
        128, 117, 136, 159],
       [118, 119, 133, 148, 181, 227, 238, 215, 212, 231, 232, 207, 185,
        149, 124, 137, 157],
       [131, 130, 147, 184, 213, 246, 254, 244, 237, 247, 244, 223, 205,
        169, 132, 140, 153],
       [138, 137, 158, 210, 241, 253, 255, 255, 254, 254, 253, 238, 216,
        181, 137, 135, 143],
       [135, 131, 157, 209, 245, 253, 254, 252, 252, 253, 252, 244, 219,
        182, 136, 129, 136],
       [132, 126, 157, 223, 253, 254, 254, 251, 248, 252, 252, 254, 237,
        181, 137, 124, 124],
       [130, 121, 143, 194, 231, 252, 254, 251, 251, 252, 249, 240, 213,
        163, 129, 120, 115],
       [119, 116, 132, 150, 193, 253, 255, 251, 251, 254, 248, 197, 170,
        135, 116, 118, 115],
       [121, 122, 116, 128, 178, 217, 230, 232, 231, 229, 217, 179, 145,
        128, 121, 112, 105],
       [ 92, 101, 111, 129, 139, 158, 178, 204, 200, 189, 167, 151, 131,
        115, 100,  93, 104],
       [ 97,  81,  72,  93, 115, 131, 133, 146, 145, 142, 137, 120,  95,
         76,  58,  83, 111],
       [120,  84,  51,  62,  67,  95, 113, 117, 117, 118,  99,  85,  66,
         64,  61,  90, 111],
       [103,  84,  50,  36,  39,  41,  49,  54,  61,  65,  60,  53,  51,
         52,  53,  85, 101]])
    # k = 1 - (k/(len(k)**2))
    k = np.flipud(k)
    k = np.fliplr(k)

    # image1 = ndimage.filters.convolve(image, k, mode='constant', cval=0.0)
    image1 = sg.convolve2d(image, k)
    show_image(image)
    show_image(image1)


if __name__ == '__main__':
    test_conv()