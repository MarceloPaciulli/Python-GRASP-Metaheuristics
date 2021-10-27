
import numpy as np
from pylab import find
from random import choice
from param_and_functions import*


#ACÁ DEFINO LOS DATOS CON LOS QUE TRABAJO
#TAMBIÉN EN param_and_functions
#filename y redimensionar
##########################################################
costos = np.loadtxt('costos.dat')
capacidades = np.loadtxt('capacidades.dat')
capacities = np.loadtxt('capacities.dat')
costos.resize(20,200)
capacidades.resize(20,200)
##########################################################  

#generar inicial
def generate_init(c):
	t = np.zeros_like(c)
	array_cap = np.zeros((c.shape[0]))
	for j in range(t.shape[1]):
		m = choice(range(t.shape[0]))
		if (array_cap[m]+capacidades[m,j]<capacities[m]):
			array_cap[m]+=capacidades[m,j]
			t[m,j]=1

	return t




#solución parcial factible
def asignar(c):
	t1 = np.zeros((c.shape[0],c.shape[1]))
	loc_tabu = []
	cap_accum=np.zeros_like(capacities)
	for i in range(400):
		n = choice(range(t1.shape[1]))
		m = choice(range(t1.shape[0]))
		if (((t1[m,n]==0)& (cap_accum[m]<capacities[m]))&(n not in (loc_tabu))):
			if ((cap_accum[m]+capacidades[m,n])<capacities[m]):
				t1[m,n]=1
				cap_accum[m]+=capacidades[m,n]
				loc_tabu.append(n)
	return t1

#rellenar con unos si es factible                        
def rellenar(e):
	def sumar_cap(e):
		lista = []
		for i in range(e.shape[0]):
			cap = 0
			for j in range(e.shape[1]):
				if e[i,j]!=0:
					cap+=capacidades[i,j]
			lista.append(cap)
		return lista
	e1 = e.copy()
	loc = find(e.sum(axis=0)==0)
	for columna in loc:
		for i in range(e1.shape[0]):
			if (((sumar_cap(e)[i]+capacidades[i,columna])<capacities[i])&(e.sum(axis=0)[columna]==0)):
				e[i,columna]=1
	return e


#restricción 1
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
    return cumple

#restricción 2
def constraint_2(e):
	if (np.unique(e.sum(axis=0)).all()==np.eye(1)):
		return True
	else:
		return False

	

#e: solución inicial           
def set_elementos_candidatos(e):
    #restricción 2
    def set_posibles_elem(e):
        set_elems = []
        for k,elem in enumerate(np.eye(e.shape[0])):
            elem1 = np.row_stack(elem)
            set_elems.append(elem1)
            return set_elems
    set_columnas = set_posibles_elem(e)
    #restricción 1
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
        return cumple
    ##que elementos se pueden agregar, qué posición 'columna', para que
    ###no se pierda la factibilidad
    set_tuplas = []
    for elem in set_columnas:
        for j in range(e.shape[1]):
            aux = e.copy()
            aux[:,j][:,np.newaxis]=elem
            if constraint_1(aux):
                set_tuplas.append[(elem,j)]
    return set_tuplas,set_columnas
                
                
                
##sumar capacidades 	    
def sumar_cap(e):
	lista = []
	for i in range(e.shape[0]):
		cap = 0
		for j in range(e.shape[1]):
			if e[i,j]!=0:
				cap+=capacidades[i,j]
		lista.append(cap)
	return lista


##lista_factibles
def lista_factibles():
	lista,lista1=[],[]
	for i in range(4000):
		lista1.append(asignar(capacidades))
		w = rellenar(lista1[i])
		if ((constraint_1(w)==True) & (w.sum()==capacidades.shape[1])):
			lista.append(w)
	return lista
    

    
