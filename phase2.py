from phase1 import *


def test_find_tfl_lights(path_img):
    picture = np.array(Image.open(path_img)).astype(float) / 255
    highpass_filter_green = high_pass_filter_green(picture)
    highpass_filter_red = high_pass_filter_red(picture)
    x_green, y_green = recognize_traffic_light(highpass_filter_green)
    x_red, y_red = recognize_traffic_light(highpass_filter_red)
    picture2 = np.array(Image.open(path_img))
    # x_red_, y_red_ = [], []
    # for i in range(len(x_red)):
    #     if (x_red[i] not in x_green and not y_red[i] in y_green):
    #         x_red_.append(x_red[i])
    #         y_red_.append(y_red[i])
    x_red_, y_red_ = [], []
    for i in range(len(x_red)):
        left = x_red[i] - 75
        right = x_red[i] + 75
        top = y_red[i] - 75
        bottom = y_red[i] + 75
        to_append = True
        for x_ind in range(left, right):
            for y_ind in range(top, bottom):
                if (x_ind in x_green and y_ind in y_green):
                    to_append = False

        if to_append:
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
    left = cord[1] - 40
    top = cord[0] - 40
    right = cord[1] + 41
    bottom = cord[0] + 41
    return np.array(Image.fromarray(img).crop((left, top, right, bottom)))


def get_separated_coor(img_path, gt_img):
    ylist, xlist = test_find_tfl_lights(img_path)
    true_list = []
    false_list = []
    for coor in zip(xlist, ylist):
        if is_contain_tfl_by_img_and_cord(gt_img, coor):
            true_list.append(coor)
        else:
            false_list.append(coor)

    return true_list, false_list


def senty_check(data_list, lable_list):
    print(lable_list)
    plt.figure()
    for i in range(min(25, len(data_list))):
        plt.subplot(5, 5, i + 1).imshow(data_list[i])
        plt.subplot(5, 5, i + 1).set_title(lable_list[i])
    plt.show(block=True)


def crop_and_labled(true_list, false_list, orginal_img):
    data_list = []
    lable_list = []
    for coor in true_list:
        croped_image = crop_img_by_center(orginal_img, coor)
        data_list.append(croped_image)
        lable_list.append(1)
    for i in range(len(true_list)):
        croped_image = crop_img_by_center(orginal_img, false_list[i])
        data_list.append(croped_image)
        lable_list.append(0)

    return data_list, lable_list


def main():
    second_dirs = {"train", "val"}
    for second_dir in second_dirs:
        ground_truth_base = './data/gtFine'
        flist_gt = glob.glob(os.path.join(ground_truth_base, second_dir, '*', '*_gtFine_labelIds.png'))

        data_list_all = []
        lable_list_all = []

        for gt_path in flist_gt:
            picture_gt = np.array(Image.open(gt_path))
            if is_contain_tfl_by_img(picture_gt):
                print(gt_path)
                orginal_path = get_img_path_from_gt(gt_path)
                if not os.path.exists(orginal_path):
                    continue
                orginal_img = np.array(Image.open(orginal_path))

                true_list, false_list = get_separated_coor(orginal_path, picture_gt)

                data_list, lable_list = crop_and_labled(true_list, false_list, orginal_img)

                data_list_all = data_list_all + data_list
                lable_list_all = lable_list_all + lable_list

        save_bin(data_list_all, lable_list_all, second_dir)


def save_bin(data_list_all, lable_list_all, second_dir):
    np.array(data_list_all).tofile('./Data_dir/' + second_dir + '/data.bin')
    np.array(lable_list_all).astype('uint8').tofile('./Data_dir/' + second_dir + '/labels.bin')


if __name__ == '__main__':
    main()
    print("end")
