import tkinter as tk
from tkinter import messagebox
import os
import pandas as pd

class HistorialDestinos:
    def __init__(self, maxlen=5):
        self.maxlen = maxlen
        self.historial = []
        self.excel_path = os.path.join(os.path.dirname(__file__), r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\excel\historial_destinos.xlsx")
        self.cargar_historial()

    def agregar_destino_si_valido(self, destino, paradas_lista):
        if destino and destino in paradas_lista and (not self.historial or self.historial[-1] != destino):
            if destino in self.historial:
                self.historial.remove(destino)
            self.historial.append(destino)
            if len(self.historial) > self.maxlen:
                # FIFO: elimina el primero (el más antiguo)
                self.historial.pop(0)
            self.guardar_historial()

    def obtener_historial(self):
        return self.historial

    def limpiar_historial(self):
        self.historial.clear()
        self.guardar_historial()

    def guardar_historial(self):
        df = pd.DataFrame({"Destino": self.historial})
        df.to_excel(self.excel_path, index=False)

    def cargar_historial(self):
        if os.path.exists(self.excel_path):
            df = pd.read_excel(self.excel_path)
            self.historial = list(df["Destino"])
        else:
            self.historial = []