from math import log2
from collections import Counter # Counter cuenta cuantas veces aparece cada símbolo
#l=log2 

def entropia(probabilidades):
    #cálculo de entropía a partir de una lista con probabilidades
    return -sum(p * log2(p) for p in probabilidades if p > 0)

def calculo(ruta):
    # Leer archivo en modo binario para que sirva con cualquier tipo de archivo (txt, exe y zip).
    with open(ruta, "rb") as x: #el rb es para abrirlo y que lea los bytes
        datos = x.read() #en datos se meten los bytes 
    
    total = len(datos)
    if total == 0:
        return None #para evitar divisiones por cero

    # Independiente 
    frecuencias = Counter(datos) #cuenta los bytes que hay en datos
    probabilidades = [cant / total for cant in frecuencias.values()] # Queda una lista por ejemplo [0.5, 0.5]
    entropInd = entropia(probabilidades)

    
    #Entropía máxima posible= log2(len(frecuencias))
    redundancind = 1 - (entropInd / log2(len(frecuencias)))

    # Dependiente 
    pares = [(datos[i], datos[i+1]) for i in range(total-1)]
    #si los datos son [65,66,67,69] -> [(65,66),(66,67), (67,68)]
    total_pares = len(pares)
    frecuenciasPares = Counter(pares)
    probabilidadesPares = [x / total_pares for x in frecuenciasPares.values()]
    entropDep = entropia(probabilidadesPares)

    # Máxima entropía para pares (n^2 posibles)
    #H_max_pares = log2(len(frecuenciasPares))
    redundanciaDep = 1 - (entropDep / log2(len(frecuenciasPares)))

    return {
        "Archivo": ruta,
        "Entropia Independiente": entropInd,
        "Redundancia Independiente": redundancind,
        "Entropia Dependiente": entropDep,
        "Redundancia Dependiente": redundanciaDep
    }


if __name__ == "__main__":
    #archivo = "texto.txt"  
    #archivo = "enpdf.pdf"  
    #archivo = "zipeado.zip"  
    archivo = "executable.exe"  
    resultados = calculo(archivo)
    if resultados:
        for nombre, valor in resultados.items():
            print(f"{nombre}: {valor}")


#nombre sería "Archivo" y valor sería ruta

#probar si puedo mandar todos los archivos y que los vaya escribiendo uno por uno