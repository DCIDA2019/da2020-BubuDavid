def distanciasPuntos(datos, bins):
    '''
    Descripción: Calcula las distancias entre todos los puntos de un arreglo y los acomoda en un histograma.
    IN ={
            datos: Los datos a manejar. 
            bins: Una lista con los bins de nuestro histograma.
        }
    OUT: Una lista con la frecuencia de distancias que se encuentran en los rangos de bins.
    '''
    # Transformamos a numpy arreglos para mayor facilidad
    datos = np.array(datos)
    # Creamos un histograma vacío.
    histograma += np.histogram(np.zeros(shape=len(datos)),bins=bins)[0]
    # Recorremos punto por punto, sólo hay que recorrer esto una cantidad "datos" veces gracias a numpy
    for index in datos:
        aux = filter(lambda x: x != 0, np.sum(np.square(datos - index), axis = 1)**(1/2))
        
        # Vamos creando nuestro histograma
        histograma += np.histogram(aux, bins=bins)[0]
    
    # Regresamos nuestro histograma, recordando que tenemos que dividir los valores entre dos porque se repiten.
    return histograma / 2


    datos1