import tkinter as tk
import random
import requests
from PIL import Image, ImageTk
from io import BytesIO

class MemoryGame:
    def __init__(self, root, tamaño):
        self.root = root
        self.tamaño = tamaño
        self.colores = [
            "#FF5733", "#FFBD33", "#FF33A8", "#33FF57",
            "#33B5FF", "#335BFF", "#8D33FF", "#FF33F4"
        ] * 2  # Duplicar los colores para luego buscar sus parejas

        random.shuffle(self.colores)
        self.cartas = self.colores[:(self.tamaño**2)]
        self.reveladas = []
        self.intentos = 0
        self.botones = []
        self.imagen_placeholder = self.cargar_imagen("https://www.shutterstock.com/shutterstock/photos/2416872153/display_1500/stock-vector-four-poker-playing-card-suits-hearts-diamonds-spades-clubs-playing-cards-icons-isolated-on-2416872153.jpg")
        self.crear_widgets()

    def cargar_imagen(self, url):
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize((100, 100), Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    def crear_widgets(self):
        for i in range(self.tamaño):
            fila = []
            for j in range(self.tamaño):
                btn = tk.Button(self.root, image=self.imagen_placeholder,
                                command=lambda x=i, y=j: self.revelar_carta(x, y))
                btn.grid(row=i, column=j)
                fila.append(btn)
            self.botones.append(fila)

    def revelar_carta(self, fila, col):
        if len(self.reveladas) < 2 and (fila, col) not in self.reveladas:
            self.botones[fila][col].config(bg=self.cartas[fila * self.tamaño + col], image='', text='')
            self.reveladas.append((fila, col))

            if len(self.reveladas) == 2:
                self.intentos += 1
                self.root.after(1000, self.comparar_cartas)

    def comparar_cartas(self):
        (fila1, col1), (fila2, col2) = self.reveladas
        if self.cartas[fila1 * self.tamaño + col1] != self.cartas[fila2 * self.tamaño + col2]:
            self.botones[fila1][col1].config(bg='white', image=self.imagen_placeholder)
            self.botones[fila2][col2].config(bg='white', image=self.imagen_placeholder)
        else:
            self.botones[fila1][col1].config(state='disabled')
            self.botones[fila2][col2].config(state='disabled')

        self.reveladas.clear()
        if self.verificar_ganador():
            self.mostrar_mensaje("¡Felicidades! Has ganado en {} intentos.".format(self.intentos))

    def verificar_ganador(self):
        return all(btn['state'] == 'disabled' for fila in self.botones for btn in fila)

    def mostrar_mensaje(self, mensaje):
        mensaje_ventana = tk.Toplevel(self.root)
        mensaje_ventana.title("Fin del Juego")
        tk.Label(mensaje_ventana, text=mensaje).pack(padx=20, pady=20)
        tk.Button(mensaje_ventana, text="Cerrar", command=mensaje_ventana.destroy).pack(pady=10)

if __name__ == "__main__":
    tamaño = 4
    root = tk.Tk()
    root.title("Juego de Memoria con Colores")
    game = MemoryGame(root, tamaño)
    root.mainloop()