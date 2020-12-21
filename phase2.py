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
    return 19 in labled_img.flatten()


def is_contain_tfl_by_img_and_cord(labled_img, cord):
    return labled_img[cord[0], cord[1]] == 19

def get_img_path_from_gt(gt_path):
    image_path = gt_path.replace('_gtFine_labelIds.png', '_leftImg8bit.png')
    return image_path.replace('gtFine', 'leftImg8bit')


def crop_img_by_center(img, cord):
    # get np.array return image
    height, width, _ = img.shape
    left = cord[0] - 40
    top = cord[1] - 40
    right = cord[0] + 41
    bottom = cord[1] + 41
    return Image.fromarray(img).crop((left, top, right, bottom))


def main():
    ground_truth_base = './data/gtFine'
    flist_gt = glob.glob(os.path.join(ground_truth_base, 'train/*', '*_gtFine_labelIds.png'))
    print(flist_gt)

    for gt_path in flist_gt:
        picture_gt = np.array(Image.open(gt_path))
        if is_contain_tfl_by_img(picture_gt):
           orginal_img = np.array(Image.open(get_img_path_from_gt(gt_path)))

           # plt.figure()
           # ax1 = plt.subplot(211)
           # ax2 = plt.subplot(212, sharex=ax1, sharey=ax1)
           # 
           # picture = np.array(Image.open(image_path))
           # ax1.imshow(picture)
           #
           # ax2.imshow(picture_gt)
           plt.show(block=True)


if __name__ == '__main__':
    main()
    plt.imshow(crop_img_by_center(0, (2048, 200)))
    print("end")
