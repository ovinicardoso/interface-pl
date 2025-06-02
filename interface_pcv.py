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
- Subida de Encosta [cite: 9]
- Subida de Encosta Alterada [cite: 26]
- Têmpera Simulada [cite: 41]

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
        self.solution = []  # A solução inicial do problema gerado
        self.current_distance = 0 # Distância da solução inicial do problema

        self.create_widgets()
        self.configure_grid()

    def configure_grid(self):
        self.master.grid_rowconfigure(3, weight=1)
        for col in range(4):
            self.master.grid_columnconfigure(col, weight=1)

    def create_widgets(self):
        pad_options = {'padx': 5, 'pady': 5}
        entry_width = 15

        config_frame = tk.LabelFrame(
            self.master, text="Configuração do Problema")
        config_frame.grid(row=0, columnspan=4, sticky='ew', **pad_options)

        tk.Label(config_frame, text="Tamanho do Problema (N cidades):").grid(
            row=0, column=0, sticky='e', **pad_options)

        tk.Entry(config_frame, textvariable=self.problem_size,
                 width=entry_width).grid(row=0, column=1, sticky='ew', **pad_options)

        tk.Button(config_frame, text="Usar Padrão (5)",
                  command=lambda: self.problem_size.set("5")).grid(
            row=0, column=2, sticky='w', **pad_options)

        tk.Button(config_frame, text="Gerar Problema",
                  command=self.gerarProblema, bg='lightblue').grid(
            row=0, column=3, sticky='ew', **pad_options)

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

        methods_frame = tk.LabelFrame(
            self.master, text="Métodos de Otimização")
        methods_frame.grid(row=2, columnspan=4, sticky='ew', **pad_options)

        methods = ["Subida de Encosta",
                   "Subida de Encosta Alterada", "Têmpera Simulada"]
        self.method_var = tk.StringVar(value=methods[0])

        self.method_menu = tk.OptionMenu(
            methods_frame, self.method_var, *methods)
        self.method_menu.grid(row=0, column=0, sticky='ew', **pad_options)
        self.method_menu.configure(state=tk.DISABLED)

        self.execute_btn = tk.Button(methods_frame, text="Executar Método",
                                     command=self.execute_method, state=tk.DISABLED,
                                     bg='lightgreen')
        self.execute_btn.grid(row=0, column=1, sticky='ew', **pad_options)

        tk.Label(methods_frame, text="Max Tentativas Sem Melhoria (t_max):").grid(
            row=0, column=2, sticky='e', **pad_options)

        self.max_attempts_var = tk.StringVar(value="100") # Default t_max para Subida de Encosta Alterada
        tk.Entry(methods_frame, textvariable=self.max_attempts_var, width=10).grid(
            row=0, column=3, sticky='w', **pad_options)

        methods_frame.grid_columnconfigure(1, weight=1)

        results_frame = tk.LabelFrame(self.master, text="Resultados")
        results_frame.grid(row=3, columnspan=4, sticky='nsew', **pad_options)

        self.results_text = tk.Text(results_frame, wrap=tk.WORD)
        results_scrollbar = tk.Scrollbar(
            results_frame, command=self.results_text.yview)

        self.results_text.grid(row=0, column=0, sticky='nsew')
        results_scrollbar.grid(row=0, column=1, sticky='ns')
        self.results_text.config(yscrollcommand=results_scrollbar.set)

        results_frame.grid_rowconfigure(0, weight=1)
        results_frame.grid_columnconfigure(0, weight=1)

    def gerarProblema(self):
        """
        Gera uma nova matriz de distâncias aleatórias para o problema do PCV e uma solução inicial.
        """
        try:
            size = int(self.problem_size.get() or 5)
            if size < 3:
                size = 3
            elif size > 20: # Limite para demonstração
                messagebox.showinfo(
                    "Aviso", "Tamanho do problema limitado a 20 para esta demonstração.")
                size = 20
            self.problem_size.set(str(size))
        except ValueError:
            size = 5
            self.problem_size.set("5")

        self.distance_matrix = [[0 for _ in range(size)] for _ in range(size)]

        # Preenche a matriz de adjacência com distâncias aleatórias simétricas
        for i in range(size):
            for j in range(i + 1, size):
                distance = random.randint(10, 100) # Distâncias entre 10 e 100
                self.distance_matrix[i][j] = distance
                self.distance_matrix[j][i] = distance # Garante simetria

        # Gera uma solução inicial aleatória
        self.solution = list(range(size))
        random.shuffle(self.solution)
        self.current_distance = self.calculate_total_distance(self.solution)

        self.display_matrix() # Exibe a matriz na interface

        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "PROBLEMA GERADO COM SUCESSO!\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Número de cidades (N): {size}\n")
        self.results_text.insert(
            tk.END, f"Solução inicial gerada: {self.format_route(self.solution)}\n")
        self.results_text.insert(
            tk.END, f"Distância inicial da solução gerada: {self.current_distance}\n\n")

        self.method_menu.configure(state=tk.NORMAL)
        self.execute_btn.configure(state=tk.NORMAL)

    def display_matrix(self):
        """Exibe a matriz de adjacência no campo de texto."""
        self.matrix_text.delete(1.0, tk.END)
        size = len(self.distance_matrix)

        # Formata o cabeçalho da matriz
        header = "     "
        for j in range(size):
            header += f"{j:6d}" # Colunas com 6 espaços
        self.matrix_text.insert(tk.END, header + "\n")
        header_sep = "-----+" + "------"*size
        self.matrix_text.insert(tk.END, header_sep + "\n")

        # Insere os dados da matriz
        for i in range(size):
            line = f"{i:3d} |" # Linha com 3 espaços para o índice
            for j in range(size):
                if i == j:
                    line += f"{'--':>6}" # "--" para a diagonal
                else:
                    line += f"{self.distance_matrix[i][j]:6d}" # Distância com 6 espaços
            self.matrix_text.insert(tk.END, line + "\n")

    def calculate_total_distance(self, route):
        """Calcula a distância total de uma rota no PCV."""
        total = 0
        size = len(route)
        for i in range(size):
            # Soma a distância entre a cidade atual e a próxima na rota
            # O operador '%' garante que a última cidade volta para a primeira
            total += self.distance_matrix[route[i]][route[(i + 1) % size]]
        return total

    def format_route(self, route):
        """Formata uma rota para exibição, incluindo o retorno à cidade inicial."""
        if not route:
            return "N/A"
        return " -> ".join(map(str, route)) + f" -> {route[0]}"

    def generate_neighbors_one_city_swap(self, route):
        """
        Gera vizinhos trocando uma cidade escolhida aleatoriamente com todas as outras.
        Esta é a função sucessora para Subida de Encosta e Subida de Encosta Alterada,
        conforme descrito nos slides[cite: 20].
        """
        n = len(route)
        if n <= 1:
            return -1, []  # Retorna índice inválido e lista vazia
        
        # Escolhe uma cidade aleatória para ser o pivô da troca [cite: 20]
        i = random.randint(0, n-1)
        neighbors = []
        for j in range(n):
            if j == i: # Não troca a cidade com ela mesma
                continue
            neighbor = route.copy()
            neighbor[i], neighbor[j] = neighbor[j], neighbor[i]  # Realiza a troca
            neighbors.append(neighbor)
        return i, neighbors # Retorna o índice da cidade pivot e a lista de vizinhos gerados

    def generate_neighbors_random_swap(self, route):
        """
        Gera um único vizinho trocando duas cidades aleatórias.
        Esta é a função sucessora para Têmpera Simulada[cite: 49].
        """
        if len(route) < 2:
            return route.copy()
        
        neighbor = route.copy()
        # Seleciona duas posições aleatórias distintas para troca
        i, j = random.sample(range(len(neighbor)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

    def execute_method(self):
        """Executa o método de otimização selecionado."""
        if not self.distance_matrix:
            messagebox.showwarning("Aviso", "Gere um problema primeiro!")
            return

        method = self.method_var.get()

        # Limpa e insere cabeçalho para os resultados do método
        self.results_text.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.results_text.insert(tk.END, f"EXECUTANDO: {method.upper()}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        # Chama o método de otimização apropriado
        if method == "Subida de Encosta":
            self.hill_climbing()
        elif method == "Subida de Encosta Alterada":
            self.hill_climbing_modified()
        elif method == "Têmpera Simulada":
            self.simulated_annealing()

    def hill_climbing(self):
        """
        Implementa o algoritmo de Subida de Encosta (Hill Climbing).
        Busca o melhor vizinho e move-se para ele se for melhor; para se não houver melhoria[cite: 16].
        """
        # A solução inicial para esta execução do algoritmo é uma cópia da solução gerada
        current_solution = self.solution[:]
        current_distance = self.calculate_total_distance(current_solution)
        iteration = 0

        self.results_text.insert(
            tk.END, f"Solução inicial (para esta execução de HC): {self.format_route(current_solution)}\n")
        self.results_text.insert(
            tk.END, f"Distância inicial (para esta execução de HC): {current_distance}\n\n")

        while True:
            iteration += 1
            # Gera vizinhos trocando uma cidade aleatória com as demais [cite: 20]
            i_pivot, neighbors = self.generate_neighbors_one_city_swap(current_solution)
            
            best_neighbor = None
            best_distance = current_distance # Inicializa com a distância da solução atual
            
            # Itera sobre os vizinhos para encontrar o melhor
            for neighbor in neighbors:
                distance = self.calculate_total_distance(neighbor)
                if distance < best_distance: # Se encontrar um vizinho melhor
                    best_neighbor = neighbor
                    best_distance = distance
            
            if best_neighbor is None:
                # Se nenhum vizinho melhor foi encontrado, atingiu um ótimo local [cite: 16]
                self.results_text.insert(
                    tk.END, f"Iteração {iteration}: Nenhum vizinho melhor encontrado. Ótimo local atingido.\n")
                break # Sai do loop
                
            # Move para o melhor vizinho encontrado
            current_solution = best_neighbor
            current_distance = best_distance

            self.results_text.insert(
                tk.END, f"Iteração {iteration}: Nova solução encontrada. Distância = {current_distance}\n")
            self.results_text.see(tk.END) # Garante que o texto seja visível
            self.master.update() # Atualiza a interface

        self.results_text.insert(
            tk.END, f"\nSOLUÇÃO FINAL (Subida de Encosta):\n")
        self.results_text.insert(
            tk.END, f"Rota: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {current_distance}\n")
        self.results_text.insert(tk.END, f"Iterações totais: {iteration}\n")
        # Calcula a melhoria em relação à solução inicial do PROBLEMA
        self.results_text.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema: {self.current_distance - current_distance}\n\n")

    def hill_climbing_modified(self):
        """
        Implementa o algoritmo de Subida de Encosta Alterada.
        Permite um número máximo de passos (t_max) sem melhoria antes de parar[cite: 26].
        """
        try:
            t_max = int(self.max_attempts_var.get())
        except ValueError:
            t_max = 100 # Valor padrão se a entrada for inválida
        
        current_solution = self.solution[:]
        current_distance = self.calculate_total_distance(current_solution)
        t = 0  # Contador de tentativas sem melhoria [cite: 26]
        iteration = 0

        self.results_text.insert(
            tk.END, f"Máximo de passos sem melhoria (t_max): {t_max}\n")
        self.results_text.insert(
            tk.END, f"Solução inicial (para esta execução de HC Alterada): {self.format_route(current_solution)}\n")
        self.results_text.insert(
            tk.END, f"Distância inicial (para esta execução de HC Alterada): {current_distance}\n\n")

        while True:
            iteration += 1
            # Gera vizinhos conforme a função sucessora [cite: 30]
            i_pivot, neighbors = self.generate_neighbors_one_city_swap(current_solution)
            
            best_neighbor = None
            best_distance = float('inf') # Inicializa com infinito para encontrar o menor vizinho
            
            # Encontra o melhor vizinho (mesmo que seja pior que o atual)
            for neighbor in neighbors:
                distance = self.calculate_total_distance(neighbor)
                if distance < best_distance:
                    best_neighbor = neighbor
                    best_distance = distance
            
            self.results_text.insert(
                tk.END, f"Iteração {iteration}: Melhor vizinho encontrado tem distância {best_distance} (Atual: {current_distance}). ")

            if best_distance < current_distance:
                # Melhoria encontrada: move para o vizinho e reseta o contador 't' [cite: 26]
                current_solution = best_neighbor
                current_distance = best_distance
                t = 0
                self.results_text.insert(
                    tk.END, f"Melhoria encontrada! Nova distância: {current_distance}. Contador 't' resetado para 0.\n")
            else:
                # Sem melhoria: incrementa o contador 't' [cite: 26]
                t += 1
                self.results_text.insert(
                    tk.END, f"Sem melhoria. Contador 't' incrementado para {t}.\n")
                if t > t_max:
                    # Limite de 't_max' atingido, para o algoritmo [cite: 26]
                    self.results_text.insert(
                        tk.END, f"  Limite de t_max ({t_max}) passos sem melhoria atingido. Parando.\n")
                    break

            self.results_text.see(tk.END)
            self.master.update()

        self.results_text.insert(
            tk.END, f"\nSOLUÇÃO FINAL (Subida de Encosta Alterada):\n")
        self.results_text.insert(
            tk.END, f"Rota: {self.format_route(current_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {current_distance}\n")
        self.results_text.insert(tk.END, f"Iterações totais: {iteration}\n")
        self.results_text.insert(
            tk.END, f"Passos sem melhoria no final (t): {t}\n")
        self.results_text.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema: {self.current_distance - current_distance}\n\n")

    def simulated_annealing(self):
        """
        Implementa o algoritmo de Têmpera Simulada (Simulated Annealing).
        Combina busca local com movimentos aleatórios para escapar de mínimos locais[cite: 41, 43].
        """
        current_solution = self.solution[:]
        current_distance = self.calculate_total_distance(current_solution)

        best_solution = current_solution[:] # Mantém a melhor solução global encontrada
        best_distance = current_distance

        # Parâmetros de Têmpera Simulada. Ajuste conforme necessidade [cite: 43]
        initial_temp = 1000.0
        final_temp = 1.0
        cooling_rate = 0.995 # Fator de redução da temperatura [cite: 46]
        max_iterations = 10000 # Limite para evitar loops infinitos ou muito longos

        temperature = initial_temp
        iteration = 0
        accepted_moves = 0 # Contador de movimentos aceitos (incluindo piores)

        self.results_text.insert(tk.END, f"Parâmetros da Têmpera Simulada:\n")
        self.results_text.insert(
            tk.END, f"Temperatura inicial: {initial_temp:.2f}\n")
        self.results_text.insert(
            tk.END, f"Temperatura final (critério de parada aprox.): {final_temp:.2f}\n")
        self.results_text.insert(
            tk.END, f"Taxa de resfriamento (cooling_rate): {cooling_rate}\n")
        self.results_text.insert(
            tk.END, f"Máximo de iterações: {max_iterations}\n\n")

        self.results_text.insert(
            tk.END, f"Solução inicial (para esta execução de TS): {self.format_route(current_solution)}\n")
        self.results_text.insert(
            tk.END, f"Distância inicial (para esta execução de TS): {current_distance}\n\n")

        # Loop principal do algoritmo: enquanto a temperatura não atinge o mínimo e não excedeu as iterações
        while temperature > final_temp and iteration < max_iterations:
            iteration += 1

            # Gera um vizinho aleatório (trocando duas cidades) [cite: 49]
            neighbor = self.generate_neighbors_random_swap(current_solution)
            neighbor_distance = self.calculate_total_distance(neighbor)

            delta_energy = neighbor_distance - current_distance # Custo do novo estado - Custo do estado atual

            # Condição de aceitação:
            if delta_energy < 0: # Se o vizinho é melhor
                current_solution = neighbor
                current_distance = neighbor_distance
                accepted_moves += 1
                if current_distance < best_distance: # Atualiza a melhor solução global se for o caso
                    best_solution = current_solution[:]
                    best_distance = current_distance
            else: # Se o vizinho é pior (delta_energy >= 0)
                # Calcula a probabilidade de aceitar um movimento pior [cite: 45]
                if temperature > 1e-9: # Evita divisão por zero ou números muito pequenos
                    acceptance_probability = math.exp(-delta_energy / temperature)
                    if random.random() < acceptance_probability:
                        current_solution = neighbor
                        current_distance = neighbor_distance
                        accepted_moves += 1

            temperature *= cooling_rate # Resfria a temperatura [cite: 46]

            # Feedback periódico na interface
            if iteration % 500 == 0 or iteration == 1: # Mostra a cada 500 iterações e na primeira
                self.results_text.insert(tk.END, f"Iter {iteration}: Temp={temperature:.2f}, "
                                         f"AtualDist={current_distance}, MelhorDistEncontrada={best_distance}\n")
                self.results_text.see(tk.END)
                self.master.update()

        # Calcula a taxa de aceitação de movimentos
        acceptance_rate = (accepted_moves / iteration) * 100 if iteration > 0 else 0

        self.results_text.insert(
            tk.END, f"\nSOLUÇÃO FINAL (Têmpera Simulada):\n")
        self.results_text.insert(
            tk.END, f"Rota: {self.format_route(best_solution)}\n")
        self.results_text.insert(tk.END, f"Distância: {best_distance}\n")
        self.results_text.insert(tk.END, f"Iterações totais: {iteration}\n")
        self.results_text.insert(
            tk.END, f"Movimentos aceitos (incl. piores): {accepted_moves} ({acceptance_rate:.1f}%)\n")
        self.results_text.insert(
            tk.END, f"Temperatura final atingida: {temperature:.2f}\n")
        self.results_text.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema: {self.current_distance - best_distance}\n\n")


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()