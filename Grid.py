import numpy as np
import wave
import matplotlib.pyplot as plt
from Mic_array import *
from GCC import *
from decimal import *

import time                            # PARA CALCULAR TIEMPO; BORRAR AL FINAL 

class Grid:
    ####        X,Y,Z se tienen que trabajar en centimetros         ####
    def __init__(
        self,
        x_room = 280,
        y_room = 560,
        z_room = 240,
    ):
        self.x_room = x_room + 1
        self.y_room = y_room + 1
        self.z_room = z_room + 1

        self.n = self.x_room*self.y_room*self.z_room        # CUBO MAS PEQUEÑO 10x10x10 cm POR DEFINIR
        self.points = np.zeros((self.n,3))
        self.place_mic_array(np.array([20,20,10]))
        self.potencia = np.zeros((self.n))


    def place_mic_array(
        self, 
        position, 
    ):
        self.Mic_Array = MicArray(position)


    def place_sound_source(
        self,
        filename,
        position,
        CHUNK,                   # ACTUALMENTE DEJAR COMO CHUNK, SE DEBE MODIFICAR SEGUN INFORMACIÓN INVESTIGADA
    ):
        if position[0] > self.x_room or position[1] > self.y_room or position[2] > self.z_room:
            print("Posición esta fuera del espacio")
            return

        recieved_signal = np.zeros((self.Mic_Array.mics_n, CHUNK))
        
        try:
            wf = wave.open(filename, 'r')
            
        except:
            print("Insertar el nombre de un archivo valido")
            return

        c = 34300
        fs = wf.getframerate()
        print ("Frecuencia señal WAV: " + str(fs))
        signal = wf.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)   
        left = signal[0::2]             # USO DE UN SOLO CANAL

        for i in range(0, self.Mic_Array.mics_n):

            tau = round(fs*(np.linalg.norm(position-self.Mic_Array.mic_position[i]))/c)
            recieved_signal[i] = left[tau: tau+CHUNK]

            print (tau)

        return recieved_signal

    
    def SRP(
        self,
        signal,
        mic_array
    ):
        # AGREGAR RUTINA DE DIVICIÓN DEL ESPACIO
        invXi_Xj = np.zeros((sum(range(mic_array.mics_n)), signal[0].size))
        n = 0
        for i in range(0, mic_array.mics_n-1):
            for j in range (i+1, mic_array.mics_n):
                Xi_Xj = np.fft.rfft(signal[i], n = signal[i].size)*np.conj(np.fft.rfft(signal[j], n = signal[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = signal[0].size)
                n += 1

        l = 0
        print (self.n)
        print (self.points.size)
        while l < self.n:
            for k in range(0, self.z_room):
                for j in range(0, self.y_room):
                    for i in range(0, self.x_room):
                        self.points[l] = [i,j,k] 
                        self.potencia[l] = GCC(invXi_Xj, self.points[l], self.Mic_Array)
                        l+=1
        test = np.argmax(abs(self.potencia))
        print("Tau obtenido: " + str(test))
        print("Potencia obtenida: " + str(self.potencia[test]))
        return self.points[np.argmax(abs(self.potencia))] 

def main():
    grid1 = Grid(x_room = 200, y_room = 300, z_room = 200)
    mic_position = np.array([100,70,0])
    sound_source_position = np.array([100,230,140])
 
    grid1.place_mic_array(mic_position)
    signal_to_plot = grid1.place_sound_source('trumpet.wav', sound_source_position, 44100)

    start = time.time()                     # PARA CALCULAR TIEMPO; BORRAR AL FINAL

    POSICIOOOON = grid1.SRP(signal_to_plot, grid1.Mic_Array)
    print(POSICIOOOON)

    end = time.time()                                                   # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    print ("\ncoste computacional: "+str(end-start))                    # PARA CALCULAR TIEMPO; BORRAR AL FINAL
    
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.set_title("Points in Space")
    ax.set_xlim([0, grid1.x_room-1])
    ax.set_ylim([0, grid1.y_room-1])
    ax.set_zlim([0, grid1.z_room-1])

    ax.scatter(POSICIOOOON[0], POSICIOOOON[1],  POSICIOOOON[2])
    ax.scatter(mic_position[0], mic_position[1], mic_position[2])
    ax.scatter(sound_source_position[0], sound_source_position[1], sound_source_position[2])
    plt.show()

    

if __name__ == "__main__":
    main()