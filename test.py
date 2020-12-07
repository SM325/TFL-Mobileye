import os
import json
import glob
import argparse

import numpy as np
from scipy import signal as sg
import scipy.ndimage as ndimage
from scipy.ndimage.filters import maximum_filter, minimum_filter
import cv2 as cv

from PIL import Image

import matplotlib.pyplot as plt

threshold = 0.6

default_base = './data'
flist = glob.glob(os.path.join(default_base, '*_leftImg8bit.png'))
for image in flist:
    # flist = glob.glob(os.path.join(default_base, 'cologne_000057_000019_leftImg8bit.png'))
    plt.figure()
    ax1 = plt.subplot(211)
    ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
    # fig, (ax1, ax2) = plt.subplots(2)

    image_path = image
    original_image = np.array(Image.open(image_path).convert("L"), dtype=float)
    original_image /= 255

    ax1.imshow(original_image)
    ax1.set_title('original')

    kernel = np.array([[-1, -1, -1, -1, -1],
                   [-1,  1,  2,  1, -1],
                   [-1,  2,  4,  2, -1],
                   [-1,  1,  2,  1, -1],
                   [-1, -1, -1, -1, -1]], dtype=float)

    # kernel =kernel/ (4- (-1))
    #
    # k = np.array([[118, 122, 121, 121, 117, 117, 122, 126, 124, 130, 130, 125, 133, 136, 145, 170, 191],
    #             [92, 93, 93, 93, 94, 95, 97, 100, 105, 117, 124, 125, 127, 126, 145, 191, 215],
    #             [80, 79, 85, 99, 101, 108, 121, 125, 127, 130, 129, 126, 124, 123, 137, 184, 212],
    #             [88, 90, 103, 118, 126, 136, 149, 159, 164, 162, 154, 137, 127,
    #              118, 121, 156, 190],
    #             [105, 113, 125, 144, 168, 194, 201, 204, 206, 209, 204, 180, 155,
    #              128, 117, 136, 159],
    #             [118, 119, 133, 148, 181, 227, 238, 215, 212, 231, 232, 207, 185,
    #              149, 124, 137, 157],
    #             [131, 130, 147, 184, 213, 246, 254, 244, 237, 247, 244, 223, 205,
    #              169, 132, 140, 153],
    #             [138, 137, 158, 210, 241, 253, 255, 255, 254, 254, 253, 238, 216,
    #              181, 137, 135, 143],
    #             [135, 131, 157, 209, 245, 253, 254, 252, 252, 253, 252, 244, 219,
    #              182, 136, 129, 136],
    #             [132, 126, 157, 223, 253, 254, 254, 251, 248, 252, 252, 254, 237,
    #              181, 137, 124, 124],
    #             [130, 121, 143, 194, 231, 252, 254, 251, 251, 252, 249, 240, 213,
    #              163, 129, 120, 115],
    #             [119, 116, 132, 150, 193, 253, 255, 251, 251, 254, 248, 197, 170,
    #              135, 116, 118, 115],
    #             [121, 122, 116, 128, 178, 217, 230, 232, 231, 229, 217, 179, 145,
    #              128, 121, 112, 105],
    #             [92, 101, 111, 129, 139, 158, 178, 204, 200, 189, 167, 151, 131,
    #              115, 100, 93, 104],
    #             [97, 81, 72, 93, 115, 131, 133, 146, 145, 142, 137, 120, 95,
    #              76, 58, 83, 111],
    #             [120, 84, 51, 62, 67, 95, 113, 117, 117, 118, 99, 85, 66,
    #              64, 61, 90, 111],
    #             [103, 84, 50, 36, 39, 41, 49, 54, 61, 65, 60, 53, 51,
    #              52, 53, 85, 101]])
    #
    # k = k - k.mean()
    # k = np.flipud(k)
    # k = np.fliplr(k)
    # k = k / 255
    #
    # filter_kernel = np.array([[-3.5, -2.25, -2, -2, -2],
    #                           [-2.25, -1, 1 / 4, 1 / 2, 1],
    #                           [-2, 1 / 4, 1, 1, 1.25],
    #                           [-2, 1 / 2, 1, 2, 3],
    #                           [-2, 1, 1.25, 3, 4]])
    # filter_kernel = np.hstack([filter_kernel[::], np.fliplr(filter_kernel)])
    # filter_kernel = np.vstack([filter_kernel[::], filter_kernel[::-1]])
    # filter_kernel = filter_kernel / 7.5

    after_filter = sg.convolve2d(original_image, kernel)

    data_max = maximum_filter(after_filter, 10)
    maxima = (after_filter == data_max)
    # data_min = minimum_filter(after_filter, 10)
    # diff = ((data_max - data_min) > 0.6)
    # maxima[diff == 0] = 0

    after_filter[maxima == False] = 0
    after_filter[after_filter < threshold] = 0

    slices = np.argwhere(after_filter > 0)


    #
    # labeled, num_objects = ndimage.label(maxima)
    # slices = ndimage.find_objects(labeled)
    # x, y = [], []
    # for dy, dx in slices:
    #     x_center = (dx.start + dx.stop - 1) / 2
    #     x.append(x_center)
    #     y_center = (dy.start + dy.stop - 1) / 2
    #     y.append(y_center)

    x, y = [], []
    for dy, dx in slices:
        x.append(dx)
        y.append(dy)

    ax1.plot(x, y, 'r+', color='r', markersize=4)

    ax2.imshow(after_filter)
    ax2.set_title('after filter')

    plt.show()

#np.argwhere
