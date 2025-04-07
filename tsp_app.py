import tkinter as tk
from tkinter import messagebox
import random


class MainApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Otimização de Rotas - PCV")
        self.master.geometry("500x300")
        self.master.minsize(400, 200)

        self.configure_grid()
        self.create_widgets()

    def configure_grid(self):
        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

    def create_widgets(self):
        main_frame = tk.Frame(self.master)
        main_frame.grid(row=0, column=0, sticky='nsew')

        main_frame.grid_rowconfigure(3, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)

        pad_options = {'padx': 10, 'pady': 10}
        btn_style = {
            'width': 20,
            'height': 2
        }

        tk.Button(main_frame, text="Métodos Básicos",
                  command=self.open_basic_methods, **btn_style).grid(
            row=0, column=0, **pad_options)

        tk.Button(main_frame, text="Algoritmos Genéticos",
                  state=tk.DISABLED, **btn_style).grid(
            row=1, column=0, **pad_options)

        tk.Button(main_frame, text="Sobre o Sistema",
                  command=self.show_about, **btn_style).grid(
            row=2, column=0, **pad_options)

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
        self.master.geometry("600x400")
        self.master.minsize(500, 300)

        self.problem_size = tk.StringVar()
        self.distance_matrix = []
        self.solution = []

        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        self.master.grid_rowconfigure(2, weight=1)
        for col in range(3):
            self.master.grid_columnconfigure(col, weight=1)

    def create_widgets(self):
        pad_options = {'padx': 5, 'pady': 5}
        entry_width = 15

        tk.Label(self.master, text="Tamanho do Problema:").grid(
            row=0, column=0, sticky='e', **pad_options)

        tk.Entry(self.master, textvariable=self.problem_size,
                 width=entry_width).grid(row=0, column=1, sticky='ew', **pad_options)

        tk.Button(self.master, text="Usar Padrão (5)",
                  command=lambda: self.problem_size.set("5")).grid(
            row=0, column=2, sticky='w', **pad_options)

        tk.Button(self.master, text="Gerar Problema",
                  command=self.gerarProblema).grid(
            row=1, column=1, sticky='ew', **pad_options)

        self.results_text = tk.Text(self.master, wrap=tk.WORD)
        self.results_text.grid(row=2, columnspan=3,
                               sticky='nsew', **pad_options)

        scrollbar = tk.Scrollbar(self.master, command=self.results_text.yview)
        scrollbar.grid(row=2, column=3, sticky='ns')
        self.results_text.config(yscrollcommand=scrollbar.set)

        methods = ["Força Bruta", "Vizinho Mais Próximo"]
        self.method_var = tk.StringVar(value=methods[0])

        self.method_menu = tk.OptionMenu(
            self.master, self.method_var, *methods)
        self.method_menu.grid(row=3, column=0, sticky='ew', **pad_options)
        self.method_menu.configure(state=tk.DISABLED)

        tk.Button(self.master, text="Executar Método",
                  state=tk.DISABLED).grid(row=3, column=1, sticky='ew', **pad_options)

    def gerarProblema(self):
        try:
            size = int(self.problem_size.get() or 5)
        except ValueError:
            size = 5

        self.distance_matrix = [
            [random.randint(1, 100) for _ in range(size)] for _ in range(size)]

        self.solution = random.sample(range(size), size)

        total_distance = sum(
            self.distance_matrix[self.solution[i]][self.solution[(i+1) % size]]
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
