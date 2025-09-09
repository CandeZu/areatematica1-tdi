import socket

# LÓGICA DE COMPRESIÓN 

# alfabeto para pasar de letra a código binario
c_compresion = {
    'A': '000', 'B': '001', 'C': '010', 'D': '011',
    'E': '100', 'F': '101', 'G': '110', 'H': '111'
}

def comprimir(texto):
    """
    Toma un texto y lo convierte a su representación binaria según el alfabeto.
    """
    resultado_binario = ""
    for char in texto.upper(): # Convertimos a mayúsculas por si acaso
        if char in c_compresion:
            resultado_binario += c_compresion[char]
            
        # Los espacios y otros caracteres que no están en el alfabeto se ignoran
    return resultado_binario 

#  CONFIGURACIÓN DEL SOCKET CLIENTE 

HOST = '127.0.0.1'  # La dirección IP del servidor (localhost)
PORT = 65432        # El puerto que está usando el servidor

# Ingresar por consola el mensaje a enviar
mensaje_original = input("Ingrese un mensaje (solo letras A-H y espacios): ")


# Comprimimos el mensaje antes de enviarlo
mensaje_comprimido = comprimir(mensaje_original)

print("--- Proceso de Compresión ---")
print(f"Mensaje original: {mensaje_original}")
print(f"Mensaje comprimido a enviar: {mensaje_comprimido}")

# Usamos 'with' para garantizar que el socket se cierre automáticamente
# Protocolo TCP e IPv4
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect((HOST, PORT)) # Intenta conectarse al servidor
        print(f"\n Conectado al servidor en {HOST}:{PORT}")
        
        # Codifica el mensaje comprimido (de string a bytes) y lo envía
        s.sendall(mensaje_comprimido.encode('utf-8'))
        
        print("[*] Mensaje enviado exitosamente.")

    except ConnectionRefusedError:
        print("[*] Error: No se pudo establecer la conexión. Comprobar si el servidor está en ejecución.")