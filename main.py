from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
import time

grid1 = Grid(x_room = 200, y_room = 300, z_room = 200)
mic_position = np.array([100,70,0])
sound_source_positions = np.array([[20,250,180],[100,210,180],[185,180,180],[110,90,180],[170,85,100],
[20,170,180],[190,100,100],[120,250,60],[85,160,60],[100,100,60]])
posicion_estimada = np.zeros((10,3))

grid1.place_mic_array(mic_position)

for i in range(0, 10):
    start = time.time()                     # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    signal, fs = grid1.place_sound_source('trumpet.wav', sound_source_positions[i])
    posicion_estimada[i] = grid1.SRP(signal, grid1.Mic_Array, fs)
    end = time.time()                                                   # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    print ("\ncoste computacional: "+str(end-start))                    # PARA CALCULAR TIEMPO; BORRAR AL FINAL

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Points in Space")
ax.set_xlim([0, grid1.x_room-1])
ax.set_ylim([0, grid1.y_room-1])
ax.set_zlim([0, grid1.z_room-1])

ax.scatter(sound_source_positions[:,0], sound_source_positions[:,1],  sound_source_positions[:,2])
ax.scatter(mic_position[0], mic_position[1], mic_position[2])
ax.scatter(posicion_estimada[:,0], posicion_estimada[:,1], posicion_estimada[:,2])

label_original = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
label_estimation = ['1\' ', '2\' ', '3\' ', '4\' ', '5\' ', '6\' ', '7\' ', '8\' ', '9\' ', '10\' ']

for i, txt in enumerate(label_original):
    ax.text(sound_source_positions[i],sound_source_positions[i],sound_source_positions[i],  '%s' % (txt))
    ax.text(posicion_estimada[i],posicion_estimada[i],posicion_estimada[i],  '%s' % label_estimation[i])

plt.show()