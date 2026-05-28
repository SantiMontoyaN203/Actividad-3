import math
import os
import tkinter as tk
from tkinter import ttk, messagebox

class Figura3D:
    def __init__(self):
        self.volumen = 0.0
        self.superficie = 0.0
    def calcular_volumen(self) -> float:
        return 0.0
    def calcular_superficie(self) -> float:
        return 0.0

class Cilindro(Figura3D):
    def __init__(self, radio: float, altura: float):
        super().__init__()
        self.radio = radio
        self.altura = altura
    def calcular_volumen(self):
        self.volumen = math.pi * (self.radio ** 2) * self.altura
        return self.volumen
    def calcular_superficie(self):
        self.superficie = 2 * math.pi * self.radio * (self.radio + self.altura)
        return self.superficie

class Esfera(Figura3D):
    def __init__(self, radio: float):
        super().__init__()
        self.radio = radio
    def calcular_volumen(self):
        self.volumen = (4/3) * math.pi * (self.radio ** 3)
        return self.volumen
    def calcular_superficie(self):
        self.superficie = 4 * math.pi * (self.radio ** 2)
        return self.superficie

class Piramide(Figura3D):
    def __init__(self, lado_base: float, altura: float, apotema: float):
        super().__init__()
        self.lado_base = lado_base
        self.altura = altura
        self.apotema = apotema
    def calcular_volumen(self):
        area_base = self.lado_base ** 2
        self.volumen = (1/3) * area_base * self.altura
        return self.volumen
    def calcular_superficie(self):
        area_base = self.lado_base ** 2
        perimetro_base = self.lado_base * 4
        area_lateral = (perimetro_base * self.apotema) / 2
        self.superficie = area_base + area_lateral
        return self.superficie

class Cubo(Figura3D):
    def __init__(self, lado: float):
        super().__init__()
        self.lado = lado
    def calcular_volumen(self):
        self.volumen = self.lado ** 3
        return self.volumen
    def calcular_superficie(self):
        self.superficie = 6 * (self.lado ** 2)
        return self.superficie


class Prisma(Figura3D):
    def __init__(self, largo: float, ancho: float, altura: float):
        super().__init__()
        self.largo = largo
        self.ancho = ancho
        self.altura = altura
    def calcular_volumen(self):
        self.volumen = self.largo * self.ancho * self.altura
        return self.volumen
    def calcular_superficie(self):
        self.superficie = 2 * (self.largo * self.ancho + self.largo * self.altura + self.ancho * self.altura)
        return self.superficie

class InterfazFiguras:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Calculadora Geométrica 3D")
        self.ventana.geometry("650x550")
        self.ventana.resizable(False, False)
        self.entradas = {}
        self.imagen_actual = None
        self.imagenes_config = {
            "Cilindro": "cilindro.png",
            "Esfera": "esfera.png",
            "Pirámide": "piramide.png",
            "Cubo": "cubo.png",
            "Prisma": "prisma.png"
        }
        self.crear_componentes()

    def crear_componentes(self):
        lbl_titulo = tk.Label(self.ventana, text="Cálculo de Volumen y Superficie", font=("Arial", 16, "bold"))
        lbl_titulo.pack(pady=10)
        frame_selector = tk.LabelFrame(self.ventana, text=" Configuración de la Figura ", font=("Arial", 10, "bold"), padx=10, pady=10)
        frame_selector.pack(fill="x", padx=20, pady=5)
        tk.Label(frame_selector, text="Seleccione una figura:", font=("Arial", 10)).grid(row=0, column=0, padx=5, sticky="w")
        self.combo_figuras = ttk.Combobox(frame_selector, values=list(self.imagenes_config.keys()), state="readonly", font=("Arial", 10))
        self.combo_figuras.grid(row=0, column=1, padx=5)
        self.combo_figuras.bind("<<ComboboxSelected>>", self.cambiar_figura)
        self.frame_central = tk.Frame(self.ventana)
        self.frame_central.pack(fill="both", expand=True, padx=20, pady=10)
        self.frame_entradas = tk.LabelFrame(self.frame_central, text=" Parámetros (cm) ", font=("Arial", 10, "bold"), padx=10, pady=10)
        self.frame_entradas.pack(side="left", fill="both", expand=True, padx=(0, 10))
        self.frame_imagen = tk.LabelFrame(self.frame_central, text=" Vista Previa ", font=("Arial", 10, "bold"), padx=10, pady=10)
        self.frame_imagen.pack(side="right", fill="both", expand=True)
        self.lbl_imagen_placeholder = tk.Label(self.frame_imagen, text="Seleccione una figura\npara ver su imagen", font=("Arial", 9, "italic"), fg="gray")
        self.lbl_imagen_placeholder.pack(expand=True)
        frame_inferior = tk.Frame(self.ventana, padx=10, pady=10)
        frame_inferior.pack(fill="x", padx=20, pady=10)
        self.btn_calcular = tk.Button(frame_inferior, text="Calcular Estadísticas", font=("Arial", 11, "bold"), bg="#2196F3", fg="white", command=self.ejecutar_calculo, state="disabled")
        self.btn_calcular.pack(fill="x", pady=5)
        self.lbl_volumen = tk.Label(frame_inferior, text="Volumen: ---", font=("Arial", 12, "bold"), fg="#4CAF50", anchor="w")
        self.lbl_volumen.pack(fill="x", pady=2)
        self.lbl_superficie = tk.Label(frame_inferior, text="Superficie: ---", font=("Arial", 12, "bold"), fg="#FF9800", anchor="w")
        self.lbl_superficie.pack(fill="x", pady=2)
        self.combo_figuras.current(0)
        self.cambiar_figura(None)

    def cambiar_figura(self, event):
        figura = self.combo_figuras.get()
        self.btn_calcular.config(state="normal")
        for widget in self.frame_entradas.winfo_children():
            widget.destroy()
        self.entradas.clear()
        campos = []
        if figura == "Cilindro":
            campos = ["Radio", "Altura"]
        elif figura == "Esfera":
            campos = ["Radio"]
        elif figura == "Pirámide":
            campos = ["Lado de la Base", "Altura", "Apotema"]
        elif figura == "Cubo":
            campos = ["Lado (Arista)"]
        elif figura == "Prisma":
            campos = ["Largo de Base", "Ancho de Base", "Altura"]
        for i, nombre_campo in enumerate(campos):
            lbl = tk.Label(self.frame_entradas, text=f"{nombre_campo}:", font=("Arial", 10))
            lbl.grid(row=i, column=0, sticky="e", pady=5, padx=5)
            entry = tk.Entry(self.frame_entradas, font=("Arial", 10), width=15)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entradas[nombre_campo] = entry
        self.actualizar_imagen(figura)

    def actualizar_imagen(self, nombre_figura):
        nombre_archivo = self.imagenes_config[nombre_figura]
        carpeta_actual = os.path.dirname(os.path.abspath(__file__))
        ruta_absoluta_imagen = os.path.join(carpeta_actual, nombre_archivo)
        try:
            self.imagen_actual = tk.PhotoImage(file=ruta_absoluta_imagen)
            self.lbl_imagen_placeholder.config(image=self.imagen_actual, text="")
        except tk.TclError:
            self.lbl_imagen_placeholder.config(
                image="", 
                text=f"[ Imagen: {nombre_archivo} ]\n(Coloca el archivo en la carpeta\npara que se visualice)",
                fg="blue"
            )

    def ejecutar_calculo(self):
        figura_seleccionada = self.combo_figuras.get()
        valores_numericos = {}
        try:
            for nombre, entry in self.entradas.items():
                valor_texto = entry.get().strip()
                if not valor_texto:
                    raise ValueError(f"El campo '{nombre}' no puede estar vacío.")
                valor_float = float(valor_texto)
                if valor_float <= 0:
                    raise ValueError(f"El valor de '{nombre}' debe ser mayor a 0.")
                valores_numericos[nombre] = valor_float
        except ValueError as e:
            messagebox.showerror("Error de Entrada", str(e) if "mayor a 0" in str(e) or "vacío" in str(e) else "Por favor, ingresa solo números válidos en los campos.")
            return
        obj_figura = None
        if figura_seleccionada == "Cilindro":
            obj_figura = Cilindro(valores_numericos["Radio"], valores_numericos["Altura"])
        elif figura_seleccionada == "Esfera":
            obj_figura = Esfera(valores_numericos["Radio"])
        elif figura_seleccionada == "Pirámide":
            obj_figura = Piramide(valores_numericos["Lado de la Base"], valores_numericos["Altura"], valores_numericos["Apotema"])
        elif figura_seleccionada == "Cubo":
            obj_figura = Cubo(valores_numericos["Lado (Arista)"])
        elif figura_seleccionada == "Prisma":
            obj_figura = Prisma(valores_numericos["Largo de Base"], valores_numericos["Ancho de Base"], valores_numericos["Altura"])

        if obj_figura:
            vol = obj_figura.calcular_volumen()
            sup = obj_figura.calcular_superficie()
            self.lbl_volumen.config(text=f"Volumen: {vol:.2f} cm³")
            self.lbl_superficie.config(text=f"Superficie: {sup:.2f} cm²")

if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazFiguras(root)
    root.mainloop()