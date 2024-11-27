import numpy as np
from PIL import Image

def mensaje_codificado(cadena):

    lista_cadena_ascii = []
    binario_msj = ''
    for i in cadena:
        lista_cadena_ascii.append(str(ord(i)))

    for i in lista_cadena_ascii:

        cadena_binario = bin(int(i))[2:]  # Convierte en binario y elimina el prefijo '0b'
        cadena_binario = cadena_binario.zfill(8)
        binario_msj += str(cadena_binario)

    return(binario_msj)

def crear_qr_conmatriz():
    
    #Crear una matriz inicializada en blanco (1).
    
    return np.ones((25, 25), dtype=int)  # 1 es blanco, 0 será negro

def patronesBusqueda(matriz):

 
    size = matriz.shape[0]
    positions = [(0, 0), (0, size - 7), (size - 7, 0)]  # Esquinas (sup izq, sup der, inf izq)

    for x, y in positions:
        # Dibujar el patrón de 7x7 (cuadrado interno)
        for i in range(7):
            for j in range(7):
                if i in [0, 6] or j in [0, 6] or (2 <= i <= 4 and 2 <= j <= 4):
                    matriz[x + i, y + j] = 0  # Negro

        # Rodear con borde de 8x8 (borde blanco exterior)
        for i in range(-1, 8):
            for j in range(-1, 8):
                if 0 <= x + i < size and 0 <= y + j < size:  # Verificar límites
                    if i in [-1, 7] or j in [-1, 7]:
                        matriz[x + i, y + j] = 1  # Blanco

    return matriz

def patronAlineacion(matriz):
    
    size = matriz.shape[0]
    alignment_position = size - 9  # Coordenada del patrón de alineación para versión 2 (20, 20)

    x, y = alignment_position, alignment_position

    # Dibujar el patrón de alineación (5x5)
    for i in range(5):
        for j in range(5):
            if i in [0, 4] or j in [0, 4] or (i == 2 and j == 2):
                matriz[x + i, y + j] = 0  # Negro
            else:
                matriz[x + i, y + j] = 1  # Blanco

    return matriz

def insertar_mensaje(matriz, mensaje_binario):
    
    #Inserta el mensaje binario en la matriz del QR, incluyendo el modo y la longitud del mensaje.
    
    # Modo: 0100 (4 bits para binario)
    modo = '0100'

    # Tamaño del mensaje en bits (8 bits en binario)
    longitud_mensaje = bin(len(mensaje_binario) // 8)[2:]
    longitud_mensaje = longitud_mensaje.zfill(8)
    print(longitud_mensaje)

    # Combinar modo, longitud y mensaje
    datos = modo + longitud_mensaje + mensaje_binario

    print(datos)
    size = matriz.shape[0]
    
    col = size - 1  # Comienza desde la última columna 24
    fila = size - 1  # Comienza desde la última fila 24 
    
    direction = -1  # Zigzag (-1: hacia arriba, 1: hacia abajo)
    datos_index = 0  # Índice actual en los datos
    cambio = 0 # Para saber cuando cambiar la fila 
    topeArriba = 0 # para saber cuando cambiar el sentido
    topeAbajo = 2
    while datos_index < len(datos) and col >= 0:
        # Ignorar áreas reservadas
        if not es_area_reservada(fila, col):
            matriz[fila, col] = 1 - int(datos[datos_index])  # Insertar bit
            datos_index += 1

        # Mover al siguiente módulo
        if direction == -1:  # Zigzag hacia arriba
            if topeAbajo < 2:
                col -= 1
                cambio = 1
                topeAbajo += 1
            else:
                if fila > 0:
                    if cambio > 0:
                        fila -= 1
                        col += 1
                        cambio = 0
                    else:
                        cambio = 1
                        col -= 1 
                else:  # Llegó al borde superior, cambia de columna
                    if cambio > 0:
                        fila -= 1
                        col += 1
                        cambio = 0
                    else:
                        cambio = 1          
                        col -= 1
                    direction = 1
                    topeAbajo = 0
        else:  # Zigzag hacia abajo
            if topeArriba < 2:
                col -= 1
                cambio = 1
                topeArriba +=1
            else:
                if fila < 24:
                    if cambio > 0:
                        fila += 1
                        col += 1
                        cambio = 0
                    else:
                        cambio = 1
                        col -= 1
                else:  # Llegó al borde inferior, cambia de columna
                    if cambio > 0:
                        fila += 1
                        col += 1
                        cambio = 0
                    else:
                        cambio = 1
                        col -= 1
                    cambio = 0
                    direction = -1
                    topeArriba = 0
    return matriz

def es_area_reservada(fila, col):
    
    #Determina si una celda está reservada para patrones de búsqueda, alineación o formato.
    # Reservar área de patrones de búsqueda
    if (fila < 9 and col > 16) or (fila < 9 and col <8) or (fila >16 and col < 9):
        return True

    # Reservar área del patrón de alineación
    if(fila in [16,17,18,19,20] and col in [16,17,18,19,20]):
        return True

    return False

def reservar_espacios(matriz):
    
    #agrega todos los formatos necesarios para el funcionamiento, sincronizacion, mascaras, etc
    size = matriz.shape[0]

    #1 - Agrega las pautas de sincronización (alternancia negro-blanco)
    #   en la fila 6 y columna 6 dentro de las áreas definidas.
    
    # Horizontal: Fila 6, columnas de 8 a 16
    for col in range(8, 17):  # Incluye 16
        if matriz[6, col] != -1:  # No sobrescribir áreas reservadas
            matriz[6, col] = col % 2  # Alterna negro (0) y blanco (1)
    
    # Vertical: Columna 6, filas de 8 a 16
    for row in range(8, 17):  # Incluye 16
        if matriz[row, 6] != -1:  # No sobrescribir áreas reservadas
            matriz[row, 6] = row % 2  # Alterna negro (0) y blanco (1)
    return matriz

def calcular_formato(correction_level='L', mask_pattern=0):
    """
    Calcula el formato binario para el nivel de corrección y la máscara dada.
    Incluye la corrección BCH para el formato.
    """
    # Mapas para los niveles de corrección
    correction_bits = {'L': '01', 'M': '00', 'Q': '11', 'H': '10'}
    
    # Asegurar que los valores sean válidos
    if correction_level not in correction_bits or not (0 <= mask_pattern <= 7):
        raise ValueError("Nivel de corrección o máscara inválidos.")
    
    # Construir los primeros 5 bits del formato
    formato_inicial = correction_bits[correction_level] + f"{mask_pattern:03b}"
    
    # Polinomio generador BCH
    generator = 0b10100110111
    
    # Convertir el formato inicial en un entero
    formato = int(formato_inicial, 2) << 10  # Desplazar 10 bits a la izquierda

    # Calcular el resto de la división (CRC)
    for i in range(len(formato_inicial) + 10 - 11, -1, -1):
        if (formato >> (i + 10)) & 1:
            formato ^= generator << i

    # Añadir los 10 bits de corrección al formato inicial
    formato_final = (int(formato_inicial, 2) << 10) | formato

    # Aplicar máscara XOR fija (0b101010000010010)
    formato_final ^= 0b101010000010010

    return f"{formato_final:015b}"  # Devolver 15 bits como string

def agregar_formato(matriz, formato_binario):
    """
    Inserta el formato calculado en las posiciones definidas en el QR.
    """
    size = matriz.shape[0]
    
    # Horizontal (fila 8)
    for i in range(6):  # Col 0-5
        matriz[8, i] = 1 - int(formato_binario[i])  # Negar porque 0 = negro
    for i in range(6, 8):  # Col 7-8
        matriz[8, size - 8 + i - 6] = 1 - int(formato_binario[i])  # Salto al borde derecho

    # Vertical (columna 8)
    for i in range(6):  # Fila 0-5
        matriz[i, 8] = 1 - int(formato_binario[i])  # Negar porque 0 = negro
    for i in range(6, 8):  # Fila 7-8
        matriz[size - 8 + i - 6, 8] = 1 - int(formato_binario[i])

    return matriz


def save_qr(matriz, filename="qr_code.png"):
    
    #Convierte la matriz en una imagen y guarda el QR resultante.
    
    img = Image.fromarray((matriz * 255).astype('uint8'))  # Convertir 0/1 a 0/255 (negro/blanco)
    img = img.resize((250, 250), Image.NEAREST)  # Redimensionar para mejor visibilidad
    img.save(filename)

# Mensaje de ejemplo
cadena = "www.daniel.com"
mensaje_binario = mensaje_codificado(cadena)

# Crear matriz QR
matriz = crear_qr_conmatriz()
matriz = patronesBusqueda(matriz)
matriz = patronAlineacion(matriz)
matriz = reservar_espacios(matriz)
formato_binario = calcular_formato('L', 0)
matriz_codificada = agregar_formato(matriz, formato_binario)
# Insertar mensaje
matriz = insertar_mensaje(matriz, mensaje_binario)

# Guardar el QR
save_qr(matriz)



