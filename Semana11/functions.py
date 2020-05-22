import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib as mpl
from getdist import plots, MCSamples
import getdist
import cosmolopy.distance as cd

def logLikelihood(x, y, model, sigma, theta):
    '''
    Descripcion: Esta función mida lo bien que un modelo estadístico se adecúa a unos datos
    para los valores de parámetros desconocidos.
    In = {
        x: Variable independiente a analizar
        y: Variable dependiente a analizar
        model: El modelo con el cual lo estamos comparando
        theta: Los parámetros de este modelo
    }
    OUT: El likelihood
    '''
    # Variable suma empezada en 0
    suma = 0
    # Construimos la suma correspondiente a la fórmula del likelihood proporcionada en las notas de la maestra.
    for i in range(len(x)):
        suma += (y[i] - model(x[i], theta))**2 / sigma[i]**2
    
    return -(0.5) * suma

# Tasa de aceptación
def tasaAceptacion(lista, pasosTotales):
    '''
    Descripción: Función que calcula la razón entre la cantidad de pasos aceptados por el método montecarlo
    y la cantidad de pasos totales
    IN = {
        lista: La lista de la cantidad de pasos aceptados de las n cadenas
        pasos: La cantidad de pasos totales del método
    }
    OUT: Una lista de n elementos con la tasa de aceptación para las n cadenas
    '''
    
    listTasa = []
    for index, accepted in enumerate(lista):
        listTasa.append(accepted/pasosTotales)
    return listTasa

# Se define el método montecarlo
def montecarlo(x, y, sigmaX, sigmaY, model, initPoints, pasosTotales, logLikelihood, logPrior=0):
    import numpy as np
    # Se asigna una semilla específica para hacer comparaciones con otros repositorios, pero se puede quitar sin problemas
    # Se declaran la cadena llamada "Cadena de Markov" y se define la "Matriz de Markov" para albergar varias cadenas
    # Específicamente serán n cadenas, donde n es la cantidad de puntos iniciales que tenemos
    markovMatrix = []
    markovChain = []
    # Se define una lista para la tasa de aceptación 
    aceptado = []
    # Este ciclo creará las n cadenas (recuerde, una por cada punto)
    for index, point in enumerate(initPoints):
        # Se crea el punto inicial, renombrado como p_old, luego será reemplazado por un p_new
        p_old = point
        # Se crea el logaritmo del likelihood relacionado con el punto inicial
        L_old = logLikelihood(x, y, line, sigmaY, p_old)
        # Realmente lo que nos importa es el Posterior, lo calculamos haciendo lo siguiente:
        logPosterior_old = L_old + logPrior(p_old)
        # Se agrega a la cadena de Markov
        markovChain = [[p_old, logPosterior_old]]
        # los elementos de la cadena aceptado siempre inician en 0
        aceptado.append(0)
        
        # Queremos que el algoritom se ejecute "PasosTotales" número de veces.
        for paso in range(pasosTotales):
            # Se define un nuevo punto de parámetros en una vecindad cercana al punto anterior, escogido de manera aleatoria
            p_new = [punto + sigmaX[index]*np.random.randn() for index, punto in enumerate(p_old)]
            # Se crea el logaritmo del likelihood asociado a este nuevo punto.
            L_new = logLikelihood(x, y, line, sigmaY, p_new)
            # Se crea, de nuevo, el posterior
            logPosterior_new = L_new + logPrior(p_new)
        
            # Condiciones para que el nuevo punto sea acepado
            # Que el nuevo likelihood, sea mayor que el anterior o
            # Que la razón entre nuestros likelihoods sea mayor a un número aleatorio.
            if (logPosterior_new>logPosterior_old or logPosterior_new-logPosterior_old>np.random.randn()):
                # Si es así, agregamos nuestro punto a la cadena de Markov y sustituimos nuestros viejos puntos y 
                # likelihood con los nuevos para repetir el proceso después
                markovChain.append([p_new, logPosterior_new])
                p_old = p_new
                logPosterior_old = logPosterior_new
                # Agregamos uno a la suma para nuestra tasa de aceptación
                aceptado[index] += 1
            else:
                # Si no se cumple lo anterior, aún así guardamos el punto creado, sin embargo ya no sustituimos los puntos
                # anteriores con los nuevos, así se repetirá el ciclo pero con los puntos anteriores
                markovChain.append([p_new, logPosterior_new])
        
        # Cada cadena de markov se guarda en nuestra "Matriz de Markov"
        markovMatrix.append(markovChain)
    # Calculamos la tasa de aceptación
    aceptados = tasaAceptacion(aceptado, pasosTotales)        
    # Regresamos nuestra Matriz de Markov y nuestra tasa de aceptación
    return [markovMatrix, aceptados]
    