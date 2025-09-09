"""
Práctico de Máquina 1 - Teoría de Información
2. Escribir un programa en lenguaje a elección, que permita:
    a. Ingresar el nombre de un archivo con extensión .bmp
    b. Valide que el archivo sea con el formato adecuado.
    c. Muestre los datos de la cabecera del archivo .bmp
"""

import struct
import os

def leer_cabecera_bmp(nombre_archivo):
    """
    Lee y analiza la cabecera de un archivo BMP
    Retorna un diccionario con la información de la cabecera
    """
    try:
        with open(nombre_archivo, 'rb') as archivo:
            # Leer los primeros 54 bytes (cabecera BMP estándar)
            cabecera = archivo.read(54)
            
            if len(cabecera) < 54:
                return None
            
            # Extraer información de la cabecera usando struct
            # Formato BMP: https://docs.fileformat.com/image/bmp/

            # '<'  = little-endian (orden de bytes)
            # '2s' = 2 bytes como string  
            # 'I'  = unsigned int (4 bytes)
            # 'H'  = unsigned short (2 bytes)
            # 'i'  = signed int (4 bytes)

            # File Header (14 bytes)
            file_header = struct.unpack('<2sIHHI', cabecera[0:14])
            signature = file_header[0].decode('ascii')
            file_size = file_header[1]
            reserved1 = file_header[2]
            reserved2 = file_header[3]
            data_offset = file_header[4]
            
            # Info Header (40 bytes para BITMAPINFOHEADER)
            info_header = struct.unpack('<IiiHHIIiiII', cabecera[14:54])
            header_size = info_header[0]
            width = info_header[1]
            height = info_header[2]
            planes = info_header[3]
            bits_per_pixel = info_header[4]
            compression = info_header[5]
            image_size = info_header[6]
            x_pixels_per_meter = info_header[7]
            y_pixels_per_meter = info_header[8]
            colors_used = info_header[9]
            colors_important = info_header[10]
            
            # Verificar que sea un archivo BMP válido
            if signature != 'BM':
                return None
                
            return {
                'signature': signature,
                'file_size': file_size,
                'reserved1': reserved1,
                'reserved2': reserved2,
                'data_offset': data_offset,
                'header_size': header_size,
                'width': width,
                'height': abs(height),  # height puede ser negativo
                'planes': planes,
                'bits_per_pixel': bits_per_pixel,
                'compression': compression,
                'image_size': image_size,
                'x_pixels_per_meter': x_pixels_per_meter,
                'y_pixels_per_meter': y_pixels_per_meter,
                'colors_used': colors_used,
                'colors_important': colors_important
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
    Muestra la información de la cabecera BMP de forma organizada
    """
    if not info:
        return
        
    print("\n" + "="*50)
    print("INFORMACIÓN DE LA CABECERA DEL ARCHIVO BMP")
    print("="*50)
    
    print(f"Firma/Signature: {info['signature']}")
    print(f"Tamaño del archivo: {info['file_size']} bytes ({info['file_size'] / 1024:.2f} KB)")
    print(f"Reservado 1: {info['reserved1']}")
    print(f"Reservado 2: {info['reserved2']}")
    print(f"Offset de datos: {info['data_offset']} bytes")
    
    print(f"\nInfo Header:")
    print(f"  Tamaño del header: {info['header_size']} bytes")
    print(f"  Ancho: {info['width']} píxeles")
    print(f"  Alto: {info['height']} píxeles")
    print(f"  Planos: {info['planes']}")
    print(f"  Bits por píxel: {info['bits_per_pixel']} bits")
    
    # Interpretar el tipo de compresión
    compression_types = {
        0: "BI_RGB (Sin compresión)",
        1: "BI_RLE8 (RLE 8 bits)",
        2: "BI_RLE4 (RLE 4 bits)",
        3: "BI_BITFIELDS",
        4: "BI_JPEG",
        5: "BI_PNG"
    }
    compression_name = compression_types.get(info['compression'], f"Desconocido ({info['compression']})")
    print(f"  Compresión: {compression_name}")
    
    print(f"  Tamaño de imagen: {info['image_size']} bytes")
    
    # Calcular resolución en DPI si está disponible
    if info['x_pixels_per_meter'] > 0:
        dpi_x = info['x_pixels_per_meter'] * 0.0254
        print(f"  Resolución X: {info['x_pixels_per_meter']} píxeles/metro ({dpi_x:.0f} DPI)")
    else:
        print(f"  Resolución X: {info['x_pixels_per_meter']} píxeles/metro")
        
    if info['y_pixels_per_meter'] > 0:
        dpi_y = info['y_pixels_per_meter'] * 0.0254
        print(f"  Resolución Y: {info['y_pixels_per_meter']} píxeles/metro ({dpi_y:.0f} DPI)")
    else:
        print(f"  Resolución Y: {info['y_pixels_per_meter']} píxeles/metro")
    
    print(f"  Colores usados: {info['colors_used']}")
    print(f"  Colores importantes: {info['colors_important']}")
    
    # Información adicional
    total_pixels = info['width'] * info['height']
    print(f"\nInformación adicional:")
    print(f"  Total de píxeles: {total_pixels:,}")
    print(f"  Aspecto (ratio): {info['width']}/{info['height']} = {info['width']/info['height']:.3f}")
    
    print("="*50)

def validar_extension_bmp(nombre_archivo):
    """
    Valida que el archivo tenga extensión .bmp
    """
    return nombre_archivo.lower().endswith('.bmp')

def main():
    print("ANALIZADOR DE ARCHIVOS BMP")
    print("Práctico de Máquina 1 - Teoría de Información")
    print("-" * 40)
    
    while True:
        # Solicitar nombre del archivo
        nombre_archivo = input("\nIngrese el nombre del archivo BMP (o 'salir' para terminar): ").strip()
        
        if nombre_archivo.lower() == 'salir':
            print("¡Hasta luego!")
            break
            
        if not nombre_archivo:
            print("Error: Debe ingresar un nombre de archivo.")
            continue
            
        # Validar extensión
        if not validar_extension_bmp(nombre_archivo):
            print("Error: El archivo debe tener extensión .bmp")
            continue
            
        # Leer y analizar la cabecera
        info_cabecera = leer_cabecera_bmp(nombre_archivo)
        
        if info_cabecera is None:
            print("Error: El archivo no tiene un formato BMP válido.")
            continue
            
        # Mostrar información
        mostrar_informacion_cabecera(info_cabecera)

if __name__ == "__main__":
    main()