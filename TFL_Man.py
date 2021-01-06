import numpy as np
import matplotlib.pyplot as plt
from timebudget import timebudget

import phase1
import phase2
import phase3


class FrameContainer(object):
    def __init__(self, img):
        self.img = img
        self.suspicious_points_of_light = []
        self.suspicious_points_auxiliary = []
        self.traffic_light = []
        self.traffic_light_auxiliary = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []


class TFL_Man(object):
    def __init__(self, data):
        self.principal_point = data['principle_point']
        self.focal_len = data['flx']
        self.prev_container = None
        self.curr_container = None
        self.EM_matrixs = dict()
        for i in range(24, 29):
            self.EM_matrixs[i + 1] = data['egomotion_' + str(i) + '-' + str(i + 1)]

    def run(self, i, frame_img):
        timebudget.report_at_exit() 
        self.prev_container = self.curr_container
        self.curr_container = FrameContainer(frame_img)

        self.run_candidates()  # part 1
        self.run_traffic_light_detection()  # part 2
        self.run_find_distance(i)  # part 3

        self.view(i)

    @timebudget
    def run_find_distance(self, i):
        if self.prev_container:
            self.curr_container.EM = self.EM_matrixs[i + 24]
            corresponding_ind, traffic_lights_3d_location, valid = phase3.calc_TFL_dist(
                self.prev_container.traffic_light,
                self.curr_container.traffic_light, self.curr_container.EM,
                self.focal_len, self.principal_point)
            if corresponding_ind is not None and traffic_lights_3d_location is not None and valid is not None:
                self.curr_container.corresponding_ind, self.curr_container.traffic_lights_3d_location, self.curr_container.valid = corresponding_ind, traffic_lights_3d_location, valid

    @timebudget
    def run_traffic_light_detection(self):
        candidates = self.curr_container.suspicious_points_of_light
        auxiliary = self.curr_container.suspicious_points_auxiliary
        traffic_light = phase2.get_tfl_candidates(self.curr_container.img, candidates, auxiliary)
        self.curr_container.traffic_light = np.array(traffic_light[0])
        self.curr_container.traffic_light_auxiliary = np.array(traffic_light[1])

    @timebudget
    def run_candidates(self):
        self.curr_container.suspicious_points_of_light, self.curr_container.suspicious_points_auxiliary = phase1.find_tfl_lights(
            self.curr_container.img)

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
