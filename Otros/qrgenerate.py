import tkinter as tk
#import reedsolo

informacion = input("Digite un link para generarle un QR: ")
lista_binarios = [] 
contador_patrones = 1

#Creamos la interfaz
pantalla = tk.Tk()
pantalla.title("Codigo QR")
pantalla.geometry("500x500")

#El canvas en la plantilla sobre la que podemos dibujar, la ponemos encima de toda la interfaz.
canvas = tk.Canvas(pantalla, width=500, height=500)
canvas.pack()

#En el canvas dibujamos los puntos negros (Bits = 1)
def dibujar_cuadrado(x, y):
   
    canvas.create_rectangle(x, y, x + 20, y + 20, fill="black")

#Generaremos los 4 patrones de busqueda como un prefab del codigo QR

def patronDebusqueda_1(): #El de arriba a la iz
    #120 por que se debe hacer 7 veces - el tamano de 1 para que encaje y cada uno ocupa 20 pixeles, estoy usando el mismo estilo del video
    j = 0 
    while j < 120: #Pinta la linea horizontal de arriba izq-der
        dibujar_cuadrado(j,0)
        j += 20

    j = 0
    while j < 120: #Pinta la linea vertical derecha, arriba-abajo
        dibujar_cuadrado(120,j)
        j += 20

    j = 120    
    while j >= 0: #Pinta la liea horizontal de abajo, der-izq
        dibujar_cuadrado(j,120)
        j -= 20

    j = 120
    while j >= 0: #Pinta la linea vertical izquierda, abajo-arriba
        dibujar_cuadrado(0,j)
        j -= 20
    #Esto genera el cuadrado negro 7x7
    i = 40
    while i <=80:
        j = 40
        while j <= 80:
            dibujar_cuadrado(j,i)
            j +=20
        i +=20
    #Esto genera el cuadrado interno 3x3

def patronDebusqueda_2(): #El de abajo a la izq

    j = 0 #120 por que se debe hacer 7 veces - el tamano de 1 para que encaje y cada uno ocupa 20 pixeles, estoy usando el mismo estilo del video
    while j < 120: 
        dibujar_cuadrado(j,360)
        j += 20
    j = 360
    while j < 480:
        dibujar_cuadrado(120,j)
        j += 20
    j = 120    
    while j >= 0: 
        dibujar_cuadrado(j,480)
        j -= 20
    j = 480
    while j >= 360:
        dibujar_cuadrado(0,j)
        j -= 20
    #Esto genera el cuadrado negro 7x7
    i = 400
    while i <=440:
        j = 40
        while j <= 80:
            dibujar_cuadrado(j,i)
            j +=20
        i +=20
    #Esto genera el cuadrado interno 3x3 
    
def patronDebusqueda_3(): #El de arriba a la derecha

    j = 360
    while j < 500: #120 por que se debe hacer 7 veces - el tamano de 1 para que encaje y cada uno ocupa 20 pixeles, estoy usando el mismo estilo del video
        dibujar_cuadrado(j,0)
        j += 20

    j = 0
    while j < 120:
        dibujar_cuadrado(480,j)
        j += 20
        
    j = 500    
    while j >= 360: 
        dibujar_cuadrado(j,120)
        j -= 20

    j = 120
    while j >= 0:
        dibujar_cuadrado(360,j)
        j -= 20
    #Esto genera el cuadrado negro 7x7
    i = 40
    while i <=80:
        j = 400
        while j <= 440:
            dibujar_cuadrado(j,i)
            j +=20
        i +=20
    #Esto genera el cuadrado interno 3x3

def patronDebusqueda_4(): #El de abajo a la derecha
    #320 en y, 320 en x
    j = 320 
    while j < 400: #Hasta 400 porque hasta ahi va el cuadrado en la interfaz 400px
        dibujar_cuadrado(j,320)
        j += 20
    j = 320
    while j < 400: #Y es igual, en un 5x5, 5 cuadrados de 20px, 320 + 100 - 20px, se le resta 20 por eso que no se explicar pero que entiendo
        dibujar_cuadrado(400,j)
        j += 20
    j = 400    
    while j >= 320: 
        dibujar_cuadrado(j,400)
        j -= 20
    j = 400
    while j >= 320:
        dibujar_cuadrado(320,j)
        j -= 20
    #Esto genera el cuadrado negro 7x7
    
    dibujar_cuadrado(360,360)
    #Esto genera el cuadrado interno 3x3

    
def pixels(): #Pixel que el video no explica para que sirve y el pixel que informan el formato, en este caso binario 0100
    dibujar_cuadrado(160,340)
    dibujar_cuadrado(460,480)

#------------------------------------------------------------------------------------------------------------------------
#Ahora los patrones de temporizacion, las lineas que definen la version del QR

def patron_vertical_version():
    j = 160 
    while j < 340: 
        dibujar_cuadrado(120,j)
        j += 40

def patron_horizontal_version():
    j = 160 
    while j < 340: #
        dibujar_cuadrado(j,120)
        j += 40

patronDebusqueda_1()
patronDebusqueda_2()
patronDebusqueda_3()
patronDebusqueda_4()
pixels()

patron_horizontal_version()
patron_vertical_version()


#A partir de este punto sera el verdadero codigo

def decimal_binario(numero):
    
    binario = bin(numero)[2:]  # Convierte en binario y elimina el prefijo '0b'
    binario_como_byte = binario.zfill(8)  # Rellena con ceros a la izquierda hasta tener 8 bits
    
    return str(binario_como_byte)

#Posiblemente la funcion mas importante del codigo, dibuja los bits como cuadros negros cuando encuentre un 1 en la cadena dada, este es para definir el tamano del mensaje
def dibujar_cuadrados_bits_tamano(cadena):
    
    contador = 0
    j = 500
    aux_j = 480 
    k = 440     # debe poner el primero en (480,440)

    for i in cadena:

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if i == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

#Hacemos una funcion por cada tipo de patron
def patron_vertical_arriba(cadena):

    contador = 0

    if contador_patrones == 1:
        j = 500
        k = 360
    if contador_patrones == 2:
        j = 500
        k=  280
    if contador_patrones == 9:
        j = 420
        k=  260
    if contador_patrones == 13:
        j = 340
        k=  480
    aux_j = j - 20

    for i in cadena:

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if i == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_3(cadena):

    contador = 0

    j = 500
    k = 200
    aux_j = j - 20
    

    for i in range(4):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

    contador = 0

    j = 460
    k= 180

    aux_j = j - 20
      

    for i in range(4,8):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_vertical_abajo(cadena):
    contador = 0

  
    if contador_patrones == 4:
        j = 460
        k = 220
    if contador_patrones == 5:
        j = 460
        k = 300
    if contador_patrones == 6:
        j = 460
        k = 380
    if contador_patrones == 11:
        j = 380
        k = 240
    if contador_patrones == 12:
        j = 380
        k = 420
    aux_j = j - 20

    for i in cadena:

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if i == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_7(cadena):
    contador = 0

    j = 460
    k = 460
    aux_j = j - 20
    
    for i in range(4):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

    contador = 0

    j = 420
    k= 480

    aux_j = j - 20
      
    for i in range(4,8):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_8(cadena):
    contador = 0

    
    j = 420
    k=  440
    aux_j = j - 20

    for i in range(4):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

    j = 420
    k=  320
    aux_j = j - 20

    for i in range(4,8):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_10(cadena):
    
    j = 420
    k=  180
    aux_j = j - 20

    for i in range(2):
   
        j -= 20
         
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)

    contador = 0
    j = 380
    k=  180
    aux_j = j - 20

    for i in range(2,8):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_14(cadena):
        
    j = 300
    k = 420
   
    for i in range(5):

        k -= 20
                
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
   
    if cadena[5] == '1':
        dibujar_cuadrado(320,300)
    if cadena[6] == '1': 
        dibujar_cuadrado(300,300)
    if cadena[7] == '1':    
        dibujar_cuadrado(320,280)             
        
def patron_tetris_arriba(cadena):

    if contador_patrones == 15:
        j = 300
        k = 280

    if contador_patrones ==17:
        j = 300
        k = 100

    if contador_patrones == 25:
        j = 220
        k = 440

    if contador_patrones == 26:
        j = 220
        k = 360    
    if cadena[0] == '1':
        dibujar_cuadrado(j,k)
    if cadena[7] == '1':
        dibujar_cuadrado(j+20,k-80)
    k -= 20
    j += 40
    contador = 0
    aux_j = j - 20

    for i in range(1,7):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_16(cadena):
    
    j = 300
    k = 200
    if cadena[0] == '1':
        dibujar_cuadrado(j,k)
    if cadena[7] == '1':
        dibujar_cuadrado(j+20,k-100)
    k -= 20
    j += 40
    contador = 0
    aux_j = j - 20

    for i in range(1,7):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k -= 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_18(cadena):

    if cadena[0] == '1':
        dibujar_cuadrado(300, 20)
    if cadena[1] == '1':
        dibujar_cuadrado(320, 0)
    if cadena[2] == '1':
        dibujar_cuadrado(300, 0)
    if cadena[3] == '1':
        dibujar_cuadrado(280, 0)
    if cadena[4] == '1':
        dibujar_cuadrado(260, 0)
    if cadena[5] == '1':
        dibujar_cuadrado(280, 20)
    if cadena[6] == '1':
        dibujar_cuadrado(260, 20)
    if cadena[7] == '1':
        dibujar_cuadrado(280, 40)

def patron_19(cadena):
    
    j = 260
    k = 40

    if cadena[0] == '1':
        dibujar_cuadrado(j,k)
    if cadena[7] == '1':
        dibujar_cuadrado(j+20,k+100)

    k += 20
    j += 40
    contador = 0
    aux_j = j - 20

    for i in range(1,7):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_tetris_abajo(cadena):

    if contador_patrones == 20:
        j = 260
        k = 140
    if contador_patrones == 21:
        j = 260
        k = 220
    if contador_patrones == 22:
        j = 260
        k = 300
    if contador_patrones == 23:
        j = 260
        k = 380
    if cadena[0] == '1':
        dibujar_cuadrado(j,k)
    if cadena[7] == '1':
        dibujar_cuadrado(j+20,k+80)

    k += 20
    j += 40
    contador = 0
    aux_j = j - 20

    for i in range(1,7):

        if contador < 2:
            j -= 20
        else:
            j = aux_j
            k += 20
            contador = 0
            
        if cadena[i] == '1':
            dibujar_cuadrado(j,k)
        
        contador += 1

def patron_24(cadena):

    if cadena[0] == '1':
        dibujar_cuadrado(260, 460)
    if cadena[1] == '1':
        dibujar_cuadrado(280, 480)
    if cadena[2] == '1':
        dibujar_cuadrado(260, 480)
    if cadena[3] == '1':
        dibujar_cuadrado(240, 480)
    if cadena[4] == '1':
        dibujar_cuadrado(220, 480)
    if cadena[5] == '1':
        dibujar_cuadrado(240, 460)
    if cadena[6] == '1':
        dibujar_cuadrado(220, 460)
    if cadena[7] == '1':
        dibujar_cuadrado(240, 440)

# Toda la parte de codificar el mensaje e imprimirlo
def pasar_ascii(cadena):#Creamos la lista con los valores en binario
    
    for i in cadena:
        lista_binarios.append(decimal_binario(ord(i))) #lista que guardara byte por byte los caracteres de el mensaje del usuario
        
tam_msj = len(informacion)

mensaje = decimal_binario(tam_msj)
dibujar_cuadrados_bits_tamano(mensaje)     
pasar_ascii(informacion)

for h in lista_binarios:
    if contador_patrones in (1,2,9,13):
        patron_vertical_arriba(h)
    if contador_patrones == 3:
        patron_3(h)
    if contador_patrones in (4,5,6,11,12):
        patron_vertical_abajo(h)
    if contador_patrones == 7:
        patron_7(h)
    if contador_patrones == 8:
        patron_8(h)
    if contador_patrones == 10:
        patron_10(h)
    if contador_patrones == 14:
        patron_14(h)
    if contador_patrones in (15,17,25,26):
        patron_tetris_arriba(h)
    if contador_patrones == 16:
        patron_16(h)
    if contador_patrones == 18:
        patron_18(h)
    if contador_patrones == 19:
        patron_19(h)
    if contador_patrones in (20,21,22,23):
        patron_tetris_abajo(h)
    if contador_patrones == 24:
        patron_24(h)
    contador_patrones += 1


def dibujar_cuadricula(canvas, ancho, alto, tam_celda): #Realmente era muy complicado calcular los px sin cuadriculas, esto lo hizo chat gpt
    
    for x in range(0, ancho, tam_celda):
        canvas.create_line(x, 0, x, alto, fill="gray")
    
    
    for y in range(0, alto, tam_celda):
        canvas.create_line(0, y, ancho, y, fill="gray")

dibujar_cuadricula(canvas, 500, 500, 20)        

#def calcular_bytes_correcion(mensaje):
    # Convertir el mensaje en bytes
    #datos_bytes = [ord(char) for char in mensaje]

    # Configurar Reed-Solomon para obtener 10 bytes de corrección
    #rs = reedsolo.RSCodec(10)  # Configuramos para generar 10 bytes de corrección

    # Codificar los datos y obtener los bytes de corrección
    #datos_codificados = rs.encode(bytes(datos_bytes))

    # Los últimos 10 bytes son los bytes de corrección
    #bytes_correcion = datos_codificados[-10:]

    # Retornar como una lista de enteros
    #return list(bytes_correcion)

#print(calcular_bytes_correcion(informacion))

pantalla.mainloop()