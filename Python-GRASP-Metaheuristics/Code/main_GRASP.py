# -*- coding: utf-8 -*-
####################################################
#TRABAJO FINAL - CURSO DE POSGRADO 'METAHEURÍSTICAS'
#Author: Marcelo A. Paciulli
####################################################


import numpy as np
from random import choice
from param_and_functions import*
from Busqueda_local import busqueda_local
import random
import winsound
import matplotlib.pyplot as plt
import time 
from func_greedy import*
from greedy_randomized_building import*


class GRASP:
    
    def procedure_GRASP(self,max_Iter,seed,alpha):
        #print(constraint_1(seed)
        #print(constraint_2(seed))
        #print(func_evaluacion(seed))
        listens = []
        mejor_costo = costos.sum()
        for k in range(max_Iter):
            s = greedy_randomized_construction(seed,alpha)
            flag = False
            s,_ = busqueda_local(s, func_evaluacion, generar_vecinos, 144.26,3.33,0.96)
            if mejor_costo > sum_costs(s):
                flag = True
                mejor_costo = sum_costs(s)
                best_solution =s.copy()
            seed = s.copy()
            listens.append(np.exp(mejor_costo/2339.0))  #e^(found/optimal)  #to minimize 
            #plt.ion()
            plt.plot(listens,'.')
            plt.title('error virtual: {0} en iteración: {1}'.format(round(listens[k],4),k+1))
            plt.xlabel('error in approximations')
            plt.ylabel('iterations')
            if flag == True:
                winsound.Beep(2500,250)
            else:
                winsound.Beep(500,250)
            plt.draw()
            print('#'*60)
            print('\n')
            print('lower cost in {0} segundos:  {1}'.format(round(time.clock(),4),mejor_costo))
            print('\n')
        plt.savefig('salida.png')
        return best_solution
   

    #generamos la semilla
    def generating_initial(self):
        init_factible = []
        for i in range(5000):
            w = generate_init(capacidades)
            r = rellenar(w.copy())
            if w.sum()==capacidades.shape[1]:
                init_factible.append(w)
                break
            elif r.sum()==capacidades.shape[1]:
                init_factible.append(r)
                break
        if init_factible==[]:
            salida = init_factible
        else:
            salida = init_factible[0]
        return salida



    
    #retornamos las asignaciones agentes-tareas y la
    #ganancia total por tales asignaciones
    def get_assign_and_profit(self,best):
        agentes_tareas = []
        costo_neto = 0
        for i in range(best.shape[0]):
            for j in range(best.shape[1]):
                if best[i,j]!=0:
                    costo_neto+=costos[i,j]
                    agentes_tareas.append((i,j))
        return (costo_neto,agentes_tareas)


if __name__ == "__main__":
    new_object = GRASP()
    print('wait for initial solution.....\n\n')
    semilla = new_object.generating_initial()
    if semilla!=[]:
        print('seed was found!\n\n')
        print('Calculating...\n\n')
        max_iter = int(input('Ingrese iteraciones máximas: '))
        print('\n\n')
        alfa = float(input('Ingrese valor de alfa (0.0-0.2): '))
        inicio = time.clock()
        print('\n\n')
        print('search for optimal solutions....\n\n')
        mejor = new_object.procedure_GRASP(max_iter,semilla,alfa)
        costo_obtenido,agentes_tareas = new_object.get_assign_and_profit(mejor)
        print('#'*60)
        print('\n\n')
        fin = time.clock()
        total = fin-inicio
        print("Mejor solución hallada: \n \n {0} \n\n".format(mejor))
        print("Tiempo consumido (seg):  {0}".format(round(total,4)))
        print("Costo obtenido:  {0}".format(costo_obtenido))
        print("Asignaciones Agente-tarea:  \n\n {0} \n\n ".format(agentes_tareas))
        print("Cantidad de tareas para cada agente: \n\n {0} \n\n".format(mejor.sum(axis=1).astype(int)))
    else:
        print('seed was not found... please try again (this process is nontrivial!)\n\n')
        print('--------------------------------------------\n\n')
        print('1- Start again (search for initial solution)\n')
        print('2- Exit \n\n')
        print('--------------------------------------------\n\n')
        opcion = int(input('Ingrese opción (1 o 2): '))
        while semilla==[] and opcion==1:
            print('\n\n')
            print('wait for initial solution.....\n\n')
            semilla = new_object.generating_initial()
            if semilla ==[]:
                print('seed was not found... please try again (this process is nontrivial!)\n\n')
                print('--------------------------------------------\n\n')
                print('1- Start again (search for initial solution)\n')
                print('2- Exit \n\n')
                print('--------------------------------------------\n\n')
                opcion = int(input('Ingrese opción (1 o 2): '))
                
        if semilla!=[]:
            print('seed was found!\n\n')
            print('Calculating...\n\n')
            max_iter = int(input('Ingrese iteraciones máximas: '))
            print('\n\n')
            alfa = float(input('Ingrese valor de alfa (0.0-0.2): '))
            inicio = time.clock()
            print('\n\n')
            print('search for optimal solutions....\n\n')
            mejor = new_object.procedure_GRASP(max_iter,semilla,alfa)
            costo_obtenido,agentes_tareas = new_object.get_assign_and_profit(mejor)
            print('#'*60)
            print('\n\n')
            fin = time.clock()
            total = fin-inicio
            print("Mejor solución hallada: \n \n {0} \n\n".format(mejor))
            print("Tiempo consumido (seg):  {0}".format(round(total,4)))
            print("Costo obtenido:  {0}".format(costo_obtenido))
            print("Asignaciones Agente-tarea:  \n\n {0} \n\n ".format(agentes_tareas))
            print("Cantidad de tareas para cada agente: \n\n {0} \n\n".format(mejor.sum(axis=1).astype(int)))
        else:
            print('\n\n')
            print('aborted.....')
            pass


        

        

