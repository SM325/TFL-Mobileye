import json
from PIL import Image
import numpy as np
import pickle

from TFL_Man import TFL_Man


class Controller:
    def __init__(self):
        with open('frames_list.json', 'r') as j:
            loaded_json = j.read()
            frames_data = json.loads(loaded_json)
        self.pkl_path = frames_data["pkl"]
        self.frames_list = frames_data["frames"]

        with open(self.pkl_path, 'rb') as pklfile:
            pkl_data = pickle.load(pklfile, encoding='latin1')

        self.tfl_man = TFL_Man(pkl_data)

    def run_managers(self):
        for i, frame_path in enumerate(self.frames_list):
            frame_img = np.asarray(Image.open(frame_path))
            self.tfl_man.run(i, frame_img)


if __name__ == '__main__':
    controller = Controller()
    controller.run_managers()
