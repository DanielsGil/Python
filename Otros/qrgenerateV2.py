import numpy as np
import reedsolo
import random
from PIL import Image

fila_final = None #Variables usadas globalmente para saber en que cordenada termina el mensaje
col_final = None

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
    
    return np.full((25, 25), 2,dtype=int)  # 1 es blanco, 0 será negro

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

def calcular_relleno_binario(mensaje_terminado):
    
    #Calcula el relleno necesario para completar un mensaje QR al tamaño especificado.
    
    #El tamaño del mensaje debe ser de 44 bytes, esto para QR version 2
    tamano_total = 44
    # Calcular la longitud actual en bytes
    longitud_actual_bits = len(mensaje_terminado)
    longitud_actual_bytes = (longitud_actual_bits + 7) // 8  # Redondear hacia arriba
    
    # Calcular el relleno necesario en bytes
    relleno_necesario = tamano_total - longitud_actual_bytes
    if relleno_necesario <= 0:
        return ""  # No se necesita relleno si ya está lleno

    # Generar el patrón de relleno en bytes
    patron_relleno = [0xEC, 0x11]
    relleno_bytes = []
    for i in range(relleno_necesario):
        relleno_bytes.append(patron_relleno[i % 2])  # Alternar entre 0xEC y 0x11
    
    # Convertir los bytes de relleno a binario
    relleno_binario = ''.join(f"{byte:08b}" for byte in relleno_bytes)

    return relleno_binario

def insertar_mensaje(matriz, mensaje_binario):
    
    #Inserta el mensaje binario en la matriz del QR, incluyendo el modo y la longitud del mensaje.

    global fila_final #Llamamos las variables globales
    global col_final

    # Modo: 0100 (4 bits para binario)
    modo = '0100'
    # Terminadores: indican el final del mensaje
    terminadores = "0000"

    # Tamaño del mensaje en bits (8 bits en binario)
    longitud_mensaje = bin(len(mensaje_binario) // 8)[2:]
    longitud_mensaje = longitud_mensaje.zfill(8)
    
    
    if fila_final == None:
        col = 24  # Comienza desde la última columna 24
        fila = 24  # Comienza desde la última fila 24
        # Combinar modo, longitud y mensaje
        datos = modo + longitud_mensaje + mensaje_binario + terminadores
        #datos = datos + calcular_relleno_binario(datos)
    else:
        #Inicia a insertarse en donde termino el mensaje
        col = col_final
        fila = fila_final
        datos = mensaje_binario #Este es el codigo de correccion de errores 

    print(datos)
    print(len(datos))

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
    
    fila_final = fila
    col_final = col
    print(fila_final,col_final)
    return matriz

def es_area_reservada(fila, col):
    
    #Determina si una celda está reservada para patrones de búsqueda, alineación o formato.
    # Reservar área de patrones de búsqueda
    if (fila < 9 and col > 16) or (fila < 9 and col <9) or (fila >16 and col < 9):
        return True

    # Reservar área del patrón de alineación
    if(fila in [16,17,18,19,20] and col in [16,17,18,19,20]):
        return True

    # Reservar área del patrón de sincronización
    if(fila == 6 and col in [8,9,10,11,12,13,14,15,16]) or (col == 6 and fila in [8,9,10,11,12,13,14,15,16]):
        return True
    
    return False

def reservar_espacios(matriz):
    
    #agrega todos los formatos necesarios para el funcionamiento, sincronizacion, mascaras, etc

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

def calcular_patron_formato():
    # Valores de corrección de error y máscara (en tu caso L y máscara 0)
    correccion_error = 0b01  # Nivel de corrección L
    mascara = 0b000  # Máscara 0
    
    # Calcula el patrón de formato según el nivel de corrección de errores y la máscara
    patron = (correccion_error << 3) | mascara
    
    # Realiza el CRC para obtener los 15 bits del patrón de formato
    patron_crc = patron ^ 0x537  # Esto es el CRC-15 que se utiliza en los códigos QR.
    
    # Retorna el patrón en binario como una cadena de 15 bits
    return f'{patron_crc:015b}'  # Formatea como binario con 15 bits

def generar_correccion_reed_solomon(mensaje_binario):
    # La longitud de los datos y la longitud del código QR
    num_data_codewords = len(mensaje_binario) // 8  # Número de código de datos (en bytes)
    
    # Crear el objeto Reed-Solomon con el número de bloques de corrección
    n_ec_codewords = num_data_codewords // 4  # Número de símbolos de corrección de errores (nivel L)
    rs = reedsolo.RSCodec(n_ec_codewords)
    
    # Convierte el mensaje binario a bytes (agrupando en bloques de 8 bits)
    mensaje_bytes = bytearray(int(mensaje_binario[i:i+8], 2) for i in range(0, len(mensaje_binario), 8))
    
    # Generar el código de corrección Reed-Solomon
    mensaje_con_correccion = rs.encode(mensaje_bytes)  # Devuelve los datos codificados junto con los códigos de corrección
    
    # Extraemos solo los bloques de corrección de errores (últimos bytes)
    bloques_correccion = mensaje_con_correccion[-n_ec_codewords:]
    
    # Convierte los bloques de corrección de errores a binario
    bloques_correccion_binario = ''.join(format(byte, '08b') for byte in bloques_correccion)
    
    return bloques_correccion_binario

def aplicar_mascara(matriz):

    global fila_final
    global col_final

    for fila in range(24, -1, -1):
        for col in range(24, -1, -1):
            # Verificar si no es un área reservada
            if not es_area_reservada(fila, col) and matriz[fila, col] != 2:
                # Aplicar la máscara 0: invierte los módulos si (fila + columna) es par
                if (fila + col) % 2 == 0:
                    matriz[fila, col] = 1 - matriz[fila, col]  # Invertir el valor (0 -> 1, 1 -> 0)

    return matriz

def insertar_relleno_aleatorio(matriz):
    #Inserta los bits de relleno de forma aleatoria (0 o 1) en las celdas vacías de la matriz QR,
    #asegurándose de que no se alteren las áreas reservadas (como los patrones de búsqueda).
    for fila in range(24, -1, -1):
        for col in range(24, -1, -1):
            # Verificar si la celda está vacía y no es parte de los patrones reservados
            if not es_area_reservada(fila, col) and matriz[fila, col] == 2:
                # Asignar un valor aleatorio entre 0 o 1 al bit de relleno
                matriz[fila, col] = random.choice([0, 1])
    return matriz

def insertar_patrondeformato(matriz, patron):
    print(patron)
    matriz[8][0] = 1 - int(patron[0])
    matriz[8][1] = 1 - int(patron[1])
    matriz[8][2] = 1 - int(patron[2])
    matriz[8][3] = 1 - int(patron[3])
    matriz[8][4] = 1 - int(patron[4])
    matriz[8][5] = 1 - int(patron[5])

    matriz[8][7] = 1 - int(patron[6])
    matriz[8][8] = 1 - int(patron[7])

    matriz[7][8] = 1 - int(patron[8])
    matriz[5][8] = 1 - int(patron[9])
    matriz[4][8] = 1 - int(patron[10])
    matriz[3][8] = 1 - int(patron[11])
    matriz[2][8] = 1 - int(patron[12])
    matriz[1][8] = 1 - int(patron[13])
    matriz[0][8] = 1 - int(patron[14])

    matriz[17][8] = 0

    matriz[24][8] = 1 - int(patron[0])
    matriz[23][8] = 1 - int(patron[1])
    matriz[22][8] = 1 - int(patron[2])
    matriz[21][8] = 1 - int(patron[3])
    matriz[20][8] = 1 - int(patron[4])
    matriz[19][8] = 1 - int(patron[5])
    matriz[18][8] = 1 - int(patron[6])
    
    matriz[8][17] = 1 - int(patron[7])
    matriz[8][18] = 1 - int(patron[8])
    matriz[8][19] = 1 - int(patron[9])
    matriz[8][20] = 1 - int(patron[10])
    matriz[8][21] = 1 - int(patron[11])
    matriz[8][22] = 1 - int(patron[12])
    matriz[8][23] = 1 - int(patron[13])
    matriz[8][24] = 1 - int(patron[14])

    return matriz

def save_qr(matriz, filename="qr_code.png"):
    
    #Convierte la matriz en una imagen y guarda el QR resultante.
    
    img = Image.fromarray((matriz * 255).astype('uint8'))  # Convertir 0/1 a 0/255 (negro/blanco)
    img = img.resize((250, 250), Image.NEAREST)  # Redimensionar para mejor visibilidad
    img.save(filename)

# Mensaje de ejemplo
cadena = "www.youtube.com/veritasium"
mensaje_binario = mensaje_codificado(cadena)

# Crear matriz QR
matriz = crear_qr_conmatriz()
matriz = patronesBusqueda(matriz)
matriz = patronAlineacion(matriz)
matriz = reservar_espacios(matriz)

# Insertar mensaje
matriz = insertar_mensaje(matriz, mensaje_binario)

#Obtenemos los bloques de correccion ya listos para insertar y los mandamos a insertar
codigoCorreccion = generar_correccion_reed_solomon(mensaje_binario)
matriz = insertar_mensaje(matriz, codigoCorreccion)

patron_formato = calcular_patron_formato()
matriz = insertar_patrondeformato(matriz, patron_formato)

#aplicar mascara
matriz = aplicar_mascara(matriz)
matriz = insertar_relleno_aleatorio(matriz)

# Guardar el QR
save_qr(matriz)