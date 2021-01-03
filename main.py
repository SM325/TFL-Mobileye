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


def create_kernel25():
    kernel = np.array([[34, 33, 32, 32, 33, 33, 35, 34, 35, 36, 39, 41, 44,
                        45, 44, 42, 40, 39, 36, 35, 34, 34, 33, 33, 32, 48],
                       [32, 30, 29, 29, 29, 29, 32, 30, 40, 42, 60, 65, 84,
                        92, 87, 62, 55, 41, 39, 35, 34, 30, 30, 31, 30, 47],
                       [32, 30, 29, 26, 28, 33, 31, 63, 75, 100, 121, 127, 147,
                        154, 151, 134, 119, 99, 58, 50, 38, 33, 32, 31, 30, 46],
                       [33, 30, 31, 26, 41, 39, 92, 115, 144, 163, 176, 179, 190,
                        193, 192, 184, 174, 154, 129, 85, 72, 44, 39, 31, 30, 44],
                       [33, 32, 34, 18, 47, 59, 133, 148, 189, 207, 216, 220, 222,
                        220, 220, 217, 209, 190, 173, 136, 104, 61, 51, 47, 34, 42],
                       [34, 34, 31, 30, 85, 119, 162, 181, 212, 220, 222, 224, 226,
                        225, 224, 222, 221, 215, 204, 173, 147, 95, 84, 63, 38, 43],
                       [35, 31, 36, 66, 120, 151, 190, 215, 218, 221, 218, 219, 219,
                        224, 223, 220, 225, 225, 218, 211, 188, 123, 118, 81, 45, 43],
                       [37, 33, 75, 89, 143, 167, 213, 226, 224, 222, 220, 220, 220,
                        222, 224, 218, 227, 232, 225, 220, 207, 149, 134, 106, 65, 46],
                       [39, 50, 102, 95, 171, 196, 222, 233, 225, 224, 228, 224, 226,
                        224, 227, 217, 227, 235, 234, 226, 219, 184, 148, 120, 96, 50],
                       [39, 81, 113, 102, 185, 215, 226, 234, 227, 226, 231, 229, 230,
                        226, 228, 219, 229, 236, 236, 238, 227, 215, 164, 128, 118, 68],
                       [42, 98, 117, 117, 195, 214, 225, 230, 227, 226, 233, 229, 222,
                        224, 231, 224, 226, 234, 238, 243, 231, 225, 181, 129, 120, 98],
                       [51, 104, 116, 124, 206, 205, 225, 231, 230, 231, 236, 227, 223,
                        230, 235, 222, 227, 236, 241, 242, 231, 227, 190, 124, 115, 113],
                       [66, 110, 117, 124, 217, 214, 230, 238, 238, 237, 237, 232, 236,
                        237, 239, 234, 239, 246, 243, 245, 236, 232, 196, 121, 115, 115],
                       [73, 110, 117, 119, 216, 223, 230, 239, 239, 238, 238, 234, 238,
                        238, 239, 240, 241, 244, 242, 244, 236, 233, 194, 122, 116, 116],
                       [67, 111, 116, 109, 205, 233, 232, 240, 242, 245, 242, 238, 236,
                        234, 235, 235, 239, 244, 239, 243, 234, 223, 172, 118, 115, 115],
                       [51, 109, 116, 99, 186, 233, 231, 237, 242, 247, 243, 239, 235,
                        233, 234, 239, 239, 244, 237, 243, 232, 209, 150, 115, 116, 104],
                       [41, 106, 116, 107, 139, 224, 228, 246, 239, 250, 244, 244, 242,
                        244, 243, 248, 240, 245, 233, 236, 216, 150, 127, 116, 117, 72],
                       [39, 78, 111, 116, 113, 168, 223, 242, 234, 245, 241, 243, 240,
                        242, 240, 245, 237, 242, 228, 224, 198, 114, 114, 116, 100, 44],
                       [38, 26, 89, 114, 118, 102, 165, 235, 220, 240, 233, 244, 232,
                        240, 233, 240, 227, 234, 213, 208, 152, 107, 115, 110, 68, 38],
                       [37, 21, 48, 91, 115, 100, 117, 206, 213, 234, 226, 242, 226,
                        236, 227, 240, 222, 230, 185, 178, 112, 110, 105, 84, 41, 32],
                       [37, 32, 25, 66, 87, 112, 117, 104, 152, 182, 198, 223, 208,
                        221, 206, 204, 183, 135, 136, 98, 107, 108, 75, 47, 32, 31],
                       [37, 31, 29, 47, 44, 78, 99, 111, 104, 134, 125, 165, 154,
                        175, 142, 143, 112, 110, 107, 89, 93, 77, 41, 39, 33, 31],
                       [37, 30, 30, 28, 34, 31, 60, 88, 95, 107, 113, 116, 115,
                        114, 115, 117, 108, 104, 92, 69, 58, 32, 33, 33, 32, 33],
                       [39, 32, 32, 32, 32, 34, 30, 51, 51, 78, 85, 90, 88,
                        88, 88, 93, 79, 74, 47, 46, 38, 37, 40, 40, 37, 42],
                       [44, 40, 40, 40, 39, 42, 43, 42, 43, 43, 43, 44, 44,
                        45, 43, 43, 43, 44, 45, 48, 49, 50, 48, 47, 45, 57],
                       [50, 47, 46, 45, 47, 50, 51, 50, 49, 48, 46, 46, 46,
                        47, 45, 46, 44, 49, 53, 54, 55, 54, 52, 48, 48, 67]], dtype=float)
    kernel = kernel - (kernel.mean())
    kernel = kernel / (kernel.max() - kernel.min())
    return kernel


def create_kernel21():
    kernel = np.array([[56, 50, 46, 43, 41, 41, 40, 39, 38, 38, 39, 40, 40, 38, 38, 37, 37, 36, 39, 51, 59, 63],
                       [56, 50, 42, 38, 38, 37, 36, 38, 40, 44, 47, 49, 47, 43, 40, 37, 35, 35, 38, 50, 61, 66],
                       [55, 45, 37, 34, 32, 29, 46, 58, 71, 81, 79, 80, 85, 87, 83, 63, 46, 38, 33, 49, 62, 67],
                       [55, 45, 36, 39, 37, 58, 84, 103, 113, 128, 144, 145, 137, 129, 111, 96, 84, 68, 50, 50, 64, 69],
                       [56, 47, 35, 36, 62, 87, 100, 112, 129, 145, 165, 182, 188, 180, 171, 140, 110, 104, 73, 56, 66,
                        71],
                       [58, 48, 38, 64, 91, 119, 125, 150, 170, 194, 211, 218, 222, 220, 216, 177, 123, 113, 104, 78,
                        66, 71],
                       [61, 50, 52, 90, 112, 137, 150, 210, 225, 222, 231, 239, 242, 241, 231, 204, 155, 121, 116, 97,
                        73, 70],
                       [62, 52, 78, 108, 128, 146, 181, 223, 223, 223, 234, 239, 240, 240, 226, 212, 180, 137, 116, 107,
                        83, 69],
                       [62, 53, 98, 117, 136, 154, 202, 226, 226, 214, 227, 232, 234, 236, 219, 211, 191, 144, 115, 113,
                        89, 68],
                       [62, 53, 97, 116, 141, 163, 211, 226, 220, 207, 201, 216, 236, 238, 219, 210, 192, 146, 115, 117,
                        90, 60],
                       [62, 53, 99, 117, 137, 169, 212, 223, 205, 189, 206, 218, 241, 242, 221, 210, 189, 143, 115, 116,
                        86, 52],
                       [63, 53, 95, 116, 130, 166, 203, 219, 222, 220, 231, 233, 244, 241, 216, 207, 181, 134, 115, 109,
                        77, 48],
                       [64, 53, 79, 109, 131, 166, 197, 207, 228, 229, 236, 239, 241, 227, 206, 213, 168, 119, 118, 98,
                        62, 48],
                       [65, 53, 57, 96, 124, 152, 186, 208, 224, 225, 224, 227, 225, 213, 210, 205, 150, 110, 111, 78,
                        52, 53],
                       [65, 53, 36, 60, 102, 120, 155, 170, 216, 226, 220, 199, 194, 189, 184, 159, 113, 103, 81, 52,
                        52, 57],
                       [68, 54, 36, 118, 118, 118, 118, 124, 149, 186, 198, 181, 155, 143, 135, 116, 90, 80, 53, 42, 54,
                        60],
                       [76, 62, 43, 40, 41, 58, 87, 102, 113, 122, 137, 133, 119, 113, 106, 86, 65, 52, 45, 48, 62, 73],
                       [93, 70, 48, 42, 39, 37, 51, 59, 71, 69, 71, 70, 72, 72, 66, 49, 41, 41, 39, 61, 83, 97],
                       [93, 80, 66, 57, 50, 46, 42, 41, 42, 44, 47, 48, 46, 45, 47, 50, 53, 57, 71, 90, 90, 90]],
                      dtype=float)
    kernel = kernel - (kernel.mean())
    kernel = kernel / (kernel.max() - kernel.min())
    return kernel


def create_kernel10():
    filter_kernel = np.array([[-3.5, -2.25, -2, -2, -2],
                              [-2.25, -1, 1 / 4, 1 / 2, 1],
                              [-2, 1 / 4, 1, 1, 1.25],
                              [-2, 1 / 2, 1, 2, 3],
                              [-2, 1, 1.25, 3, 4]])
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
    kernel = kernel - (kernel.mean())
    kernel = kernel / (kernel.max() - kernel.min())
    return kernel


def create_kernel3():
    kernel = np.array([[-1 / 9, -1 / 9, -1 / 9],
                       [-1 / 9, 8 / 9, -1 / 9],
                       [-1 / 9, -1 / 9, -1 / 9]], dtype=float)
    return kernel


def find_tfl_lights(c_image: np.ndarray, fig_ax, **kwargs):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """
    threshold = 0.3
    c_image = ndimage.gaussian_filter(c_image, sigma=1)

    after_filter = c_image
    # kernels = [create_kernel3(), create_kernel5(), create_kernel10(), create_kernel21(), create_kernel25()]
    kernels = [create_kernel3(), create_kernel10()]

    for kernel in kernels:
        after_filter = sg.convolve2d(after_filter, kernel, boundary="symm", mode="same")
        after_filter = after_filter / (after_filter.max() - after_filter.min())

    # fig_ax.imshow(after_filter)
    # fig_ax.set_title('filter')

    return non_max_suppression(after_filter, threshold)


def non_max_suppression(after_filter, threshold):
    data_max = maximum_filter(after_filter, 35)
    maxima = (after_filter == data_max)
    after_filter[maxima == False] = 0
    after_filter[after_filter < threshold] = 0
    slices = np.argwhere(after_filter > 0)
    x, y = [], []
    for dy, dx in slices:
        x.append(dx)
        y.append(dy)
    # print(len(x))
    return x, y


def non_max_suppression2(after_filter, threshold):
    threshold = 0.25 # no
    data_max = maximum_filter(after_filter, 75)
    maxima = (after_filter == data_max)
    data_min = minimum_filter(after_filter, 75)
    diff = ((data_max - data_min) > threshold)
    maxima[diff == 0] = 0

    labeled, num_objects = ndimage.label(maxima)
    slices = ndimage.find_objects(labeled)
    x, y = [], []
    for dy, dx in slices:
        x_center = (dx.start + dx.stop - 1) / 2
        x.append(int(x_center))
        y_center = (dy.start + dy.stop - 1) / 2
        y.append(int(y_center))
    print(len(x))
    return x, y


def show_image_and_gt(image, objs, fig_num=None):
    # plt.imshow(image)
    # plt.subplot()
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
    # red_image = np.array(color_image[:, :, 0])
    # red_image = red_image / 255
    # green_image = color_image[:, :, 1]
    # # green_image /= 255

    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]

    show_image_and_gt(image, objects, fig_num)
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
        blue_val = color_image[y, x, 2]


        if red_val >= green_val:
            ax2.plot(x, y, 'r+', color='r', markersize=5)
        else:
            ax2.plot(x, y, 'g+', color='g', markersize=7)


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
    default_base = './data/leftImg8bit/train/aachen'
    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))
    counter = 21
    for image in flist:
        if counter <=0 :
            break
        counter-=1
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None


        test_find_tfl_lights(image, json_fn)
        # plt.show(block=True)

    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")
    plt.show(block=True)


if __name__ == '__main__':
    main()
