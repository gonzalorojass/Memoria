from Grid import *
from Mic_array import *
from GCC import *
from Camara import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import timeit                            # PARA CALCULAR TIEMPO

NUMBER_OF_MICROPHONES = 6
####    INICIALIZACIÓN DE GRILLA     ####

grid1 = Grid.Grid(x_room = 305, y_room = 376, z_room = 235)
camara = Camara(np.array([108,0,80]))
mic_position = np.array([1058,10,80])
posicion_estimada = np.zeros(3)

###     INICIALIZACION GRAFICOS     ####

plt.ion()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, grid1.dimensiones[0]])
ax.set_ylim([0, grid1.dimensiones[1]])
ax.set_zlim([0, grid1.dimensiones[2]])

sc = ax.scatter(0,0,0)
ax.scatter(mic_position[0], mic_position[1], mic_position[2])


####    ESCUCHA DEL MICROFONO        ####

RESPEAKER_RATE = 44100
CHUNK = 44100
RESPEAKER_CHANNELS = 8

to_check = np.zeros((8))
not_mic = np.array([0,1])
mic_data = np.zeros((6, CHUNK))

input("Press Enter to start")

with MicArray(grid=grid1, center=mic_position, rate = RESPEAKER_RATE, chunk_size = CHUNK) as mic:
    for chunk in mic.read_chunks():

        start = timeit.default_timer()      # Calculo tiempo

        for i in range(RESPEAKER_CHANNELS):
            to_check[i] = np.max(chunk[i::8])

        if((not_mic != np.argpartition(to_check, 2)[0:2]).all()):
            not_mic = np.argpartition(to_check, 2)[0:2]
            channel_0 = np.max(not_mic)+1

        for i in range(0, 6):
            mic_data[i] = chunk[(i+channel_0 if (i+channel_0 <= 7) else channel_0-8+i)::8]

        invXi_Xj = np.zeros((sum(range(NUMBER_OF_MICROPHONES)), chunk[0::8].size))
        n = 0
        for i in range(0, NUMBER_OF_MICROPHONES-1):
            for j in range (i+1, NUMBER_OF_MICROPHONES):
                
                Xi_Xj = np.fft.rfft(mic_data[i], n = mic_data[i].size)*np.conj(np.fft.rfft(mic_data[j], n = mic_data[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = chunk[0::8].size)
                n += 1

        ignore, posicion_estimada = grid1.HSRP(invXi_Xj,"room", RESPEAKER_RATE)
        stop = timeit.default_timer()

        print('Time: ', stop - start)
        print(posicion_estimada)
        camara.point_at_location(posicion_estimada)
        grid1.reset_tree()

        sc._offsets3d = (np.array([posicion_estimada[0]]), np.array([posicion_estimada[1]]), np.array([posicion_estimada[2]]))
        plt.pause(0.1)
        plt.draw()

        fig.savefig('temp.png', dpi=fig.dpi)
    
        input("Press Enter to continue")