import numpy as np
from scipy.fft import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt        # BORRAR EN EL FUTURO (QUIZAS)
import time                            # PARA CALCULAR TIEMPO; BORRAR AL FINAL 

np.set_printoptions(threshold=np.inf)  # PARA IMPRESION DE ARREGLOS SIN TRUNCAR

fs = 6800        #DOBLE DE 3400 Hz (FRECUENCIA VOZ HUMANA)

t = np.arange(256)      # DATO INUTIL PARA TESTEAR ARREGLO DE 256 CON NP.SIN  BORRAR

m1 = fft(np.sin(t))                  # DEFINIR LOS MICROFONOS COMO ARREGLOS DE ENTRADA EXTERNA
m2 = fft(np.sin(t-2))
m3 = fft(np.sin(t+2))
m4 = fft(np.sin(t))
m5 = fft(np.sin(t))
m6 = fft(np.sin(t))

mic_array = [m1, m2, m3, m4, m5, m6]    # QUIZAS ASI?

mic_location = [np.array([3,3,3]), np.array([1,2,3]), np.array([1,2,3]), np.array([1,2,3]), np.array([1,2,3]), np.array([1,2,3])]

start = time.time()                     # PARA CALCULAR TIEMPO; BORRAR AL FINAL 
c = 343                                 # VELOCIDAD DEL SONIDO


grid = np.zeros(1000)                    # DEFINIR GRILLA SOBRE LA CUAL TRABAJAR
tau = np.zeros(15)
pair = 0

Sum_final = 0.0

####    TESTING DE FFT     ####

t1 = np.array([[[1,2,3],[4,5,6],[7,8,9]],[[11,12,13],[14,15,16],[17,18,19]]])
print(t1.shape)
print(t1[:,1,:])


t = np.arange(256)
sp = fftshift(fft(np.sin(t)))
freq = fftshift(fftfreq(t.shape[-1]))


k=0
tau1 = np.zeros(15)
pot = np.zeros(15)
####    TESTING DE FFT     ####

for i in range(0,5):
    for j in range (i+1,6):
        x = np.array([1,2,3])                                   # CAMBIAR CUANDO SE ITERE EN LAS POSICIONES

        tau[pair] = round(fs*(np.linalg.norm(x-mic_location[i]) -     # DEFINIR TAU COMO UN ARREGLO (?)
        np.linalg.norm(x-mic_location[j]))/c)

        Xi_Xj = fft(mic_array[i])*np.conj(fft(mic_array[j]))
        peso = 1/(abs(Xi_Xj))                                   # DESARROLLAR COMO FUNCIÓN EXTERNA         
        invXi_Xj = np.array(ifft(Xi_Xj*peso))


         ###         PLOT DE LA CORRELACIÓN          ###

        tau1[k] = (np.argmax(np.abs(invXi_Xj)))
        pot[k] = invXi_Xj[int(tau1[k])]
        k+=1
       
        fig, ax = plt.subplots(1, figsize=(15, 7))
        x = np.arange(0, invXi_Xj.size)
        ax.plot(x, abs(invXi_Xj))
        plt.show() 
        
        ###         PLOT DE LA CORRELACIÓN          ###

        Sum_final += invXi_Xj
        pair += 1

# for x in range(0, grid.size):                                     # RECORRER EL ARREGLO DE LA GRILLA (ITERACION 1)
#     print('Test')

end = time.time()                                                   # PARA CALCULAR TIEMPO; BORRAR AL FINAL 

print("valores de tau:")
print(tau1)
print(pot)
print ("\ncoste computacional: "+str(end-start))      # PARA CALCULAR TIEMPO; BORRAR AL FINAL
