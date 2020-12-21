import matplotlib.pyplot as plt
from PIL import Image
import scipy.ndimage.filters as filters
import numpy as np
from scipy import signal
import scipy.ndimage as ndimage

import os
import json
import glob
import argparse



def high_pass_filter_green(img):
    highpass_filter = np.array([[-1/9, -1/9, -1/9],
                   [-1/9, 8/9, -1/9],
                   [-1/9, -1/9, -1/9]])

    return signal.convolve2d(img[:,:, 1], highpass_filter,  boundary="symm", mode="same")

def high_pass_filter_red(img):
    highpass_filter = np.array([[-1/9, -1/9, -1/9],
                   [-1/9, 8/9, -1/9],
                   [-1/9, -1/9, -1/9]])

    return signal.convolve2d(img[:,:, 0], highpass_filter,  boundary="symm", mode="same")


def recognize_traffic_light(img):
    neighborhood_size = 75
    threshold = 0.2

    data_max = filters.maximum_filter(img, neighborhood_size)
    maxima = (img == data_max)
    data_min = filters.minimum_filter(img, neighborhood_size)

    diff = ((data_max - data_min) >= threshold)
    maxima[diff == 0] = 0

    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)

    x, y = [], []
    for dy, dx in slices:
        # if (dx.start > 5 and dx.start < 1995 and dy.start > 5 and dy.start < 995):
        x_center = int((dx.start + dx.stop - 1) / 2)
        x.append(x_center)
        y_center = int((dy.start + dy.stop - 1) / 2)
        y.append(y_center)
    return x, y

def print_picture(path_img):

    picture = np.array(Image.open(path_img)).astype(float) / 255

    highpass_filter_green = high_pass_filter_green(picture)
    highpass_filter_red = high_pass_filter_red(picture)

    x_green, y_green = recognize_traffic_light(highpass_filter_green)

    x_red, y_red = recognize_traffic_light(highpass_filter_red)

    picture2 = np.array(Image.open(path_img))

    x_red_, y_red_ = [], []
    for i in range(len(x_red)):
        if (x_red[i] not in x_green and not y_red[i] in y_green):
            x_red_.append(x_red[i])
            y_red_.append(y_red[i])

    plt.figure()
    plt.imshow(picture)

    cord = zip(x_green, y_green)
    for x, y in cord:
        red_val = picture2[y, x, 0]
        green_val = picture2[y, x, 1]
        if red_val >= green_val:
            plt.plot(x, y, 'r+')
        else:
            plt.plot(x, y, 'g+')

    cord = zip(x_red_, y_red_)
    for x, y in cord:
        red_val = picture2[y, x, 0]
        green_val = picture2[y, x, 1]
        if red_val >= green_val:
            plt.plot(x, y, 'r+')
        else:
            plt.plot(x, y, 'g+')

    print(len(x_green), ", ", len(x_red_))

    plt.show(block=True)


def main(argv=None):

    # parser = argparse.ArgumentParser("Test TFL attention mechanism")
    # parser.add_argument('-i', '--image', type=str, help='Path to an image')
    # parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    # parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    # args = parser.parse_args(argv)
    default_base = './data'
    # if args.dir is None:
    #     args.dir = default_base
    flist = glob.glob(os.path.join(default_base, '*_leftImg8bit.png'))

    for image in flist:
        # json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        # if not os.path.exists(json_fn):
        #     json_fn = None

        # test_find_tfl_lights(image, json_fn)
        print_picture(image)
        plt.show(block=True)

    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)


if __name__ == '__main__':
    main()