import subprocess
import tkinter as tk
from tkinter import messagebox
import time
import os

rastreo_on=False
proceso = None
texto = None



def programar_apagado(entry):

    try:
        # Obtener la hora ingresada y la convertirla a segundos restantes
        hora_apagado = entry.get()
        hora_objetivo = time.strptime(hora_apagado, "%H:%M")
        segundos_objetivo = hora_objetivo.tm_hour * 3600 + hora_objetivo.tm_min * 60

        # Calcular la diferencia en segundos desde el momento actual
        ahora = time.localtime()
        segundos_ahora = ahora.tm_hour * 3600 + ahora.tm_min * 60 + ahora.tm_sec
        segundos_restantes = segundos_objetivo - segundos_ahora

        if segundos_restantes <= 0:
            segundos_restantes += 86400  # Añadir un día si ya pasó la hora

        # Ejecutar el comando de apagado con el tiempo restante
        os.system(f"shutdown /s /t {segundos_restantes}")
        messagebox.showinfo("Apagado Programado", f"El equipo se apagará en {segundos_restantes // 3600} horas y {(segundos_restantes % 3600) // 60} minutos.")
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa la hora en formato HH:MM.")

def iniciar_rastreo(entry):
    #Nombre del archivo
    archivo_sh = "rastreo.sh"

    global texto
    texto = entry.get()
    #Variables a buscar y a modificar
    variable_a_modificar = "proceso="
    nuevo_valor = texto

    #Leer el archivo y modificar el valor
    with open(archivo_sh, "r") as archivo:
        lineas = archivo.readlines()

    #Modificar la línea específica
    with open(archivo_sh, "w") as archivo:
        for linea in lineas:
            #Si la línea contiene la variable a modificar, reemplaza el valor
            if linea.startswith(variable_a_modificar):
                linea = f"{variable_a_modificar}{nuevo_valor}\n"
            archivo.write(linea)
    global proceso
    proceso = subprocess.Popen(['bash', "rastreo.sh"])
    

def crear_analisis():
    # Archivo que almacena la cantidad de segundos que se uso un proceso
    archivo_txt = 'tiempo_acumulado.txt'
    archivo_sh = 'crear_excel.sh'
    global texto #Nombre del proceso anteriormente pedido

    # Leer el contenido del archivo y guardarlo en una variable
    with open(archivo_txt, 'r') as archivo:
        contenido = archivo.read().strip()  

    print(contenido)
    os.remove(archivo_txt)
    #Modificamos el archivo shell para que tenga los valores del analisis

    variable_a_modificar = 'echo "Juan,30" >> archivo.csv'
    nuevo_valor = '"' + f"{texto}" + "," + f"{contenido}" + '"'
    
    with open(archivo_sh, "r") as archivo:
        lineas = archivo.readlines()

    #Modificar una línea específica para cambiar lo que se quiere
    with open(archivo_sh, "w") as archivo:
        for linea in lineas:
            #Si la línea contiene la variable a modificar, reemplaza el valor
            if linea.startswith(variable_a_modificar):
                linea = f"echo {nuevo_valor} >> archivo.csv\n"
            archivo.write(linea)

    subprocess.Popen(['bash', "crear_excel.sh"])
    
# Configuración de la ventana de Tkinter
inicio = tk.Tk()
inicio.title("PC MANAGER")
inicio.geometry("400x300")


def interfaz_principal():
    
    inicio.withdraw()

    ventana_principal = tk.Toplevel()
    ventana_principal.title("PC MANAGER")
    ventana_principal.geometry("400x500")

    tk.Label(ventana_principal, text="Qué deseas realizar? ", font=(2)).pack(pady=30)

    c_excelbutton = tk.Button(ventana_principal, text="Proceso de rastreo", width=20, height=3 ,command=interfazRastreo)#Igualamos a lambda para que command nos permita pasar argumentos a la funcion
    c_excelbutton.pack(pady=10)

    copiar_button = tk.Button(ventana_principal, text="Crear copia de seguridad", width=20, height=3 ,command=lambda: subprocess.Popen(f'start cmd /c copiar_archivos.bat', shell=True))#Igualamos a lambda para que command nos permita pasar argumentos a la funcion
    copiar_button.pack(pady=10)

    apagar_button = tk.Button(ventana_principal, text="Apagar el ordenador", width=20, height=3 ,command=programarApagado)#Igualamos a lambda para que command nos permita pasar argumentos a la funcion
    apagar_button.pack(pady=10)

def programarApagado():
    
    inicio.withdraw()

    apagado = tk.Toplevel()
    apagado.title("Programación del apagado")
    apagado.geometry("400x500")

    label_hora = tk.Label(apagado, text="Ingresa la hora de apagado (HH:MM):")
    label_hora.pack()

    entry_hora = tk.Entry(apagado)
    entry_hora.pack()

    boton_apagar = tk.Button(apagado, text="Programar Apagado", command=lambda: programar_apagado(entry_hora))
    boton_apagar.pack()

def interfazRastreo():

    inicio.withdraw()

    rastreo = tk.Toplevel()
    rastreo.title("Programación del monitoreo de un proceso")
    rastreo.geometry("400x200")
    global rastreo_on
    global proceso
    if rastreo_on is False:
        label_rastreo = tk.Label(rastreo, text="Ingrese el nombre especifico del\n proceso que desea monitorear:")
        label_rastreo.pack()

        entry_proceso = tk.Entry(rastreo)
        entry_proceso.pack()

        boton_rastreo = tk.Button(rastreo, text="Rastrear proceso", command=lambda: [iniciar_rastreo(entry_proceso), rastreo.destroy()])
        boton_rastreo.pack()

        rastreo_on=True
    else:
        label_Frastreo = tk.Label(rastreo, text="Ya se encuentra activo un rastreo \n ¿Desea finalizar el rastreo y generar el analisis?:")
        label_Frastreo.pack()

        boton_FinRastreo = tk.Button(rastreo, text="Finalizar rastreo", command=lambda: [proceso.terminate(),crear_analisis(), rastreo.destroy()])
        boton_FinRastreo.pack()
        rastreo_on=False
    
    
# Texto
tk.Label(inicio, text="Bienvenido a PC MANAGER" , font=(2)).pack(pady=20)
tk.Label(inicio, text="Controle su pc, por ende, su vida" , font=(2)).pack(pady=0)
# Botón para un archivo .bat
iniciar_button = tk.Button(inicio, text="Encender",font=(2), width=10, height=10 ,command=interfaz_principal) 
iniciar_button.pack(pady=50)


# Ejecuta la ventana principal de la interfaz
inicio.mainloop()
