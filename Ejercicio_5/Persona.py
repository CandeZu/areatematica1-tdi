class PersonaFija:
    def __init__(self, apNom, dir, dni, estudiosP, estudiosS, estudiosU, casa, obraSocial, trabaja, casado, jubilado):
        #Definimos el nombre con tamaño 40
        if len(apNom) < 40:
            self.ApNom = apNom + (" "*(40-len(apNom)))
        elif len(apNom) > 40:
            self.ApNom = apNom[:40]
        else:
            self.ApNom = apNom
        
        #Definimos dirección con tamaño 40
        if len(dir) < 40:
            self.Dir = dir + (" "*(40-len(dir)))
        elif len(dir) > 40:
            self.Dir = dir[:40]
        else:
            self.Dir = dir
        
        #Definimos el dni con tamaño 8
        self.Dni = dni[:8]
        
        #Definimos los campos bivaluados con S/N
        self.ByteBivaluado = self.Bivaluado(estudiosP, estudiosS, estudiosU, casa, obraSocial, trabaja, casado, jubilado)
        self.campos=enumerate(["estudiosPrimarios", "estudiosS", "estudiosU", "casa", "obraSocial", "trabaja", "casado", "jubilado"])

    def Bivaluado(self, eP, eS, eU, c, oS, t, a, j):
        #Definimos un byte en 0
        byte = int('00000000',2)
        #Por cada caracteristica se setea un bit del byte en 1 o 0 dependiendo si es S o N, respectivamente, 
        #esto se hace con una operación OR entre el byte y una máscara
        if eP == 'S':
            byte = byte | int('10000000',2)
        if eS == 'S':
            byte = byte | int('01000000',2)
        if eU == 'S':
            byte = byte | int('00100000',2)
        if c == 'S':
            byte = byte | int('00010000',2)
        if oS == 'S':
            byte = byte | int('00001000',2)
        if t == 'S':
            byte = byte | int('00000100',2)
        if a == 'S':
            byte = byte | int('00000010',2)
        if j == 'S':
            byte = byte | int('00000001',2)
        return byte

    def Mostrar(self):
        print(f"Apellido y Nombre: {self.ApNom}")
        print(f"Dirección: {self.Dir}")
        print(f"DNI: {self.Dni}")

        #Definimos una máscara para verificar cada uno de los bits del byte en cuestión
        byteMask = int('10000000',2)
        for i,j in self.campos:
            if self.ByteBivaluado & byteMask == 0:
                print(f"{j}: Si")
            else:
                print(f"{j}: No")
            byteMask = byteMask >> 1 #Desplazo la máscara un bit a la derecha para verificar el siguiente bit del byte


class PersonaVariable:
    def __init__(self, apNom, dir, dni, estudiosP, estudiosS, estudiosU, casa, obraSocial, trabaja, casado, jubilado):
        self.ApNom = apNom
        self.Dir = dir
        self.Dni = dni[:8]
        self.ByteBivaluado = self.Bivaluado(estudiosP, estudiosS, estudiosU, casa, obraSocial, trabaja, casado, jubilado)
        self.campos=enumerate(["estudiosP", "estudiosS", "estudiosU", "casa", "obraSocial", "trabaja", "casado", "jubilado"])

    def Mostrar(self):
        print(f"Apellido y Nombre: {self.ApNom}")
        print(f"Dirección: {self.Dir}")
        print(f"DNI: {self.Dni}")

        #Definimos una máscara para verificar cada uno de los bits del byte en cuestión
        byteMask = int('10000000',2)
        for i,j in self.campos:
            if self.ByteBivaluado & byteMask == 0:
                print(f"{j}: Si")
            else:
                print(f"{j}: No")
            byteMask = byteMask >> 1

    def Bivaluado(self, eP, eS, eU, c, oS, t, a, j):
        byte = int('00000000',2)
        if eP == 'S':
            byte = byte | int('10000000',2)
        if eS == 'S':
            byte = byte | int('01000000',2)
        if eU == 'S':
            byte = byte | int('00100000',2)
        if c == 'S':
            byte = byte | int('00010000',2)
        if oS == 'S':
            byte = byte | int('00001000',2)
        if t == 'S':
            byte = byte | int('00000100',2)
        if a == 'S':
            byte = byte | int('00000010',2)
        if j == 'S':
            byte = byte | int('00000001',2)
        return byte


