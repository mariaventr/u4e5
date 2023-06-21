import requests
import tkinter as tk
from tkinter import messagebox
import json

class CinefilosArgentinosApp:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://api.themoviedb.org/3'
        self.generos = self.obtener_generos()
        self.peliculas = self.obtener_peliculas_populares()

        self.ventana = tk.Tk()
        self.ventana.title("Cinéfilos Argentinos")
        self.ventana.geometry("400x300")

        self.listbox = tk.Listbox(self.ventana)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        for pelicula in self.peliculas:
            self.listbox.insert(tk.END, pelicula['title'])
        self.listbox.bind("<Double-Button-1>", self.mostrar_detalles_pelicula)

    def obtener_generos(self):
        generos = {}
        try:
            with open('generos.json', 'r') as file:
                data = json.load(file)

                generos = {}
                for genero in data['genres']:
                    generos[genero['id']] = genero['name']

        except FileNotFoundError:
            messagebox.showerror('Error', 'No se encontró el archivo de géneros.')
        except json.JSONDecodeError:
            messagebox.showerror('Error', 'Error al decodificar el archivo de géneros.')
        return generos

    def obtener_peliculas_populares(self):
        peliculas_populares = []
        try:
            url = f'{self.base_url}/discover/movie?api_key={self.api_key}&language=es'
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            peliculas_populares = data['results']
        except requests.exceptions.RequestException as e:
            messagebox.showerror('Error de conexión', str(e))
        return peliculas_populares


    def mostrar_detalles_pelicula(self, event):
        widget = event.widget
        index = int(widget.curselection()[0])
        pelicula = self.peliculas[index]

        generos_pelicula = []

        for genero_id in pelicula['genre_ids']:
            genero = self.generos.get(genero_id)
            if genero:
                generos_pelicula.append(genero)

        generos_str = ', '.join(generos_pelicula)

        messagebox.showinfo(
            pelicula['title'],
            f"Título: {pelicula['title']}\n"
            f"Resumen: {pelicula['overview']}\n"
            f"Lenguaje original: {pelicula['original_language']}\n"
            f"Fecha de lanzamiento: {pelicula['release_date']}\n"
            f"Géneros: {generos_str}"
        )

    def run(self):
        self.ventana.mainloop()
    

if __name__ == '__main__':
    api_key = '73d0d4618e15d50f7d8f09c8c0de4845'
    app = CinefilosArgentinosApp(api_key)
    app.run()
