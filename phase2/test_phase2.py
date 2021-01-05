from phase2 import *


# from tensorflow.keras.models import load_model
# loaded_model = load_model("model_final.h5")
#
#
# def viz_my_data(images,labels, predictions=None, num=(5,5), labels2name= {0:'No TFL',1:'Yes TFL'}):
#     assert images.shape[0] == labels.shape[0]
#     assert predictions is None or predictions.shape[0] == images.shape[0]
#     h = 5
#     n = num[0]*num[1]
#     ax = plt.subplots(num[0],num[1],figsize=(h*num[0],h*num[1]),gridspec_kw={'wspace':0.05},squeeze=False,sharex=True,sharey=True)[1]#.flatten()
#     idxs = np.random.randint(0,images.shape[0],n)
#     # j = 0
#     for i,idx in enumerate(idxs):
#       # if((labels[idx] == 0 and predictions[idx] > 0.5) or (labels[idx] == 1 and predictions[idx] < 0.5)):
#       ax.flatten()[i].imshow(images[idx])
#       title = labels2name[labels[idx]]
#       if predictions is not None : title += ' Prediction: {:.2f}'.format(predictions[idx])
#       ax.flatten()[i].set_title(title)
#         # j+=1
#
#
#
# viz_my_data(num=(6,6),predictions=predictions[:,1],**val);


def main():
        ground_truth_base = './data/leftImg8bit/test'
        flist_gt = glob.glob(os.path.join(ground_truth_base,'*', '*_leftImg8bit.png'))
        data_list = []
        for gt_path in flist_gt:
            try:
                ylist, xlist = test_find_tfl_lights(gt_path)
                orginal_img = np.array(Image.open(gt_path))

                for coor in zip(xlist, ylist):
                    croped_image = crop_img_by_center(orginal_img, coor)
                    data_list.append(croped_image)
                    # plt.imshow(croped_image)
                    # plt.show()
            except:
                print("error in file", gt_path)
        np.array(data_list).tofile('./Data_dir/test' + '/data.bin')



if __name__ == '__main__':
    main()
    print("end")
