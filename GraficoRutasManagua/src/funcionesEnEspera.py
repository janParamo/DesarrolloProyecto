

        # --- Lista de solo nombres de rutas, sin paradas (secundario, ahora comentado) ---
        # self.rutas_listbox = tk.Listbox(
        #     left_frame,
        #     font=("Arial", 12),
        #     width=20,
        #     height=22,
        #     bg="#e0f7fa",
        #     highlightthickness=0,
        #     borderwidth=0,
        #     relief="flat"
        # )
        # for ruta in rutas_dict.keys():
        #     self.rutas_listbox.insert(tk.END, f"Ruta {ruta}")
        # self.rutas_listbox.pack(pady=0, fill="y", expand=True)





        # --- Mapa gráfico tradicional (secundario, ahora comentado) ---
        # try:
        #     imagen = Image.open(r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\mapa.png")
        #     imagen = imagen.resize((625, 468), Image.Resampling.LANCZOS)
        #     self.imagen_tk = ImageTk.PhotoImage(imagen)
        #     tk.Label(right_frame, image=self.imagen_tk, bg="#e0f7fa").pack(pady=10)
        # except Exception as e:
        #     tk.Label(right_frame, text=f"No se pudo cargar el mapa: {e}", bg="#e0f7fa", fg="red").pack(pady=10)





    # def mostrar_ruta_en_mapa(self, recorrido):
    #     # Cargar el mapa base
    #     mapa_path = r"c:\Users\landm\OneDrive\Escritorio\DesarrolloProyecto\GraficoRutasManagua\src\mapa.png"
    #     img = Image.open(mapa_path)
    #     fig, ax = plt.subplots(figsize=(8, 6))
    #     ax.imshow(img)
    #     ax.axis('off')
    #
    #    # Posiciones de las paradas (debes adaptar esto a tus coordenadas reales)
    #     posiciones = {
    #         "Mercado Mayoreo": (851, 241),
    #         "Mercado Iván Montenegro": (714, 281),
    #         "Linda Vista": (88, 117),
    #         "Plaza Inter": (309, 158),
    #         "UCA": (328, 305),
    #         "Subasta": (860, 110),
    #         "Metrocentro": (371, 296),
    #         "Zumen": (166, 301),
    #         "Mercado Oriental": (387, 163),
    #         "Mercado Roberto Huembes": (530, 314),
    #         "UNAN": (307, 420),
    #         "Tierra Prometida": (146, 335),
    #         "Mercado Israel": (136, 304),
    #         "Gancho de Camino": (408, 166)
    #     }
    #
    #     # Dibuja nodos y líneas
    #     for i, parada in enumerate(recorrido):
    #         if parada in posiciones:
    #             color = 'red' if i == 0 or i == len(recorrido)-1 else 'green'
    #             ax.plot(*posiciones[parada], 'o', color=color, markersize=12)
    #             ax.text(*posiciones[parada], parada, fontsize=9, color='black', ha='center', va='bottom')
    #             if i > 0 and recorrido[i-1] in posiciones:
    #                 prev = recorrido[i-1]
    #                 ax.plot(
    #                     [posiciones[prev][0], posiciones[parada][0]],
    #                     [posiciones[prev][1], posiciones[parada][1]],
    #                     color='blue', linewidth=2
    #                 )
    #
    #     plt.tight_layout()
    #     plt.show()