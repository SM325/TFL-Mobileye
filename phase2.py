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


def main():
    ground_truth_base = './data/gtFine'
    flist_gt = glob.glob(os.path.join(ground_truth_base, 'train/*', '*_gtFine_labelIds.png'))
    print(flist_gt)

    for gt_path in flist_gt:
        plt.figure()
        ax1 = plt.subplot(211)
        ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)

        image_path = gt_path.replace('_gtFine_labelIds.png', '_leftImg8bit.png')
        image_path = image_path.replace('gtFine', 'leftImg8bit')

        picture = np.array(Image.open(image_path))
        ax1.imshow(picture)

        picture_gt = np.array(Image.open(gt_path))
        ax2.imshow(picture_gt)

        plt.show(block=True)


if __name__ == '__main__':
    # main()
    is_contain_tfl_by_img("s")
