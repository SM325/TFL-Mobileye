import test_conv

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
    from scipy.ndimage.filters import maximum_filter, minimum_filter

    print("PIL imports:")
    from PIL import Image

    print("matplotlib imports:")
    import matplotlib.pyplot as plt
except ImportError:
    print("Need to fix the installation")
    raise

print("All imports okay. Yay!")


def create_kernel10():
    filter_kernel = np.array([[-3.5, -2.25, -2, -2, -2],
                              [-2.25, -1, 1 / 4, 1 / 2, 1],
                              [-2, 1 / 4, 1, 1, 1.25],
                              [-2, 1 / 2, 1, 2, 3],
                              [-2, 1, 1.25, 3, 4]])
    filter_kernel = np.hstack([filter_kernel[::], np.fliplr(filter_kernel)])
    filter_kernel = np.vstack([filter_kernel[::], filter_kernel[::-1]])
    filter_kernel = filter_kernel / (filter_kernel.max() - filter_kernel.min())
    filter_kernel_3m = np.array([filter_kernel, filter_kernel, filter_kernel])
    return filter_kernel


def create_kernel10():
    filter_kernel = np.array([[-3.5, -2.25, -2, -2, -2],
                              [-2.25, -1, 1 / 4, 1 / 2, 1],
                              [-2, 1 / 4, 1, 1, 1.25],
                              [-2, 1 / 2, 1, 2, 3],
                              [-2, 1, 1.25, 3, 4]], dtype=float)
    filter_kernel = np.hstack([filter_kernel[::], np.fliplr(filter_kernel)])
    filter_kernel = np.vstack([filter_kernel[::], filter_kernel[::-1]])
    filter_kernel = filter_kernel / (filter_kernel.max() - filter_kernel.min())
    return filter_kernel


def create_kernel5():
    kernel = np.array([[-1, -1, -1, -1, -1],
                       [-1, 1, 2, 1, -1],
                       [-1, 2, 4, 2, -1],
                       [-1, 1, 2, 1, -1],
                       [-1, -1, -1, -1, -1]], dtype=float)

    kernel = kernel / (kernel.max() - kernel.min())
    return kernel


def create_kernel3():
    kernel = np.array([[-1/9, -1/9, -1/9],
                       [-1/9, 8/9, -1/9],
                       [-1/9, -1/9, -1/9]], dtype=float)

    kernel = kernel / (kernel.max() - kernel.min())
    return kernel

def find_tfl_lights(c_image: np.ndarray, fig_ax, **kwargs):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """
    threshold = 2.5
    # kernel = get_kernel(5)
    # kernel_arr = [create_kernel3(), create_kernel5(), create_kernel10()]
    kernel_arr = [create_kernel10()]
    c_image = ndimage.gaussian_filter(c_image, sigma=1)
    after_filter = c_image

    for kernel in kernel_arr:
        after_filter = sg.convolve2d(after_filter, kernel, boundary="symm", mode="same")
    # after_filter = ndimage.convolve(c_image, kernel, mode='constant', cval=0.0)

    fig_ax.imshow(after_filter, cmap="gray")
    fig_ax.set_title('filter')

    data_max = maximum_filter(after_filter, 35)
    maxima = (after_filter == data_max)
    after_filter[maxima == False] = 0
    after_filter[after_filter < threshold] = 0

    slices = np.argwhere(after_filter > 0)

    # red_x, red_y, green_x, green_y = [], [], [], []

    x, y = [], []

    for dy, dx in slices:
        x.append(dx)
        y.append(dy)
    print(len(x))
    return x, y


def show_image_and_gt(image, objs, fig_num=None):
    # plt.figure(fig_num).clf()
    plt.imshow(image)
    plt.subplot()
    labels = set()
    if objs is not None:
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        if len(labels) > 1:
            plt.legend()


def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """
    color_image = np.array(Image.open(image_path))
    image = np.array(Image.open(image_path).convert("L"), dtype=float)
    image /= 255

    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]


    # show_image_and_gt(image, objects, fig_num)
    plt.figure()
    ax1 = plt.subplot(221)
    ax2 = plt.subplot(222, sharex=ax1, sharey=ax1)
    ax3 = plt.subplot(223, sharex=ax1, sharey=ax1)

    ax1.imshow(color_image)
    ax1.set_title('original')

    ax2.imshow(color_image)
    ax2.set_title('original after filter')

    x, y = find_tfl_lights(image, ax3, some_threshold=42)

    cord = zip(x, y)

    for x, y in cord:
        red_val = color_image[y, x, 0]
        green_val = color_image[y, x, 1]
        if red_val >= green_val:
            ax2.plot(x, y, 'r+', color='r', markersize=4)
        else:
            ax2.plot(x, y, 'b+', color='b', markersize=4)


    # ax2.plot(red_x, red_y, 'r+', color='r', markersize=4)
    # ax2.plot(green_x, green_y, 'b+', color='b', markersize=4)


def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""
    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = './data'
    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    # flist = glob.glob(os.path.join(args.dir, 'munster_000023_000019_leftImg8bit.png'))

    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None

        test_find_tfl_lights(image, json_fn)
        plt.show(block=True)

        # plt.show(block=True)
    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)


if __name__ == '__main__':
    # test_conv.test_conv()
    main()
