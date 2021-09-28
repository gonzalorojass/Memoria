import numpy as np
import wave
from copy import deepcopy
from treelib import Tree, Node
from Mic_array import *
from GCC import *

class Grid:
    def __init__(
        self,
        x_room = 280,
        y_room = 560,
        z_room = 240,
    ):
        self.x_room = x_room + 1
        self.y_room = y_room + 1
        self.z_room = z_room + 1

        self.n = self.x_room*self.y_room*self.z_room
        self.points = np.zeros((self.n,3))
        self.place_mic_array(np.array([20,20,10]))
        self.potencia = np.zeros((self.n))

        self.room_partitions = Tree()
        dimensiones_habitacion =  np.array([x_room, y_room, z_room])
        esquinas_raiz = self.corners(np.array([0,0,0]), dimensiones_habitacion)
        self.room_partitions.create_node(identifier="room", data={
                    "halves": np.array([x_room, y_room, z_room]),
                    "esquinas": esquinas_raiz,
                })
        self.temporal_partitions = deepcopy(self.room_partitions)

    def place_mic_array(
        self, 
        position, 
    ):
        self.Mic_Array = MicArray(position)


    def place_sound_source(
        self,
        filename,
        position,
        # CHUNK,                   # SE USARA ACTUALMENTE 1 SEGUNDO (CHUNK = fs)
    ):
        if position[0] > self.x_room or position[1] > self.y_room or position[2] > self.z_room:
            print("Posición esta fuera del espacio")
            return
        
        try:
            wf = wave.open(filename, 'r')
            
        except:
            print("Insertar el nombre de un archivo valido")
            return

        c = 34300
        fs = wf.getframerate()
        recieved_signal = np.zeros((self.Mic_Array.mics_n, fs))

        signal = wf.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)   
        left = signal[0::2]             # USO DE UN SOLO CANAL

        for i in range(0, self.Mic_Array.mics_n):
            tau = round(fs*(np.linalg.norm(position-self.Mic_Array.mic_position[i]))/c)
            recieved_signal[i] = left[tau: tau+fs]

        invXi_Xj = np.zeros((sum(range(self.Mic_Array.mics_n)), recieved_signal[0].size))
        n = 0
        for i in range(0, self.Mic_Array.mics_n-1):
            for j in range (i+1, self.Mic_Array.mics_n):
                Xi_Xj = np.fft.rfft(recieved_signal[i], n = recieved_signal[i].size)*np.conj(np.fft.rfft(recieved_signal[j], n = recieved_signal[j].size))
                peso = 1/(abs(Xi_Xj))
                invXi_Xj[n] = np.fft.irfft(Xi_Xj*peso, n = recieved_signal[0].size)
                n += 1

        return invXi_Xj, fs

    def HSRP(
        self,
        inverted_signal,
        parent_id,
        fs,
        halves
    ):
        halves = np.array([(halves[0])/2, (halves[1])/2, (halves[2])/2])
        id_potencia_mayor = None
        potencia_alta = 0

        if self.temporal_partitions.depth() == 0:
            esquinas_nodo = self.corners(np.array([0,0,0]), halves)
            self.temporal_partitions.create_node(identifier="1", parent="room",
            data={
                "halves": halves,
                "esquinas": self.corners(np.array([0,0,0]), halves),
                "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
            })

            for i in range(1,8):
                esquinas_nodo = self.corners(self.temporal_partitions.get_node("1").data["esquinas"][i], halves)
                self.temporal_partitions.create_node(identifier=str(i+1), parent="room",
                data={
                    "halves": halves,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })

        else:
            esquinas_nodo_padre = self.corners(self.temporal_partitions.get_node(parent_id).data["esquinas"][0], halves)
            for i in range(0,8):
                esquinas_nodo = self.corners(esquinas_nodo_padre[i], halves)
                self.temporal_partitions.create_node(identifier=parent_id + str(i+1), parent=parent_id,
                data={
                    "halves": halves,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })        

        for hoja in self.temporal_partitions.leaves():
            if potencia_alta < hoja.data["potencia"]:
                potencia_alta = hoja.data["potencia"]
                id_potencia_mayor = hoja.identifier
  
        if np.prod(self.temporal_partitions.get_node(id_potencia_mayor).data["halves"]) <= 1000:
            centro = self.temporal_partitions.get_node(id_potencia_mayor).data["esquinas"][0] + halves
            return id_potencia_mayor, centro

        else:
            new_halves = self.temporal_partitions.get_node(id_potencia_mayor).data["halves"]
            id_posicion, centro = self.HSRP(inverted_signal, id_potencia_mayor, fs, new_halves)
            return id_posicion, centro

    def corners(
        self,
        v0,
        v1
    ):
        esquinas = np.zeros((8,3))
        for i in range(0,8):
            l = format(i, '03b')
            l = np.array([int(l[0]),int(l[1]), int(l[2])])
            esquinas[i] = v0 + l*v1
        
        return esquinas

    def reset_tree(self):
        self.temporal_partitions = deepcopy(self.room_partitions)