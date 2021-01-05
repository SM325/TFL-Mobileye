import json
from PIL import Image
import numpy as np
import pickle
import matplotlib.pyplot as plt


import phase1
import phase2
import phase3 as phase3

class FrameContainer(object):
    def __init__(self, img_path):
        self.img = np.asarray(Image.open(img_path))
        self.suspicious_points_of_light =[]
        self.suspicious_points_auxiliary =[]
        self.traffic_light = []
        self.traffic_light_auxiliary = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


class TFL_Man(object):
    def __init__(self, pkl_path):
        with open(pkl_path, 'rb') as pklfile:
            data = pickle.load(pklfile, encoding='latin1')
        self.principal_point = data['principle_point']
        self.focal_len = data['flx']
        self.prev_container = None
        self.curr_container = None
        self.EM_matrixs = dict()
        for i in range(24, 29):
            self.EM_matrixs[i+1] = data['egomotion_' + str(i) + '-' + str(i + 1)]
        # self.EM = [(i+1, data['egomotion_' + str(i) + '-' + str(i + 1)]) for i in range(24, 29)]

    def run(self, i, frame_path):
        self.prev_container = self.curr_container
        self.curr_container = FrameContainer(frame_path)

        # part 1
        self.curr_container.suspicious_points_of_light,  self.curr_container.suspicious_points_auxiliary = phase1.find_tfl_lights(self.curr_container.img)
        # self.plot_part_x(1)

        # part 2
        candidates = self.curr_container.suspicious_points_of_light
        auxiliary = self.curr_container.suspicious_points_auxiliary
        traffic_light = phase2.get_tfl_candidates(self.curr_container.img, candidates, auxiliary)
        self.curr_container.traffic_light = np.array(traffic_light[0])
        self.curr_container.traffic_light_auxiliary = np.array(traffic_light[1])
        # self.plot_part_x(2)

        # part 3
        if self.prev_container:
            self.curr_container.EM = self.EM_matrixs[i+24]
            self.curr_container = phase3.calc_TFL_dist(self.prev_container, self.curr_container, self.focal_len, self.principal_point)

        self.view(i)

    def view(self, i):
        plt.suptitle('frame #' + str(i))
        part1 = plt.subplot(222)
        part2 = plt.subplot(221)
        part3 = plt.subplot(212)
        self.plot_part_x(1, part1)
        self.plot_part_x(2, part2)
        if self.prev_container:
            self.plot_part_x(3, part3)
        plt.show()

    def plot_part_x(self, part_num, subplot):
        if part_num != 3:
            if part_num == 1:
                subplot.set_title('candidates')
                candidates = self.curr_container.suspicious_points_of_light
                auxiliary = self.curr_container.suspicious_points_auxiliary
            elif part_num == 2:
                subplot.set_title('traffic light')
                candidates = self.curr_container.traffic_light
                auxiliary = self.curr_container.traffic_light_auxiliary
            subplot.imshow(self.curr_container.img)
            for i, coord in enumerate(candidates):
                if auxiliary[i] == "red":
                    subplot.plot(coord[0], coord[1], 'r.')
                else:
                    subplot.plot(coord[0], coord[1], 'g.')
        else:
            subplot.set_title('distance')
            subplot.imshow(self.curr_container.img)
            curr_p = self.curr_container.traffic_light
            subplot.plot(curr_p[:, 0], curr_p[:, 1], 'b+')

            for i in range(len(curr_p)):
                if self.curr_container.valid[i]:
                    subplot.text(curr_p[i, 0], curr_p[i, 1],
                                 r'{0:.1f}'.format(self.curr_container.traffic_lights_3d_location[i, 2]), color='r',
                                 size=12)



#controller -class
def main():
    with open('frames_list.json', 'r') as j:
        loaded_json = j.read()
        frames_data = json.loads(loaded_json)
    pkl_path = frames_data["pkl"]
    frames_list = frames_data["frames"]

    tfl_man = TFL_Man(pkl_path) #send the pkl and not path
    for i, frame_path in enumerate(frames_list):
        tfl_man.run(i, frame_path) # send the farne and not phath

    print("end")





if __name__ == '__main__':
    main()
