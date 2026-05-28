import math
import tkinter as tk
from tkinter import messagebox

class CalculadorNotas:
    def __init__(self, notas: list[float]):
        self.notas = notas

    def calcular_promedio(self) -> float:
        return sum(self.notas) / len(self.notas)

    def obtener_mayor(self) -> float:
        return max(self.notas)

    def obtener_menor(self) -> float:
        return min(self.notas)

    def calcular_desviacion(self) -> float:
        promedio = self.calcular_promedio()
        suma_cuadrados = 0.0
        for nota in self.notas:
            diferencia = nota - promedio
            suma_cuadrados += diferencia ** 2
        varianza = suma_cuadrados / len(self.notas)
        desviacion = math.sqrt(varianza)
        return desviacion

class InterfazNotas(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Control de Notas Estudiantiles")
        self.geometry("500x450")
        self.resizable(False, False)
        self.campos_notas = []
        self.iniciar_componentes()

    def iniciar_componentes(self):
        lbl_titulo = tk.Label(self, text="Ingreso de Notas", font=("Arial", 14, "bold"))
        lbl_titulo.pack(pady=15)
        frame_entradas = tk.Frame(self)
        frame_entradas.pack(pady=10)

        for i in range(5):
            fila = tk.Frame(frame_entradas)
            fila.pack(pady=5, fill="x")
            lbl_nota = tk.Label(fila, text=f"Nota {i+1}: ", font=("Arial", 11), width=8, anchor="w")
            lbl_nota.pack(side="left")
            txt_nota = tk.Entry(fila, font=("Arial", 11), width=8)
            txt_nota.pack(side="left", padx=5)
            self.campos_notas.append(txt_nota)

        btn_calcular = tk.Button(
            self, 
            text="Calcular Estadísticas", 
            font=("Arial", 11, "bold"), 
            bg="#2196F3", 
            fg="white", 
            command=self.ejecutar_calculo
        )
        btn_calcular.pack(pady=20)
        lbl_separador = tk.Label(self, text="---------------- Resultados ----------------", fg="gray")
        lbl_separador.pack()
        self.lbl_promedio = tk.Label(self, text="Promedio: -", font=("Arial", 11))
        self.lbl_promedio.pack(anchor="w", padx=40, pady=2)
        self.lbl_desviacion = tk.Label(self, text="Desviación Estándar: -", font=("Arial", 11))
        self.lbl_desviacion.pack(anchor="w", padx=40, pady=2)
        self.lbl_mayor = tk.Label(self, text="Mayor Nota: -", font=("Arial", 11))
        self.lbl_mayor.pack(anchor="w", padx=40, pady=2)
        self.lbl_menor = tk.Label(self, text="Menor Nota: -", font=("Arial", 11))
        self.lbl_menor.pack(anchor="w", padx=40, pady=2)

    def ejecutar_calculo(self):
        try:
            notas_numericas = []
            for campo in self.campos_notas:
                texto = campo.get().strip()
                if not texto:
                    raise ValueError("Todos los campos de notas deben ser completados.")
                nota = float(texto.replace(",", "."))
                if nota < 0:
                    raise ValueError("Las notas no pueden ser negativas.")
                notas_numericas.append(nota)

            calculador = CalculadorNotas(notas_numericas)
            promedio = calculador.calcular_promedio()
            desviacion = calculador.calcular_desviacion()
            mayor = calculador.obtener_mayor()
            menor = calculador.obtener_menor()
            self.lbl_promedio.config(text=f"Promedio: {promedio:.2f}")
            self.lbl_desviacion.config(text=f"Desviación Estándar: {desviacion:.2f}")
            self.lbl_mayor.config(text=f"Mayor Nota: {mayor:.2f}")
            self.lbl_menor.config(text=f"Menor Nota: {menor:.2f}")

        except ValueError as err:
            messagebox.showerror("Error de Entrada", f"Por favor verifica los datos ingresados.\nDetalle: {err}")

if __name__ == "__main__":
    app = InterfazNotas()
    app.mainloop()