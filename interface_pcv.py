import tkinter as tk
from tkinter import messagebox, ttk
import random
import math
import copy


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

Algoritmos implementados:
- Subida de Encosta
- Subida de Encosta Alterada
- Têmpera Simulada

Desenvolvido por:
- Izaque Nogueira e Vinicius Cardoso"""
        messagebox.showinfo("Sobre o Sistema", about_text)


class BasicMethodsWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Métodos de Otimização - PCV")
        self.master.geometry("900x700")
        self.master.minsize(800, 600)

        self.problem_size = tk.StringVar()
        self.distance_matrix = []
        self.solution = []
        self.current_distance = 0

        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        self.master.grid_rowconfigure(3, weight=1)
        for col in range(4):
            self.master.grid_columnconfigure(col, weight=1)

    def create_widgets(self):
        pad_options = {'padx': 5, 'pady': 5}
        entry_width = 15

        # Frame para configuração do problema
        config_frame = tk.LabelFrame(self.master, text="Configuração do Problema")
        config_frame.grid(row=0, columnspan=4, sticky='ew', **pad_options)

        tk.Label(config_frame, text="Tamanho do Problema:").grid(
            row=0, column=0, sticky='e', **pad_options)

        tk.Entry(config_frame, textvariable=self.problem_size,
                 width=entry_width).grid(row=0, column=1, sticky='ew', **pad_options)

        tk.Button(config_frame, text="Usar Padrão (5)",
                  command=lambda: self.problem_size.set("5")).grid(
            row=0, column=2, sticky='w', **pad_options)

        tk.Button(config_frame, text="Gerar Problema",
                  command=self.gerarProblema, bg='lightblue').grid(
            row=0, column=3, sticky='ew', **pad_options)

        # Frame para exibição da matriz
        matrix_frame = tk.LabelFrame(self.master, text="Matriz de Adjacência")
        matrix_frame.grid(row=1, columnspan=4, sticky='ew', **pad_options)

        self.matrix_text = tk.Text(matrix_frame, height=8, wrap=tk.NONE)
        matrix_scrollbar_v = tk.Scrollbar(matrix_frame, orient=tk.VERTICAL, 
                                          command=self.matrix_text.yview)
        matrix_scrollbar_h = tk.Scrollbar(matrix_frame, orient=tk.HORIZONTAL, 
                                          command=self.matrix_text.xview)
        
        self.matrix_text.configure(yscrollcommand=matrix_scrollbar_v.set,
                                   xscrollcommand=matrix_scrollbar_h.set)
        
        self.matrix_text.grid(row=0, column=0, sticky='nsew')
        matrix_scrollbar_v.grid(row=0, column=1, sticky='ns')
        matrix_scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        matrix_frame.grid_rowconfigure(0, weight=1)
        matrix_frame.grid_columnconfigure(0, weight=1)

        # Frame para métodos
        methods_frame = tk.LabelFrame(self.master, text="Métodos de Otimização")
        methods_frame.grid(row=2, columnspan=4, sticky='ew', **pad_options)

        methods = ["Subida de Encosta", "Subida de Encosta Alterada", "Têmpera Simulada"]
        self.method_var = tk.StringVar(value=methods[0])

        self.method_menu = tk.OptionMenu(methods_frame, self.method_var, *methods)
        self.method_menu.grid(row=0, column=0, sticky='ew', **pad_options)
        self.method_menu.configure(state=tk.DISABLED)

        self.execute_btn = tk.Button(methods_frame, text="Executar Método",
                                     command=self.execute_method, state=tk.DISABLED,
                                     bg='lightgreen')
        self.execute_btn.grid(row=0, column=1, sticky='ew', **pad_options)

        # Parâmetros específicos
        tk.Label(methods_frame, text="Max Tentativas (Subida Alterada):").grid(
            row=0, column=2, sticky='e', **pad_options)
        
        self.max_attempts = tk.StringVar(value="100")
        tk.Entry(methods_frame, textvariable=self.max_attempts, width=10).grid(
            row=0, column=3, sticky='w', **pad_options)

        methods_frame.grid_columnconfigure(1, weight=1)

        # Frame para resultados
        results_frame = tk.LabelFrame(self.master, text="Resultados")
        results_frame.grid(row=3, columnspan=4, sticky='nsew', **pad_options)

        self.results_text = tk.Text(results_frame, wrap=tk.WORD)
        results_scrollbar = tk.Scrollbar(results_frame, command=self.results_text.yview)
        
        self.results_text.grid(row=0, column=0, sticky='nsew')
        results_scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_text.config(yscrollcommand=results_scrollbar.set)

        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

    def gerarProblema(self):
        try:
            size = int(self.problem_size.get() or 5)
            if size < 3:
                size = 3
            elif size > 20:
                size = 20
        except ValueError:
            size = 5

        # Gerar matriz de distâncias simétrica
        self.distance_matrix = [[0 for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(i + 1, size):
                distance = random.randint(10, 100)
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance

        # Solução inicial aleatória
        self.solution = list(range(size))
        random.shuffle(self.solution)
        
        self.current_distance = self.calculate_total_distance(self.solution)

        # Exibir matriz
        self.display_matrix()

        # Exibir informações do problema
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "PROBLEMA GERADO COM SUCESSO!\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Número de cidades: {size}\n")
        self.results_text.insert(tk.END, f"Solução inicial: {self.format_route(self.solution)}\n")
        self.results_text.insert(tk.END, f"Distância inicial: {self.current_distance}\n\n")

        # Habilitar controles
        self.method_menu.configure(state=tk.NORMAL)
        self.execute_btn.configure(state=tk.NORMAL)

    def display_matrix(self):
        self.matrix_text.delete(1.0, tk.END)
        size = len(self.distance_matrix)
        
        # Cabeçalho
        header = "     "
        for j in range(size):
            header += f"{j:6d}"
        self.matrix_text.insert(tk.END, header + "\n")
        
        # Linhas da matriz
        for i in range(size):
            line = f"{i:3d}: "
            for j in range(size):
                if i == j:
                    line += f"{'--':>6}"
                else:
                    line += f"{self.distance_matrix[i][j]:6d}"
            self.matrix_text.insert(tk.END, line + "\n")

    def calculate_total_distance(self, route):
        total = 0
        size = len(route)
        for i in range(size):
            total += self.distance_matrix[route[i]][route[(i + 1) % size]]
        return total

    def format_route(self, route):
        return " -> ".join(map(str, route)) + f" -> {route[0]}"

    def get_neighbors(self, route):
        """Gera vizinhos usando troca de 2 cidades (2-opt)"""
        neighbors = []
        n = len(route)
        
        for i in range(n):
            for j in range(i + 2, n):
                if j == n - 1 and i == 0:
                    continue  # Evita trocar primeiro com último
                
                neighbor = route.copy()
                # Inverter segmento entre i+1 e j
                neighbor[i+1:j+1] = reversed(neighbor[i+1:j+1])
                neighbors.append(neighbor)
        
        return neighbors

    def execute_method(self):
        if not self.distance_matrix:
            messagebox.showwarning("Aviso", "Gere um problema primeiro!")
            return

        method = self.method_var.get()
        
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, f"EXECUTANDO: {method.upper()}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        if method == "Subida de Encosta":
            self.hill_climbing()
        elif method == "Subida de Encosta Alterada":
            self.hill_climbing_modified()
        elif method == "Têmpera Simulada":
            self.simulated_annealing()

    def hill_climbing(self):
        current_solution = self.solution.copy()
        current_distance = self.calculate_total_distance(current_solution)
        iteration = 0
        
        self.results_text.insert(tk.END, f"Solução inicial: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância inicial: {current_distance}\n\n")
        
        while True:
            iteration += 1
            neighbors = self.get_neighbors(current_solution)
            best_neighbor = None
            best_distance = current_distance
            
            # Encontrar melhor vizinho
            for neighbor in neighbors:
                distance = self.calculate_total_distance(neighbor)
                if distance < best_distance:
                    best_neighbor = neighbor
                    best_distance = distance
            
            # Se não há melhoria, parar
            if best_neighbor is None:
                break
            
            current_solution = best_neighbor
            current_distance = best_distance
            
            self.results_text.insert(tk.END, f"Iteração {iteration}: Distância = {current_distance}\n")
            self.results_text.see(tk.END)
            self.master.update()
        
        self.results_text.insert(tk.END, f"\nSOLUÇÃO FINAL (Subida de Encosta):\n")
        self.results_text.insert(tk.END, f"Rota: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {current_distance}\n")
        self.results_text.insert(tk.END, f"Iterações: {iteration}\n")
        self.results_text.insert(tk.END, f"Melhoria: {self.current_distance - current_distance}\n\n")

    def hill_climbing_modified(self):
        try:
            max_attempts = int(self.max_attempts.get())
        except ValueError:
            max_attempts = 100
        
        current_solution = self.solution.copy()
        current_distance = self.calculate_total_distance(current_solution)
        best_solution = current_solution.copy()
        best_distance = current_distance
        
        self.results_text.insert(tk.END, f"Máximo de tentativas: {max_attempts}\n")
        self.results_text.insert(tk.END, f"Solução inicial: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância inicial: {current_distance}\n\n")
        
        for attempt in range(max_attempts):
            # Executar subida de encosta
            local_solution = current_solution.copy()
            local_distance = current_distance
            improvements = 0
            
            while True:
                neighbors = self.get_neighbors(local_solution)
                best_neighbor = None
                best_neighbor_distance = local_distance
                
                for neighbor in neighbors:
                    distance = self.calculate_total_distance(neighbor)
                    if distance < best_neighbor_distance:
                        best_neighbor = neighbor
                        best_neighbor_distance = distance
                
                if best_neighbor is None:
                    break
                
                local_solution = best_neighbor
                local_distance = best_neighbor_distance
                improvements += 1
            
            # Atualizar melhor solução global
            if local_distance < best_distance:
                best_solution = local_solution.copy()
                best_distance = local_distance
                self.results_text.insert(tk.END, f"Tentativa {attempt + 1}: Nova melhor solução! Distância = {best_distance}\n")
            
            # Reiniciar com solução aleatória
            current_solution = list(range(len(self.solution)))
            random.shuffle(current_solution)
            current_distance = self.calculate_total_distance(current_solution)
            
            if (attempt + 1) % 20 == 0:
                self.results_text.insert(tk.END, f"Progresso: {attempt + 1}/{max_attempts} tentativas\n")
                self.results_text.see(tk.END)
                self.master.update()
        
        self.results_text.insert(tk.END, f"\nSOLUÇÃO FINAL (Subida de Encosta Alterada):\n")
        self.results_text.insert(tk.END, f"Rota: {self.format_route(best_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {best_distance}\n")
        self.results_text.insert(tk.END, f"Tentativas: {max_attempts}\n")
        self.results_text.insert(tk.END, f"Melhoria: {self.current_distance - best_distance}\n\n")

    def simulated_annealing(self):
        current_solution = self.solution.copy()
        current_distance = self.calculate_total_distance(current_solution)
        best_solution = current_solution.copy()
        best_distance = current_distance
        
        # Parâmetros da têmpera simulada
        initial_temp = 1000
        final_temp = 1
        cooling_rate = 0.995
        max_iterations = 10000
        
        temperature = initial_temp
        iteration = 0
        
        self.results_text.insert(tk.END, f"Parâmetros da Têmpera Simulada:\n")
        self.results_text.insert(tk.END, f"Temperatura inicial: {initial_temp}\n")
        self.results_text.insert(tk.END, f"Temperatura final: {final_temp}\n")
        self.results_text.insert(tk.END, f"Taxa de resfriamento: {cooling_rate}\n")
        self.results_text.insert(tk.END, f"Max iterações: {max_iterations}\n\n")
        
        self.results_text.insert(tk.END, f"Solução inicial: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância inicial: {current_distance}\n\n")
        
        accepted_moves = 0
        
        while temperature > final_temp and iteration < max_iterations:
            iteration += 1
            
            # Gerar vizinho aleatório (troca de duas cidades)
            neighbor = current_solution.copy()
            i, j = random.sample(range(len(neighbor)), 2)
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
            
            neighbor_distance = self.calculate_total_distance(neighbor)
            delta = neighbor_distance - current_distance
            
            # Aceitar ou rejeitar o movimento
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_solution = neighbor
                current_distance = neighbor_distance
                accepted_moves += 1
                
                # Atualizar melhor solução
                if current_distance < best_distance:
                    best_solution = current_solution.copy()
                    best_distance = current_distance
            
            # Resfriar temperatura
            temperature *= cooling_rate
            
            # Log periódico
            if iteration % 1000 == 0:
                self.results_text.insert(tk.END, f"Iteração {iteration}: T={temperature:.2f}, "
                                                f"Atual={current_distance}, Melhor={best_distance}\n")
                self.results_text.see(tk.END)
                self.master.update()
        
        acceptance_rate = (accepted_moves / iteration) * 100 if iteration > 0 else 0
        
        self.results_text.insert(tk.END, f"\nSOLUÇÃO FINAL (Têmpera Simulada):\n")
        self.results_text.insert(tk.END, f"Rota: {self.format_route(best_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {best_distance}\n")
        self.results_text.insert(tk.END, f"Iterações: {iteration}\n")
        self.results_text.insert(tk.END, f"Movimentos aceitos: {accepted_moves} ({acceptance_rate:.1f}%)\n")
        self.results_text.insert(tk.END, f"Temperatura final: {temperature:.2f}\n")
        self.results_text.insert(tk.END, f"Melhoria: {self.current_distance - best_distance}\n\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()