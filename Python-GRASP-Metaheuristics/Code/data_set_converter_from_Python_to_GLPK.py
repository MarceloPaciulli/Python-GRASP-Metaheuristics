import numpy as np
import random


def data_file_generator(rows,columns,name):
    archivo = open("data_set_6.txt",'w')  #creo un archivo de escritura
    e = np.loadtxt(name) #archivo generado en python 
    e.resize(rows,columns)
    for j,item in enumerate(list(e.astype(int))):
        archivo.write(str(item)+'\n')
    archivo.close()    #cerramos el archivo

data_file_generator(50,200,'example.dat')

