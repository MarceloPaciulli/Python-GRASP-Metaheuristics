import numpy as np
import random


def data_file_generator(rows,columns):
    archivo = open("data_set.txt",'w')  #creo un archivo de escritura
    e = np.loadtxt('capacidades_gap.dat')
    e.resize(rows,columns)
    for j,item in enumerate(list(e.astype(int))):
        archivo.write(str(item)+'\n')
    archivo.close()    #cerramos el archivo

data_file_generator(10,40)

