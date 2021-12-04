from matplotlib.pyplot import margins
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
        self.dimensiones = np.array([x_room, y_room, z_room])
        self.margin_dimensions = np.array([x_room, y_room, z_room])

    def place_sound_source(
        self,
        filename,
        position,
    ):
        if position[0] > self.dimensiones[0] + 1 or position[1] > self.dimensiones[1] + 1 or position[2] > self.dimensiones[2] + 1:
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
        left = signal[0::2]

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
        to_divide = None
    ):
        if to_divide is None:
            to_divide = self.margin_dimensions
        to_divide = np.array([(to_divide[0])/2, (to_divide[1])/2, (to_divide[2])/2])
        id_potencia_mayor = None
        potencia_alta = 0

        if self.temporal_partitions.depth() == 0:
            esquinas_nodo = self.corners(self.temporal_partitions.get_node("room").data["esquinas"][0], to_divide)
            self.temporal_partitions.create_node(identifier="1", parent="room",
            data={
                "to_divide": to_divide,
                "esquinas": esquinas_nodo,
                "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
            })

            for i in range(1,8):
                esquinas_nodo = self.corners(self.temporal_partitions.get_node("1").data["esquinas"][i], to_divide)
                self.temporal_partitions.create_node(identifier=str(i+1), parent="room",
                data={
                    "to_divide": to_divide,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })

        else:
            esquinas_nodo_padre = self.corners(self.temporal_partitions.get_node(parent_id).data["esquinas"][0], to_divide)
            for i in range(0,8):
                esquinas_nodo = self.corners(esquinas_nodo_padre[i], to_divide)
                self.temporal_partitions.create_node(identifier=parent_id + str(i+1), parent=parent_id,
                data={
                    "to_divide": to_divide,
                    "esquinas": esquinas_nodo,
                    "potencia": GCC(inverted_signal, esquinas_nodo, self.Mic_Array, fs),
                })        

        for hoja in self.temporal_partitions.leaves():
            if potencia_alta < hoja.data["potencia"]:
                potencia_alta = hoja.data["potencia"]
                id_potencia_mayor = hoja.identifier
  
        if np.prod(self.temporal_partitions.get_node(id_potencia_mayor).data["to_divide"]) <= 100:
            #self.temporal_partitions.show()
            print(id_potencia_mayor)
            print(self.temporal_partitions.get_node(id_potencia_mayor).data)
            centro = self.temporal_partitions.get_node(id_potencia_mayor).data["esquinas"][0] + to_divide
            return id_potencia_mayor, centro

        else:
            new_to_divide = self.temporal_partitions.get_node(id_potencia_mayor).data["to_divide"]
            id_posicion, centro = self.HSRP(inverted_signal, id_potencia_mayor, fs, new_to_divide)
            return id_posicion, centro

    def place_mic_array(
    self, 
    position, 
    ):
        self.Mic_Array = MicArray(position)
        mic_margin = position + np.array([0,80,0])
        self.margin_dimensions[1] = self.dimensiones[1] - mic_margin[1]

        self.room_partitions = Tree()
        esquinas_raiz = self.corners(np.array([0,mic_margin[1],0]), self.margin_dimensions)
        self.room_partitions.create_node(identifier="room", data={
                    "to_divide": self.margin_dimensions,
                    "esquinas": esquinas_raiz,
                })
        self.temporal_partitions = deepcopy(self.room_partitions)

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