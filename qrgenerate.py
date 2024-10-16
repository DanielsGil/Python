import tkinter as tk


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

#Generaremos los 3 patrones de busqueda como un prefab del codigo QR
def patronDebusqueda_1():
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

def patronDebusqueda_2():

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
    #  

def patronDebusqueda_3():

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


patronDebusqueda_1()
patronDebusqueda_2()
patronDebusqueda_3()


pantalla.mainloop()
