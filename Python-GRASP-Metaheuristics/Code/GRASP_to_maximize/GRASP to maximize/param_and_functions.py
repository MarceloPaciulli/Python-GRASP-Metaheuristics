import numpy as np
from random import choice
from pylab import find
import time
from func_greedy import*


#>>> np.savetxt('capacities_gap.dat',capacities,fmt='%.1e')
#>>> e = np.loadtxt('capacities_gap.dat')
ganancias = np.loadtxt('ganancias.dat')
capacidades = np.loadtxt('capacidades.dat')
capacities = np.loadtxt('capacities.dat')
ganancias.resize(10,50)
capacidades.resize(10,50)

"""
ganancias = np.loadtxt('benefits_gap.dat')
capacidades = np.loadtxt('capacidadesh_gap.dat')
capacities = np.loadtxt('capacitiesh_gap.dat')
ganancias.resize(50,200)
capacidades.resize(50,200)"""

#generación de solución inicial (factible)
def generar_aleatorio(m,n):
	init_array = np.zeros((m,n))
	for j in range(n):
		init_array[choice(range(0,m)),j]=1
	return init_array


#beneficio
def benefit(e):
        ganancia_neta = 0
        for i in range(e.shape[0]):
                for j in range(e.shape[1]):
                        if e[i,j]!=0:
                                ganancia_neta+=ganancias[i,j]
        return ganancia_neta


#función objetivo, con restricciones
def func_evaluacion(X):
        X_1 = np.array(X).reshape(X.shape[0],X.shape[1])
        def benefit(e):
                ganancia_neta = 0
                for i in range(e.shape[0]):
                        for j in range(e.shape[1]):
                                if e[i,j]!=0:
                                        ganancia_neta+=ganancias[i,j]
                return ganancia_neta
        def constraint_1(e):
                cumple = True
                for i in range(e.shape[0]):
                        lim_capacity = 0
                        for j in range(e.shape[1]):
                                if e[i,j]!=0:
                                        lim_capacity+=capacidades[i,j]
                                        if lim_capacity>capacities[i]:
                                                cumple = False
                                                break
                return (cumple,lim_capacity)
        def constraint_2(e):
                if (np.unique(e.sum(axis=0)).all()==np.eye(1)):
                        return True
                else:
                        return False
        output_1 = constraint_1(X_1)
        output_2 = constraint_2(X_1)
        if output_1[0] & output_2:
                #print(benefit(X_1))
                salida = benefit(X_1)
        else:
                salida = - benefit(X_1) - output_1[1]
        return salida 


#neighborhood function (randomized hibrid)
def generar_vecinos(x_init):
        soluciones_vecinas = []
        def constraint_1(e):
                cumple = True
                for i in range(e.shape[0]):
                        lim_capacity = 0
                        for j in range(e.shape[1]):
                                if e[i,j]!=0:
                                        lim_capacity+=capacidades[i,j]
                                        if lim_capacity>capacities[i]:
                                                cumple = False
                                                break
                return (cumple,lim_capacity)
        def constraint_2(e):
                if (np.unique(e.sum(axis=0)).all()==np.eye(1)):
                        return True
                else:
                        return False
        x_init_1 = np.array(x_init).copy()
        flag = choice([True,False])
        for k in range(10):
                if flag==True:
                        #print(flag)
                        x_init_2 = x_init_1.copy()
                        col_1 = choice(range(0,x_init_1.shape[1]))
                        elem = list(range(0,x_init_1.shape[1]))
                        elem.remove(col_1)
                        col_2 = choice(elem)
                        aux = x_init_2.copy()
                        x_init_2[:,col_1] = aux[:,col_2]
                        x_init_2[:,col_2] = aux[:,col_1]
                        if constraint_1(x_init_2)[0] & constraint_2(x_init_2):
                                soluciones_vecinas.append(x_init_2)
                        flag = choice([True,False])
                else:
                        #print(flag)
                        x_init_2 = x_init_1.copy()
                        n = choice(range(0,x_init_1.shape[1]))
                        unidad = find(x_init_1[:,n]==1)
                        m = find(x_init_1[:,n]==0)
                        new_item = choice(m)
                        x_init_2[new_item].put(n,1)
                        x_init_2[unidad,n]=0
                        if constraint_1(x_init_2)[0] & constraint_2(x_init_2):
                                soluciones_vecinas.append(x_init_2)
                                flag = choice([True,False])
        return soluciones_vecinas

    
#neighborhood function1 (intercambio de 2 columnas)
def generar_vecinos1(x_init):
	soluciones_vecinas = []
	x_init_1 = np.array(x_init).copy()
	for k in range(15):
		x_init_2 = x_init_1.copy()
		col_1 = choice(range(0,x_init_1.shape[1])) #columna aleatoria n
		elem = list(range(0,x_init_1.shape[1]))
		elem.remove(col_1)
		col_2 = choice(elem)
		aux = x_init_2.copy()
		x_init_2[:,col_1] = aux[:,col_2]
		x_init_2[:,col_2] = aux[:,col_1]
		soluciones_vecinas.append(x_init_2)
	return soluciones_vecinas



#neighborhood function2 (añade y quita un 1 en una columna aleatoria)
def generar_vecinos_2(x_init):
	soluciones_vecinas = []
	x_init_1 = np.array(x_init).copy()
	for k in range(15):
		x_init_2 = x_init_1.copy()
		n = choice(range(0,x_init_1.shape[1])) #columna aleatoria n
		unidad = find(x_init_1[:,n]==1) #la posición del 1 en la columna n
		m = find(x_init_1[:,n]==0)
		new_item = choice(m) #tengo la fila donde irá a parar el nuevo 1
		x_init_2[new_item].put(n,1)
		x_init_2[unidad,n]=0  #donde tenía un 1, reemplazo por 0
		soluciones_vecinas.append(x_init_2)
	return soluciones_vecinas    
