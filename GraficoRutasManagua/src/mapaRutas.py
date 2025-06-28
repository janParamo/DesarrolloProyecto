import tkinter as tk
from PIL import Image, ImageTk
import os

def mostrar_mapa_rutas(parent, mapa_path):
    ventana = tk.Toplevel(parent)
    ventana.title("Mapa de rutas")
    ventana.geometry("800x600")
    ventana.resizable(True, True)

    if not os.path.exists(mapa_path):
        tk.Label(ventana, text="¡No se encontró la imagen del mapa!", font=("Arial", 16)).pack(pady=30)
        return

    canvas = tk.Canvas(ventana, bg="#222831")
    canvas.pack(fill="both", expand=True)

    mapa_img_original = Image.open(mapa_path)
    mapa_img_zoom = mapa_img_original.copy()
    mapa_img_tk = ImageTk.PhotoImage(mapa_img_zoom)
    mapa_canvas_img = canvas.create_image(0, 0, anchor="nw", image=mapa_img_tk)

    zoom_factor = [1.0]  # Usar lista para mutabilidad en closures

    def actualizar_imagen():
        w, h = mapa_img_original.size
        new_size = (int(w * zoom_factor[0]), int(h * zoom_factor[0]))
        img_zoom = mapa_img_original.resize(new_size, Image.Resampling.LANCZOS)
        nonlocal mapa_img_tk
        mapa_img_tk = ImageTk.PhotoImage(img_zoom)
        canvas.itemconfig(mapa_canvas_img, image=mapa_img_tk)
        canvas.config(scrollregion=canvas.bbox("all"))

    # Variables para arrastrar el mapa
    drag_data = {"x": 0, "y": 0}

    def start_drag(event):
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    def do_drag(event):
        dx = event.x - drag_data["x"]
        dy = event.y - drag_data["y"]
        canvas.move(mapa_canvas_img, dx, dy)
        drag_data["x"] = event.x
        drag_data["y"] = event.y

    canvas.bind("<ButtonPress-1>", start_drag)
    canvas.bind("<B1-Motion>", do_drag)

    def zoom(event):
        if event.delta > 0 or event.num == 4:
            zoom_factor[0] *= 1.1
        elif event.delta < 0 or event.num == 5:
            zoom_factor[0] /= 1.1
        zoom_factor[0] = max(0.2, min(zoom_factor[0], 5))
        actualizar_imagen()
        centrar_imagen()

    canvas.bind("<MouseWheel>", zoom)      # Windows

    def centrar_imagen(event=None):
        canvas_width = canvas.winfo_width()
        canvas_height = canvas.winfo_height()
        img_width = int(mapa_img_zoom.width)
        img_height = int(mapa_img_zoom.height)
        x = max((canvas_width - img_width) // 2, 0)
        y = max((canvas_height - img_height) // 2, 0)
        canvas.coords(mapa_canvas_img, x, y)
        canvas.config(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", lambda e: centrar_imagen())

    actualizar_imagen()
    centrar_imagen()