import numpy as np

SOUND_SPEED = 34300
NUMBER_OF_MICROPHONES = 6


def GCC(
    correlated,
    corners_to_check,
    mic_position,
    fs = 44100,
):
    potencia = 0
    if isinstance(correlated, np.ndarray):
        n=0
        for i in range(0, NUMBER_OF_MICROPHONES-1):
            for j in range (i+1, NUMBER_OF_MICROPHONES):
                for corner in corners_to_check:
                    tau = -round(fs*(np.linalg.norm(corner-mic_position[i]) -
                    np.linalg.norm(corner-mic_position[j]))/SOUND_SPEED)

                    if((corner == corners_to_check[0]).all()):
                        tau_min = tau_max = tau

                    if tau < -(correlated[n].size):
                        tau = tau + correlated[n].size
                    if tau < 0:
                        tau = tau-1

                    if tau < tau_min:
                        tau_min = tau
                    if tau > tau_max:
                        tau_max = tau

                for k in range(int(tau_min), int(tau_max)+1):
                    potencia += np.real(correlated[n][k])

                n = n + 1

        return potencia

    else:
        print("Correlated debe ser del tipo numpy.ndarray")
        return None