import numpy as np

def informacion_mutua(Pxy, Px, Py):
    """
    Calcula I(X;Y) = sum_x sum_y P(x,y) * log2( P(x,y) / (Px(x)*Py(y)) )
    """
    I = 0.0
    for i in range(len(Px)):
        for j in range(len(Py)):
            if Pxy[i, j] > 0:
                I += Pxy[i, j] * np.log2(Pxy[i, j] / (Px[i] * Py[j]))
    return I


def capacidad_grid(W, paso):

    R = W.shape[0] #Calcula el R, por ejemplo si viniera una matriz de 2x3 entonces el shape daría como resultado 2
    #Todavía se permite matrices incorrectas
    
    #incialización
    mejor_I = -1
    mejor_Px = None

    # Generamos distribuciones de entrada que sumen 1
    if R == 2:
        for p in np.arange(0, 1+paso, paso): #Osea de 0,05 -> 0,10->0,15 hasta llegar a 1
            #print(p)
            Px = np.array([p, 1-p]) # [0.3,0.7]
            Py = Px @ W  # el producto matricial -> [0.34,0.66]
            
            Pxy = np.outer(Px, np.ones(R)) * W #parte complicada pero básicamente se usa un vector de unos para (np.ones) 'copiar' cada Px en las columnas y poder así multiplicar toda la matriz con W
            #y para la multiplicación se usa el np.outer
            I = informacion_mutua(Pxy, Px, Py)
            if I > mejor_I:
                mejor_I = I
                mejor_Px = Px

    elif R == 3:
        for p1 in np.arange(0, 1+paso, paso):
            for p2 in np.arange(0, 1-p1+paso, paso):
                p3 = 1 - p1 - p2
                if p3 < -1e-9:  # evitamos negativos por redondeo
                    continue
                Px = np.array([p1, p2, p3])
                Py = Px @ W
                Pxy = np.outer(Px, np.ones(R)) * W
                I = informacion_mutua(Pxy, Px, Py)
                if I > mejor_I:
                    mejor_I = I
                    mejor_Px = Px

    elif R == 4:
        for p1 in np.arange(0, 1+paso, paso):
            for p2 in np.arange(0, 1-p1+paso, paso):
                for p3 in np.arange(0, 1-p1-p2+paso, paso):
                    p4 = 1 - p1 - p2 - p3
                    if p4 < -1e-9:
                        continue
                    Px = np.array([p1, p2, p3, p4])
                    Py = Px @ W
                    Pxy = np.outer(Px, np.ones(R)) * W
                    I = informacion_mutua(Pxy, Px, Py)
                    if I > mejor_I:
                        mejor_I = I
                        mejor_Px = Px

    return mejor_I, mejor_Px


# ------------------ EJEMPLO ------------------

# Canal binario simétrico con error 0.1 
#Revisar para mandar esto por una entrada de datos (?) --> Sería más molesto pero a su vez tengo que comprobar que cada línea sea 1
W = np.array([[0.9, 0.1],
              [0.1, 0.9]])

#W[i,j] = P(Y=j| X=i) osea si se envía 0 hay un 90% de probabilidades de recibir 0
# por eso el 0.9, 0.1 

capacidad, Px_opt = capacidad_grid(W, paso=0.05) #paso para encontrar la mejor distribución, se puede probar con otros números parecidos
print("Capacidad aproximada:", capacidad, "bits")
print("Distribución óptima de entrada:", Px_opt)
