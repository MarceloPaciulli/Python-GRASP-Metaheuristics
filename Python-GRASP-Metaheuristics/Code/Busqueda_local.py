
# coding: utf-8


import numpy as np
import matplotlib.pyplot as plt
import random


def busqueda_local(solucion_inicial, evaluacion, obtener_vecinos,
                        T_max, T_min, reduccion):
  
    from random import random

    solucion_mejor = solucion_actual = solucion_inicial
    evaluacion_mejor = evaluacion_actual = evaluacion(solucion_actual)
    soluciones_evaluadas = 1

    T = T_max
    while T >= T_min:
        vecinos = obtener_vecinos(solucion_actual)
        for vecino in vecinos:
            evaluacion_vecino = evaluacion(vecino)
            soluciones_evaluadas += 1
            
            if (evaluacion_vecino < evaluacion_actual or
                random() > np.exp((evaluacion_vecino - evaluacion_actual) / T)):
                solucion_actual = vecino
                evaluacion_actual = evaluacion_vecino
                if evaluacion_mejor > evaluacion_actual:
                    solucion_mejor = solucion_actual
                    evaluacion_mejor = evaluacion_actual

        T = reduccion * T

    return solucion_mejor, soluciones_evaluadas

