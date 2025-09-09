"""
Práctico de Máquina 1 - Teoría de Información
1. Escribir un programa en lenguaje a elección, que permita:
    a. Ingresar el nombre de un archivo con extensión .wav
    b. Valide que el archivo sea con el formato adecuado.
    c. Muestre los datos de la cabecera del archivo .wav
"""

import struct
import os

def leer_cabecera_wav(nombre_archivo):
    """
    Lee y analiza la cabecera de un archivo WAV
    Retorna un diccionario con la información de la cabecera
    """
    try:
        with open(nombre_archivo, 'rb') as archivo:
            # Leer los primeros 44 bytes (cabecera WAV estándar)
            cabecera = archivo.read(44)
            
            if len(cabecera) < 44:
                return None
            
            # Extraer información de la cabecera usando struct
            # Formato WAV: https://docs.fileformat.com/audio/wav/

            # '<'  = little-endian (orden de bytes)
            # '4s' = 4 bytes como string
            # 'I'  = unsigned int (4 bytes)
            # 'H'  = Entero sin signo 2 bytes

            # RIFF Header (12 bytes)
            riff_header = struct.unpack('<4sI4s', cabecera[0:12])
            chunk_id = riff_header[0].decode('ascii')
            chunk_size = riff_header[1]
            format_type = riff_header[2].decode('ascii')
            
            # fmt Subchunk (24 bytes)
            fmt_header = struct.unpack('<4sIHHIIHH', cabecera[12:36])
            subchunk1_id = fmt_header[0].decode('ascii')
            subchunk1_size = fmt_header[1]
            audio_format = fmt_header[2]
            num_channels = fmt_header[3]
            sample_rate = fmt_header[4]
            byte_rate = fmt_header[5]
            block_align = fmt_header[6]
            bits_per_sample = fmt_header[7]
            
            # data Subchunk header (8 bytes)
            data_header = struct.unpack('<4sI', cabecera[36:44])
            subchunk2_id = data_header[0].decode('ascii')
            subchunk2_size = data_header[1]
            
            # Verificar que sea un archivo WAV válido
            if chunk_id != 'RIFF' or format_type != 'WAVE':
                return None
                
            return {
                'chunk_id': chunk_id,
                'chunk_size': chunk_size,
                'format': format_type,
                'subchunk1_id': subchunk1_id,
                'subchunk1_size': subchunk1_size,
                'audio_format': audio_format,
                'num_channels': num_channels,
                'sample_rate': sample_rate,
                'byte_rate': byte_rate,
                'block_align': block_align,
                'bits_per_sample': bits_per_sample,
                'subchunk2_id': subchunk2_id,
                'subchunk2_size': subchunk2_size
            }
            
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no existe.")
        return None
    except PermissionError:
        print(f"Error: No se tiene permiso para leer el archivo '{nombre_archivo}'.")
        return None
    except Exception as e:
        print(f"Error inesperado al leer el archivo: {e}")
        return None

def mostrar_informacion_cabecera(info):
    """
    Muestra la información de la cabecera WAV de forma organizada
    """
    if not info:
        return
        
    print("\n" + "="*50)
    print("INFORMACIÓN DE LA CABECERA DEL ARCHIVO WAV")
    print("="*50)
    
    print(f"Identificador RIFF: {info['chunk_id']}")
    print(f"Tamaño del chunk: {info['chunk_size']} bytes")
    print(f"Formato: {info['format']}")
    
    print(f"\nSubchunk fmt:")
    print(f"  ID: {info['subchunk1_id']}")
    print(f"  Tamaño: {info['subchunk1_size']} bytes")
    
    # Interpretar el formato de audio
    formato_audio = "PCM" if info['audio_format'] == 1 else f"Formato {info['audio_format']}"
    print(f"  Formato de audio: {formato_audio}")
    
    print(f"  Número de canales: {info['num_channels']} ({'Mono' if info['num_channels'] == 1 else 'Estéreo' if info['num_channels'] == 2 else 'Multicanal'})")
    print(f"  Frecuencia de muestreo: {info['sample_rate']} Hz")
    print(f"  Tasa de bytes: {info['byte_rate']} bytes/segundo")
    print(f"  Alineación de bloque: {info['block_align']} bytes")
    print(f"  Bits por muestra: {info['bits_per_sample']} bits")
    
    print(f"\nSubchunk data:")
    print(f"  ID: {info['subchunk2_id']}")
    print(f"  Tamaño de datos de audio: {info['subchunk2_size']} bytes")
    
    # Calcular duración aproximada
    if info['byte_rate'] > 0:
        duracion_segundos = info['subchunk2_size'] / info['byte_rate']
        minutos = int(duracion_segundos // 60)
        segundos = duracion_segundos % 60
        print(f"  Duración aproximada: {minutos}:{segundos:05.2f}")
    
    print("="*50)

def validar_extension_wav(nombre_archivo):
    """
    Valida que el archivo tenga extensión .wav
    """
    return nombre_archivo.lower().endswith('.wav')

def main():
    print("ANALIZADOR DE ARCHIVOS WAV")
    print("Práctico de Máquina 1 - Teoría de Información")
    print("-" * 40)
    
    while True:
        # Solicitar nombre del archivo
        nombre_archivo = input("\nIngrese el nombre del archivo WAV (o 'salir' para terminar): ").strip()
        
        if nombre_archivo.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        if not nombre_archivo:
            print("Error: Debe ingresar un nombre de archivo.")
            continue
            
        # Validar extensión
        if not validar_extension_wav(nombre_archivo):
            print("Error: El archivo debe tener extensión .wav")
            continue
            
        # Leer y analizar la cabecera
        info_cabecera = leer_cabecera_wav(nombre_archivo)
        
        if info_cabecera is None:
            print("Error: El archivo no tiene un formato WAV válido.")
            continue
            
        # Mostrar información
        mostrar_informacion_cabecera(info_cabecera)

if __name__ == "__main__":
    main()
