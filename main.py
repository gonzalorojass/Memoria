from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt
import time

grid1 = Grid(x_room = 200, y_room = 300, z_room = 200)
mic_position = np.array([100,10,0])
sound_source_positions = np.array([[100,150,100],[180,290,190],[20,184,20],[35,195,125],[165,120,50]])
posicion_estimada = np.zeros((5,3))

grid1.place_mic_array(mic_position)

for i in range(0, 5):
    start = time.time()                     # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    signal, fs = grid1.place_sound_source('trumpet.wav', sound_source_positions[i])
    useless, posicion_estimada[i] = grid1.HSRP(signal,"room", fs)
    grid1.reset_tree()  
    end = time.time()                                                   # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    print ("\ncoste computacional: "+str(end-start))                    # PARA CALCULAR TIEMPO; BORRAR AL FINAL

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Puntos en el espacio")
ax.set_xlim([0, grid1.dimensiones[0]])
ax.set_ylim([0, grid1.dimensiones[1]])
ax.set_zlim([0, grid1.dimensiones[2]])

ax.scatter(sound_source_positions[:,0], sound_source_positions[:,1],  sound_source_positions[:,2])
ax.scatter(mic_position[0], mic_position[1], mic_position[2])
ax.scatter(posicion_estimada[:,0], posicion_estimada[:,1], posicion_estimada[:,2])

label_original = ['1', '2', '3', '4', '5']
label_estimation = ['1\' ', '2\' ', '3\' ', '4\' ', '5\' ']

print("Posicion estimada: ")
print(posicion_estimada)

print("Posicion Fuente: ")
print(sound_source_positions)

ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('z [cm]')

for i, txt in enumerate(label_original):
    ax.text(sound_source_positions[i][0],sound_source_positions[i][1],sound_source_positions[i][2],  '%s' % (txt))
    ax.text(posicion_estimada[i][0],posicion_estimada[i][1],posicion_estimada[i][2],  '%s' % label_estimation[i])

plt.show()