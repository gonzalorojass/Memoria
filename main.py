from Grid import *
from Mic_array import *
from GCC import *
import matplotlib.pyplot as plt

grid1 = Grid(x_room = 200, y_room = 300, z_room = 200)
mic_position = np.array([100,20,0])
sound_source_positions = np.array([[100,150,100],[180,290,190],[20,85,20],[35,195,125],[165,95,50]])
posicion_estimada = np.zeros((5,3))
camera_position = np.array([100,0,0])

coste_comp = np.zeros(5)
direccion_fuente = np.zeros((5,2))
direccion_estimada = np.zeros((5,2))

grid1.place_mic_array(mic_position)

for i in range(0, 5):
    start = time.time()                     # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    signal, fs = grid1.place_sound_source('trumpet.wav', sound_source_positions[i])
    posicion_estimada[i] = grid1.SRP(signal, grid1.Mic_Array, fs)
    end = time.time()                                                   # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    print ("\ncoste computacional: "+str(end-start))                    # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    coste_comp[i] = end-start

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.set_title("Puntos en el espacio")
ax.set_xlim([0, grid1.x_room-1])
ax.set_ylim([0, grid1.y_room-1])
ax.set_zlim([0, grid1.z_room-1])

ax.scatter(sound_source_positions[:,0], sound_source_positions[:,1],  sound_source_positions[:,2],c='b')
ax.scatter(mic_position[0], mic_position[1], mic_position[2], c='g')
ax.scatter(posicion_estimada[:,0], posicion_estimada[:,1], posicion_estimada[:,2],c='r')

label_original = ['1', '2', '3', '4', '5']
label_estimation = ['1\' ', '2\' ', '3\' ', '4\' ', '5\' ']

print("Posicion estimada: ")
print(posicion_estimada)

print("Posicion Fuente: ")
print(sound_source_positions)

for j in range(0, 5):
    position_diff_f = sound_source_positions[j] - camera_position
    position_diff_e = posicion_estimada[j] - camera_position

    #FUENTE
    xy = position_diff_f[0]**2 + position_diff_f[1]**2
    if (position_diff_f[0] > 0):
        to_sum = 0
        print(to_sum)
    elif (position_diff_f[0] < 0) and (position_diff_f[1] >= 0):
        to_sum = math.pi
        print(to_sum)
    elif (position_diff_f[0] < 0) and (position_diff_f[1] < 0):
        to_sum = -math.pi
        print(to_sum)
    elif (position_diff_f[0] == 0) and (position_diff_f[1] > 0):
        to_sum = math.pi/2
        print(position_diff_f[0])
        print(to_sum)
    else:
        to_sum = -math.pi/2
        print(to_sum)

    if position_diff_f[0] == 0:
        azimuth = np.array([math.pi/2])
    else:
        azimuth = np.arctan(np.array([position_diff_f[1]/position_diff_f[0]])) + to_sum
    theta = np.arctan(np.array([position_diff_f[2]/np.sqrt(xy)]))
    direccion_fuente[j] = np.array([theta[0], azimuth[0]])

    #ESTIMADA
    xy_e = position_diff_e[0]**2 + position_diff_e[1]**2
    if (position_diff_e[0] > 0):
        to_sum = 0
        print(to_sum)
    elif (position_diff_e[0] < 0) and (position_diff_e[1] >= 0):
        to_sum = math.pi
        print(to_sum)
    elif (position_diff_e[0] < 0) and (position_diff_e[1] < 0):
        to_sum = -math.pi
        print(to_sum)
    elif (position_diff_e[0] == 0) and (position_diff_e[1] > 0):
        to_sum = math.pi/2
        print(to_sum)
    else:
        to_sum = -math.pi/2
        print(to_sum)
    
    theta_e = np.arctan(np.array([position_diff_e[2]/np.sqrt(xy_e)])) 
    azimuth_e = np.arctan(np.array([position_diff_e[1]/position_diff_e[0]])) + to_sum
    direccion_estimada[j] = np.array([theta_e[0], azimuth_e[0]])

print("Dirección Fuente: ")
print(direccion_fuente)

print("Dirección Estimada: ")
print(direccion_estimada)

for t in range(0, 5):
    if t == 0:
        print ("H-SRP & " + str(sound_source_positions[t]) + " & " + str(direccion_fuente[t]) + " & " + str(posicion_estimada[t]) + " & " + str(direccion_estimada[t]) + " & " + str(coste_comp[t]) + " \\\\")
    else:
        print (" & " + str(sound_source_positions[t]) + " & " + str(direccion_fuente[t]) + " & " + str(posicion_estimada[t]) + " & " + str(direccion_estimada[t]) + " & " + str(coste_comp[t]) + " \\\\")


ax.set_xlabel('x [cm]')
ax.set_ylabel('y [cm]')
ax.set_zlabel('z [cm]')

for i, txt in enumerate(label_original):
    ax.text(sound_source_positions[i][0],sound_source_positions[i][1],sound_source_positions[i][2],  '%s' % (txt))
    ax.text(posicion_estimada[i][0],posicion_estimada[i][1],posicion_estimada[i][2],  '%s' % label_estimation[i])

plt.show()