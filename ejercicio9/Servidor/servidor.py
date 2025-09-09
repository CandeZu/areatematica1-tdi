import socket

# LÓGICA DE DESCOMPRESIÓN

# El alfabeto inverso para pasar de código binario a letra
c_descomprension = {
    '000': 'A', '001': 'B', '010': 'C', '011': 'D',
    '100': 'E', '101': 'F', '110': 'G', '111': 'H'
}

def descomprimir(datos_binarios):
    """
    Toma una cadena de bits y la convierte de nuevo al texto original.
    """
    texto_original = ""
    # Leemos la cadena de 3 en 3 caracteres (la longitud de cada código)
    for i in range(0, len(datos_binarios), 3):
        chunk = datos_binarios[i:i+3]
        if chunk in c_descomprension:
            texto_original += c_descomprension[chunk]
    return texto_original

# CONFIGURACIÓN DEL SOCKET SERVIDOR

HOST = '127.0.0.1'  # Dirección IP local (localhost)
PORT = 65432        # Puerto para escuchar (puede ser cualquiera > 1023)

# Usamos 'with' para garantizar que el socket se cierre automáticamente
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT)) # Asocia el socket con la dirección y el puerto
    s.listen() # Pone el socket en modo de escucha para aceptar conexiones

    print(f" [*] Servidor escuchando en {HOST}:{PORT}")
    print(" [*] Esperando a que un cliente se conecte...")

    # Acepta una nueva conexión. Esto es un punto de bloqueo.
    # El código no continuará hasta que un cliente se conecte.
    conn, addr = s.accept()

    with conn:
        print(f"Conexión establecida con {addr}")
        
        # Recibe los datos del cliente en un búfer de 1024 bytes
        datos_recibidos = conn.recv(1024)
        
        # Decodifica los bytes a una cadena de texto (UTF-8)
        datos_comprimidos = datos_recibidos.decode('utf-8')
        
        print("\n--- Proceso de Descompresión ---")
        print(f"Recibido (comprimido): {datos_comprimidos}")
        
        # Llama a la función para descomprimir
        mensaje_descomprimido = descomprimir(datos_comprimidos)
        
        print(f"Mensaje original (descomprimido): {mensaje_descomprimido}")
        print("\n[*] Proceso finalizado. Cerrando conexión.")