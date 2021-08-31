import numpy as np
import math

class MicArray:
    def __init__(
        self,
        center = np.array([0,0,0]),
        distance_to_center = 30,
        mics_n = 6

    ):
        self.center = center
        self.distance_to_center = distance_to_center
        self.mics_n = mics_n

        self.mic_position = np.zeros((mics_n,3))

        for  i in range(0, mics_n):
            x = math.sin((i*math.pi)/3)*distance_to_center + center[0]
            y = math.cos((i*math.pi)/3)*distance_to_center + center[1]
            self.mic_position[i, :] = [x, y , center[2]]

        self.mic_position[abs(self.mic_position) < 1e-14] = 0

