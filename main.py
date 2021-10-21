from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

import timeit                            # PARA CALCULAR TIEMPO

NUMBER_OF_MICROPHONES = 6
####    INICIALIZACIÓN DE GRILLA     ####

grid1 = Grid.Grid(x_room = 314, y_room = 422, z_room = 235)
mic_position = np.array([121,10,75])
posicion_estimada = np.zeros(3)

####    ESCUCHA DEL MICROFONO        ####

RESPEAKER_RATE = 44100
CHUNK = 1024*4

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, grid1.dimensiones[0]])
ax.set_ylim([0, grid1.dimensiones[1]])
ax.set_zlim([0, grid1.dimensiones[2]])

sc = ax.scatter(0,0,0)
ax.scatter(mic_position[0], mic_position[1], mic_position[2])

fig.show()

with MicArray(grid=grid1, center=mic_position, rate = RESPEAKER_RATE, chunk_size = CHUNK) as mic:
    for chunk in mic.read_chunks():

        start = timeit.default_timer()      # Calculo tiempo

        invXi_Xj = np.zeros((sum(range(NUMBER_OF_MICROPHONES)), chunk[0::8].size))
        n = 0
        for i in range(0, NUMBER_OF_MICROPHONES-1):
            for j in range (i+1, NUMBER_OF_MICROPHONES):
                Xi_Xj = np.fft.rfft(chunk[i::8], n = chunk[i::8].size)*np.conj(np.fft.rfft(chunk[j::8], n = chunk[j::8].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = chunk[0::8].size)
                n += 1

        ignore, posicion_estimada = grid1.HSRP(invXi_Xj,"room", RESPEAKER_RATE)
        stop = timeit.default_timer()

        print('Time: ', stop - start) 
        print(posicion_estimada)
        grid1.reset_tree()
    
        sc._offsets3d = (np.array([posicion_estimada[0]]), np.array([posicion_estimada[1]]), np.array([posicion_estimada[2]]))
        plt.pause(0.1)
        plt.draw()

