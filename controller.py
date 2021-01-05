import json
from PIL import Image
import numpy as np
import pickle
import matplotlib.pyplot as plt


import phase1
import phase2
import part3.SFM

class FrameContainer(object):
    def __init__(self, img_path):
        self.img = np.asarray(Image.open(img_path))
        self.suspicious_points_of_light =[]
        self.traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


class TFL_Man(object):
    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        self.Principal_point = data['principle_point']
        self.focal_len = data['flx']
        self.prev_container = None
        self.curr_container = None
        self.EM = [(i+1, data['egomotion_' + str(i) + '-' + str(i + 1)]) for i in range(24, 29)]

    def run(self, i, frame_path):
        self.prev_container = self.curr_container
        self.curr_container = FrameContainer(frame_path)

        # part 1
        self.curr_container.suspicious_points_of_light = phase1.find_tfl_lights(self.curr_container.img)
        # self.plot_part1()

        # part 2
        candidates, auxiliary = self.curr_container.suspicious_points_of_light
        self.curr_container.traffic_light = phase2.get_tfl_candidates(self.curr_container.img, candidates, auxiliary)

        # part 3

        if self.prev_container:
            #part3
            pass


    def plot_part1(self):
        candidates, auxiliary = self.curr_container.suspicious_points_of_light
        plt.imshow(self.curr_container.img)
        for i, coord in enumerate(candidates):
            if auxiliary[i] == "red":
                plt.plot(coord[0], coord[1], 'r.')
            else:
                plt.plot(coord[0], coord[1], 'g.')
        plt.show()






def main():
    with open('frames_list.json', 'r') as j:
        loaded_json = j.read()
        frames_data = json.loads(loaded_json)
    pkl_path = frames_data["pkl"]
    frames_list = frames_data["frames"]

    tfl_man = TFL_Man(pkl_path)
    for i, frame_path in enumerate(frames_list):
        tfl_man.run(i, frame_path)

    print("end")





if __name__ == '__main__':
    main()
