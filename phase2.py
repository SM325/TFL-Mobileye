from phase1 import *
from tensorflow.keras.models import load_model


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


def is_front_light(img_path, coor):
    # return True
    picture = np.array(Image.open(img_path))
    total_color =  1 / 8 * picture[coor[0] + 1, coor[1]] + 1 / 8 * picture[coor[0] - 1, coor[1]] + \
                  1 / 8 * picture[coor[0], coor[1] - 1] + 1 / 8 * picture[coor[0], coor[1] + 1] + 1 / 8 * picture[coor[0] + 1, coor[1] + 1] + 1 / 8 *\
                  picture[coor[0] - 1, coor[1] - 1] + \
                  1 / 8 * picture[coor[0] + 1, coor[1] - 1] + 1 / 8 * picture[coor[0] - 1, coor[1] + 1]

    if (total_color[0] > 255/2 or total_color[1] > 255/2 ):
        return True
    return False


def get_separated_coor(img_path, gt_img):
    ylist, xlist = test_find_tfl_lights(img_path) # here we change
    true_list = []
    false_list = []
    for coor in zip(xlist, ylist):
        # if is_contain_tfl_by_img_and_cord(gt_img, coor) and is_front_light(img_path, coor):
        if is_contain_tfl_by_img_and_cord(gt_img, coor):
            true_list.append(coor)
        else:
            false_list.append(coor)

    return true_list, false_list


def senty_check(data_list, lable_list):
    plt.figure()
    for i in range(min(25, len(data_list))):
        plt.subplot(5, 5, i + 1).imshow(data_list[i])
        plt.subplot(5, 5, i + 1).set_title(lable_list[i])
    plt.show(block=True)


def crop_and_labled(true_list, false_list, orginal_img):
    data_list = []
    lable_list = []
    if len(true_list) == 0:
        return [], []
    if len(false_list) >= len(true_list):
        for coor in true_list:
            croped_image = crop_img_by_center(orginal_img, coor)
            data_list.append(croped_image)
            lable_list.append(1)
        for i in range(int(len(true_list) * 1.1)):
            croped_image = crop_img_by_center(orginal_img, false_list[np.random.randint(0, len(false_list))])
            data_list.append(croped_image)
            lable_list.append(0)
    else:
        for coor in false_list:
            croped_image = crop_img_by_center(orginal_img, coor)
            data_list.append(croped_image)
            lable_list.append(0)
        for i in range(len(false_list)):
            croped_image = crop_img_by_center(orginal_img, true_list[np.random.randint(0, len(true_list))])
            data_list.append(croped_image)
            lable_list.append(1)

    return data_list, lable_list


def main_():
    second_dirs = ["test"]
    for second_dir in second_dirs:
        ground_truth_base = './data/gtFine'
        flist_gt = glob.glob(os.path.join(ground_truth_base, second_dir, '*', '*_gtFine_labelIds.png'))
        print(flist_gt[0])
        data_list_all = []
        lable_list_all = []
        for gt_path in flist_gt:
            try:
                picture_gt = np.array(Image.open(gt_path))
                if is_contain_tfl_by_img(picture_gt):
                    orginal_path = get_img_path_from_gt(gt_path)
                    if not os.path.exists(orginal_path):
                        continue
                    orginal_img = np.array(Image.open(orginal_path))

                    true_list, false_list = get_separated_coor(orginal_path, picture_gt)

                    data_list, lable_list = crop_and_labled(true_list, false_list, orginal_img)

                    data_list_all = data_list_all + data_list
                    lable_list_all = lable_list_all + lable_list
            except:
                print("error in file", gt_path)
        save_bin(data_list_all, lable_list_all, second_dir)


def save_bin(data_list_all, lable_list_all, second_dir):
    np.array(data_list_all).tofile('./Data_dir/' + second_dir + '/data.bin')
    np.array(lable_list_all).astype('uint8').tofile('./Data_dir/' + second_dir + '/labels.bin')


def get_tfl_candidates(img, candidates, auxiliary):
    res_cand =[]
    res_aux =[]
    for i, coord in enumerate(candidates):
        cropped_img = crop_img_by_center(img, (coord[1], coord[0]))
        if is_traffic_light(cropped_img):
            res_cand.append(coord)
            res_aux.append(auxiliary[i])

    return res_cand, res_aux

def is_traffic_light(cropped_img):
    loaded_model = load_model("model_final.h5")
    predictions = loaded_model.predict(np.array([cropped_img]))
    return np.argmax(predictions[0])


if __name__ == '__main__':
    main()
    print("end")
