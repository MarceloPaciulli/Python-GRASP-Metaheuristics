
import numpy as np
from random import choice
from pylab import find
from func_greedy import*
from param_and_functions import*




def build_seeds(x_init):
        elementos = []
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
        for k in range(2):
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
                                e1 = x_init_2[:,col_1][:,np.newaxis]
                                e2 = x_init_2[:,col_2][:,np.newaxis]
                                elementos.append([(e1,e2),(col_1,col_2),flag])
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
                                element = x_init_2[:,n][:,np.newaxis]
                                elementos.append([element,n,flag])
                                flag = choice([True,False])
        return (soluciones_vecinas,elementos)

def costs(x):
    l = []
    for i in range(len(x[0])):
        l.append(func_evaluacion(x[0][i]))
    return l

def rcl(x,alfa,cmin,cmax):
    costos = []
    lista_restringida = []
    for i,elem in enumerate(x):
        costos.append(func_evaluacion(elem))
    for k in range(len(costos)):
        if costos[k]>=cmin+alfa*(cmax-cmin):
            lista_restringida.append(k)
    return lista_restringida
    

def get_best_index(aux,elems1): #elems1: solutions[0]
        def get_profit(nb):
                suma = 0
                for i in range(nb.shape[0]):
                        for j in range(nb.shape[1]):
                                if nb[i,j]!=0:
                                        suma+=ganancias[i,j]
                return suma
        profitss = []
        for i,item in enumerate(elems1):
                if i in aux:
                        profitss.append(get_profit(item))
        return aux[profitss.index(max(profitss))]


    
def greedy_randomized_construction(semilla,alfa):
    s = semilla.copy()
    solutions = build_seeds(s)  #vecinos,elementos
    conjunto_candidato = solutions[1]
    costos_incrementales = costs(solutions)
    RCL = []
    while conjunto_candidato!=[]:
        c_min = min(costos_incrementales)
        c_max = max(costos_incrementales)
        aux = rcl(solutions[0],alfa,c_min,c_max)
        for item in aux:
            RCL.append(conjunto_candidato[item])
        #ELEGIMOS CUALQUIERA DE LAS TRES MANERAS DE ELEGIR EL ELEMENTO DE LA LISTA RCL
        elem_a_incorporar =  RCL[aux.index(get_best_index(aux,solutions[0]))]#best-improvement
        #elem_a_incorporar = RCL[0]  #first-improvement
        #elem_a_incorporar = choice(RCL) #random improvement
        if elem_a_incorporar[2]==False:
            pos_columna = elem_a_incorporar[1]
            columna = elem_a_incorporar[0]
            s[:,pos_columna][:,np.newaxis]= columna
        else:
            pos_columna1 = elem_a_incorporar[1][0]
            pos_columna2 = elem_a_incorporar[1][1]
            columna1 = elem_a_incorporar[0][0]
            columna2 = elem_a_incorporar[0][1]
            s[:,pos_columna1][:,np.newaxis]=columna1
            s[:,pos_columna2][:,np.newaxis]=columna2
        #actualizamos el conjunto candidato y
        #reevaluamos costos incrementales
        solutions = build_seeds(s)
        conjunto_candidato = solutions[1]
        costos_incrementales = costs(solutions)
    return s
    
    
