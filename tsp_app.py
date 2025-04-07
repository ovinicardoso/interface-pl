import tkinter as tk
from tkinter import messagebox
import random

class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Otimização de Rotas - PCV")
        
        self.frame = tk.Frame(self.master)
        self.frame.pack(padx=200, pady=160)
        
        tk.Button(self.frame, text="Métodos Básicos", command=self.open_basic_methods).pack(pady=5)
        tk.Button(self.frame, text="Algoritmos Genéticos", state=tk.DISABLED).pack(pady=5)
        tk.Button(self.frame, text="Sobre o Sistema", command=self.show_about).pack(pady=5)
    
    def open_basic_methods(self):
        BasicMethodsWindow(tk.Toplevel(self.master))
    
    def show_about(self):
        about_text = """Aplicação do Problema do Caixeiro Viajante (PCV) na área de Logística e Transporte para a roteirização de entregas.

Desenvolvido por:
- Izaque Nogueira e Vinicius Cardoso"""
        messagebox.showinfo("Sobre o Sistema", about_text)

class BasicMethodsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Métodos Básicos")
        
        self.problem_size = tk.StringVar()
        self.distance_matrix = []
        self.solution = []
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.master, text="Tamanho do Problema:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(self.master, textvariable=self.problem_size).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.master, text="Usar Padrão (5)", command=lambda: self.problem_size.set("5")).grid(row=0, column=2, padx=5, pady=5)
        
        tk.Button(self.master, text="Gerar Problema", command=self.gerarProblema).grid(row=1, columnspan=3, pady=10)
        
        self.results_text = tk.Text(self.master, height=10, width=50)
        self.results_text.grid(row=2, columnspan=3, padx=5, pady=5)
        
        methods = ["Força Bruta", "Vizinho Mais Próximo"]
        self.method_var = tk.StringVar(value=methods[0])
        
        self.method_menu = tk.OptionMenu(self.master, self.method_var, *methods)
        self.method_menu.grid(row=3, column=0, pady=5)
        self.method_menu.configure(state=tk.DISABLED)
        tk.Button(self.master, text="Executar Método", state=tk.DISABLED).grid(row=3, column=1, pady=5)
    
    def gerarProblema(self):
        try:
            size = int(self.problem_size.get() or 5)
        except ValueError:
            size = 5
        
        self.distance_matrix = [[random.randint(1, 100) for _ in range(size)] for _ in range(size)]
        
        self.solution = random.sample(range(size), size)
        
        total_distance = sum(
            self.distance_matrix[self.solution[i]][self.solution[(i+1)%size]]
            for i in range(size)
        )
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "Problema Gerado!\n")
        self.results_text.insert(tk.END, f"Tamanho: {size} cidades\n")
        self.results_text.insert(tk.END, f"Solução Inicial: {self.solution}\n")
        self.results_text.insert(tk.END, f"Distância Total: {total_distance}")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()