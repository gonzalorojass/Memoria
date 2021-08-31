import numpy as np
from Mic_array import *

c = 34300

def GCC(
    correlated,
    position_to_check,
    mic_array: MicArray,
    fs = 44100,
):
    potencia = 0
    if isinstance(correlated, np.ndarray):
        if (position_to_check[1] < mic_array.center[1]+mic_array.distance_to_center) or (position_to_check[2] < mic_array.center[2]):
            potencia = 0
    
        else:
            n=0
            for i in range(0, mic_array.mics_n-1):
                for j in range (i+1, mic_array.mics_n):

                    tau = -round(fs*(np.linalg.norm(position_to_check-mic_array.mic_position[i]) -
                    np.linalg.norm(position_to_check-mic_array.mic_position[j]))/c)

                    if tau < -(correlated[n].size):
                        tau = tau + correlated[n].size

                    if tau < 0:
                        tau = tau-1

                    potencia += np.real(correlated[n][tau])

                    n = n + 1
                    if(n == 15):
                        n=0

        return potencia
    else:
        print("Correlated debe ser del tipo numpy.ndarray")
        return None