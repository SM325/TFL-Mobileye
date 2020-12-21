from phase1 import *

def test_find_tfl_lights(path_img):
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
    x_all = x_green + x_red_
    y_all = y_green + y_red_
    return x_all, y_all


def is_contain_tfl_by_img(labled_img):
    # labled_img np.array
    # path_ = './data/gtFine/train/aachen/aachen_000010_000019_gtFine_labelIds.png'
    # labled_img = np.array(Image.open(path_))
    return 19 in labled_img.flatten()


def is_contain_tfl_by_img_and_cord(labled_img, cord):
    path_ = './data/gtFine/train/aachen/aachen_000010_000019_gtFine_labelIds.png'
    labled_img = np.array(Image.open(path_))
    return labled_img[cord[0], cord[1]] == 19


def main(argv=None):
    original_images_base = './data/leftImg8bit'
    ground_truth_base = './data/gtFine'

    flist = glob.glob(os.path.join(original_images_base,'train/aachen', '*_leftImg8bit.png'))

    for image in flist:
        picture = np.array(Image.open(image)) # uint8 pic
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')
        if not os.path.exists(json_fn):
            json_fn = None
        # print(test_find_tfl_lights(image))
    # default_base = './data'
    # flist = glob.glob(os.path.join(default_base, '*_leftImg8bit.png'))
    #
    # for image in flist:
    #     test_find_tfl_lights(image)
    #     plt.show(block=True)


if __name__ == '__main__':
    # main()
    is_contain_tfl_by_img("s")
