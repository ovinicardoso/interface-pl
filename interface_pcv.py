import tkinter as tk
from tkinter import messagebox, ttk
import random
import math
import copy


class AplicacaoPrincipal:
    def __init__(self, mestre):
        self.mestre = mestre
        self.mestre.title("Otimização de Rotas - PCV")
        self.mestre.geometry("500x300")
        self.mestre.minsize(400, 200)

        self.configurar_grade()
        self.criar_widgets()

    def configurar_grade(self):
        self.mestre.grid_rowconfigure(0, weight=1)
        self.mestre.grid_columnconfigure(0, weight=1)

    def criar_widgets(self):
        frame_principal = tk.Frame(self.mestre)
        frame_principal.grid(row=0, column=0, sticky='nsew')

        frame_principal.grid_rowconfigure(3, weight=1)
        frame_principal.grid_columnconfigure(0, weight=1)

        opcoes_preenchimento = {'padx': 10, 'pady': 10}
        estilo_botao = {
            'width': 20,
            'height': 2
        }

        tk.Button(frame_principal, text="Métodos Básicos",
                  command=self.abrir_janela_metodos_basicos, **estilo_botao).grid(
            row=0, column=0, **opcoes_preenchimento)

        tk.Button(frame_principal, text="Algoritmos Genéticos",
                  state=tk.DISABLED, **estilo_botao).grid(
            row=1, column=0, **opcoes_preenchimento)

        tk.Button(frame_principal, text="Sobre o Sistema",
                  command=self.mostrar_sobre, **estilo_botao).grid(
            row=2, column=0, **opcoes_preenchimento)

    def abrir_janela_metodos_basicos(self):
        JanelaMetodosBasicos(tk.Toplevel(self.mestre))

    def mostrar_sobre(self):
        texto_sobre = """Aplicação do Problema do Caixeiro Viajante (PCV) na área de Logística e Transporte para a roteirização de entregas.

Algoritmos implementados:
- Subida de Encosta
- Subida de Encosta Alterada
- Têmpera Simulada

Desenvolvido por:
- Izaque Nogueira e Vinicius Cardoso"""
        messagebox.showinfo("Sobre o Sistema", texto_sobre)


class JanelaMetodosBasicos:
    def __init__(self, mestre):
        self.mestre = mestre
        self.mestre.title("Métodos de Otimização - PCV")
        self.mestre.geometry("900x700")
        self.mestre.minsize(800, 600)

        self.tamanho_problema = tk.StringVar()
        self.matriz_distancia = []
        self.solucao_inicial = []
        self.distancia_inicial = 0

        self.criar_widgets()
        self.configurar_grade()
        
        self.exibir_parametros_metodo()


    def configurar_grade(self):
        self.mestre.grid_rowconfigure(3, weight=1)
        for col in range(4):
            self.mestre.grid_columnconfigure(col, weight=1)

    def criar_widgets(self):
        opcoes_preenchimento = {'padx': 5, 'pady': 5}
        largura_entrada = 15

        frame_config = tk.LabelFrame(
            self.mestre, text="Configuração do Problema")
        frame_config.grid(row=0, columnspan=4, sticky='ew', **opcoes_preenchimento)

        tk.Label(frame_config, text="Tamanho do Problema (N cidades):").grid(
            row=0, column=0, sticky='e', **opcoes_preenchimento)

        tk.Entry(frame_config, textvariable=self.tamanho_problema,
                 width=largura_entrada).grid(row=0, column=1, sticky='ew', **opcoes_preenchimento)

        tk.Button(frame_config, text="Usar Padrão (5)",
                  command=lambda: self.tamanho_problema.set("5")).grid(
            row=0, column=2, sticky='w', **opcoes_preenchimento)

        tk.Button(frame_config, text="Gerar Problema",
                  command=self.gerar_problema, bg='lightblue').grid(
            row=0, column=3, sticky='ew', **opcoes_preenchimento)

        frame_matriz = tk.LabelFrame(self.mestre, text="Matriz de Adjacência")
        frame_matriz.grid(row=1, columnspan=4, sticky='ew', **opcoes_preenchimento)

        self.texto_matriz = tk.Text(frame_matriz, height=8, wrap=tk.NONE)
        barra_rolagem_matriz_v = tk.Scrollbar(frame_matriz, orient=tk.VERTICAL,
                                          command=self.texto_matriz.yview)
        barra_rolagem_matriz_h = tk.Scrollbar(frame_matriz, orient=tk.HORIZONTAL,
                                          command=self.texto_matriz.xview)

        self.texto_matriz.configure(yscrollcommand=barra_rolagem_matriz_v.set,
                                   xscrollcommand=barra_rolagem_matriz_h.set)

        self.texto_matriz.grid(row=0, column=0, sticky='nsew')
        barra_rolagem_matriz_v.grid(row=0, column=1, sticky='ns')
        barra_rolagem_matriz_h.grid(row=1, column=0, sticky='ew')

        frame_matriz.grid_rowconfigure(0, weight=1)
        frame_matriz.grid_columnconfigure(0, weight=1)

        frame_metodos = tk.LabelFrame(
            self.mestre, text="Métodos de Otimização")
        frame_metodos.grid(row=2, columnspan=4, sticky='ew', **opcoes_preenchimento)

        metodos = ["Subida de Encosta",
                   "Subida de Encosta Alterada", "Têmpera Simulada", "Todos"]
        self.variavel_metodo = tk.StringVar(value=metodos[0])
        self.variavel_metodo.trace_add("write", lambda *args: self.exibir_parametros_metodo())

        self.menu_metodo = tk.OptionMenu(
            frame_metodos, self.variavel_metodo, *metodos)
        self.menu_metodo.grid(row=0, column=0, sticky='ew', **opcoes_preenchimento)
        self.menu_metodo.configure(state=tk.DISABLED)

        self.botao_executar = tk.Button(frame_metodos, text="Executar Método",
                                     command=self.executar_metodo, state=tk.DISABLED,
                                     bg='lightgreen')
        self.botao_executar.grid(row=0, column=1, sticky='ew', **opcoes_preenchimento)

        frame_metodos.grid_columnconfigure(1, weight=1)

        self.frame_parametros_hc_mod = tk.Frame(frame_metodos)
        tk.Label(self.frame_parametros_hc_mod, text="Max Tentativas Sem Melhoria (t_max):").grid(
            row=0, column=0, sticky='e', **opcoes_preenchimento)
        self.var_max_tentativas = tk.StringVar(value="100")
        tk.Entry(self.frame_parametros_hc_mod, textvariable=self.var_max_tentativas, width=10).grid(
            row=0, column=1, sticky='w', **opcoes_preenchimento)
        
        self.frame_parametros_ts = tk.Frame(frame_metodos)
        tk.Label(self.frame_parametros_ts, text="Temp. Inicial (Ti):").grid(
            row=0, column=0, sticky='e', **opcoes_preenchimento)
        self.var_temp_inicial = tk.StringVar(value="1000.0")
        tk.Entry(self.frame_parametros_ts, textvariable=self.var_temp_inicial, width=10).grid(
            row=0, column=1, sticky='w', **opcoes_preenchimento)

        tk.Label(self.frame_parametros_ts, text="Temp. Final (Tf):").grid(
            row=1, column=0, sticky='e', **opcoes_preenchimento)
        self.var_temp_final = tk.StringVar(value="1.0")
        tk.Entry(self.frame_parametros_ts, textvariable=self.var_temp_final, width=10).grid(
            row=1, column=1, sticky='w', **opcoes_preenchimento)

        tk.Label(self.frame_parametros_ts, text="Taxa Resfriamento (Fr):").grid(
            row=2, column=0, sticky='e', **opcoes_preenchimento)
        self.var_taxa_resfriamento = tk.StringVar(value="0.995")
        tk.Entry(self.frame_parametros_ts, textvariable=self.var_taxa_resfriamento, width=10).grid(
            row=2, column=1, sticky='w', **opcoes_preenchimento)


        frame_resultados = tk.LabelFrame(self.mestre, text="Resultados")
        frame_resultados.grid(row=3, columnspan=4, sticky='nsew', **opcoes_preenchimento)

        self.texto_resultados = tk.Text(frame_resultados, wrap=tk.WORD)
        barra_rolagem_resultados = tk.Scrollbar(
            frame_resultados, command=self.texto_resultados.yview)

        self.texto_resultados.grid(row=0, column=0, sticky='nsew')
        barra_rolagem_resultados.grid(row=0, column=1, sticky='ns')
        self.texto_resultados.config(yscrollcommand=barra_rolagem_resultados.set)
        
        tk.Button(frame_resultados, text="Limpar Resultados",
                  command=self.limpar_resultados, bg='lightcoral').grid(
            row=1, column=0, columnspan=2, sticky='ew', **opcoes_preenchimento)

        frame_resultados.grid_rowconfigure(0, weight=1)
        frame_resultados.grid_columnconfigure(0, weight=1)

    def exibir_parametros_metodo(self):
        self.frame_parametros_hc_mod.grid_forget()
        self.frame_parametros_ts.grid_forget()

        metodo_selecionado = self.variavel_metodo.get()

        if metodo_selecionado == "Subida de Encosta Alterada":
            self.frame_parametros_hc_mod.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
        elif metodo_selecionado == "Têmpera Simulada":
            self.frame_parametros_ts.grid(row=1, column=0, columnspan=4, sticky='ew', padx=5, pady=5)
        elif metodo_selecionado == "Todos":
            self.frame_parametros_hc_mod.grid(row=1, column=0, columnspan=2, sticky='ew', padx=5, pady=5)
            self.frame_parametros_ts.grid(row=2, column=0, columnspan=4, sticky='ew', padx=5, pady=5)


    def limpar_resultados(self):
        self.texto_resultados.delete(1.0, tk.END)

    def gerar_problema(self):
        try:
            tamanho = int(self.tamanho_problema.get() or 5)
            if tamanho < 3:
                tamanho = 3
            elif tamanho > 20:
                messagebox.showinfo(
                    "Aviso", "Tamanho do problema limitado a 20 para esta demonstração.")
                tamanho = 20
            self.tamanho_problema.set(str(tamanho))
        except ValueError:
            tamanho = 5
            self.tamanho_problema.set("5")

        self.matriz_distancia = [[0 for _ in range(tamanho)] for _ in range(tamanho)]

        for i in range(tamanho):
            for j in range(i + 1, tamanho):
                distancia = random.randint(10, 100)
                self.matriz_distancia[i][j] = distancia
                self.matriz_distancia[j][i] = distancia

        self.solucao_inicial = list(range(tamanho))
        random.shuffle(self.solucao_inicial)
        self.distancia_inicial = self.calcular_distancia_total(self.solucao_inicial)

        self.exibir_matriz()

        self.texto_resultados.delete(1.0, tk.END)
        self.texto_resultados.insert(tk.END, "=" * 50 + "\n")
        self.texto_resultados.insert(tk.END, "PROBLEMA GERADO COM SUCESSO!\n")
        self.texto_resultados.insert(tk.END, "=" * 50 + "\n\n")
        self.texto_resultados.insert(tk.END, f"Número de cidades (N): {tamanho}\n")
        self.texto_resultados.insert(
            tk.END, f"Solução inicial gerada: {self.formatar_rota(self.solucao_inicial)}\n")
        self.texto_resultados.insert(
            tk.END, f"Distância inicial da solução gerada: {self.distancia_inicial}\n\n")

        self.menu_metodo.configure(state=tk.NORMAL)
        self.botao_executar.configure(state=tk.NORMAL)

    def exibir_matriz(self):
        self.texto_matriz.delete(1.0, tk.END)
        tamanho = len(self.matriz_distancia)

        cabecalho = "     "
        for j in range(tamanho):
            cabecalho += f"{j:6d}"
        self.texto_matriz.insert(tk.END, cabecalho + "\n")
        separador_cabecalho = "-----+" + "------"*tamanho
        self.texto_matriz.insert(tk.END, separador_cabecalho + "\n")

        for i in range(tamanho):
            linha = f"{i:3d} |"
            for j in range(tamanho):
                if i == j:
                    linha += f"{'--':>6}"
                else:
                    linha += f"{self.matriz_distancia[i][j]:6d}"
            self.texto_matriz.insert(tk.END, linha + "\n")

    def calcular_distancia_total(self, rota):
        total = 0
        tamanho = len(rota)
        for i in range(tamanho):
            total += self.matriz_distancia[rota[i]][rota[(i + 1) % tamanho]]
        return total

    def formatar_rota(self, rota):
        if not rota:
            return "N/A"
        return " -> ".join(map(str, rota)) + f" -> {rota[0]}"

    def gerar_vizinho_troca_uma_cidade(self, rota):
        n = len(rota)
        if n <= 1:
            return -1, []
        
        i = random.randint(0, n-1)
        vizinhos = []
        for j in range(n):
            if j == i:
                continue
            vizinho = rota.copy()
            vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
            vizinhos.append(vizinho)
        return i, vizinhos

    def gerar_vizinho_troca_aleatoria(self, rota):
        if len(rota) < 2:
            return rota.copy()
        
        vizinho = rota.copy()
        i, j = random.sample(range(len(vizinho)), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
        return vizinho

    def executar_metodo(self):
        if not self.matriz_distancia:
            messagebox.showwarning("Aviso", "Gere um problema primeiro!")
            return

        metodo = self.variavel_metodo.get()

        self.texto_resultados.insert(tk.END, "\n" + "=" * 50 + "\n")
        self.texto_resultados.insert(tk.END, f"EXECUTANDO: {metodo.upper()}\n")
        self.texto_resultados.insert(tk.END, "=" * 50 + "\n\n")

        if metodo == "Subida de Encosta":
            self.subida_encosta()
        elif metodo == "Subida de Encosta Alterada":
            self.subida_encosta_alterada()
        elif metodo == "Têmpera Simulada":
            self.tempera_simulada()
        elif metodo == "Todos":
            self.executar_todos_metodos()

    def subida_encosta(self):
        solucao_atual = self.solucao_inicial[:]
        distancia_atual = self.calcular_distancia_total(solucao_atual)
        iteracao = 0

        self.texto_resultados.insert(
            tk.END, f"Solução inicial (para esta execução de Subida de Encosta): {self.formatar_rota(solucao_atual)}\n")
        self.texto_resultados.insert(
            tk.END, f"Distância inicial (para esta execução de Subida de Encosta): {distancia_atual}\n\n")

        while True:
            iteracao += 1
            self.texto_resultados.insert(tk.END, f"Iteração {iteracao}:\n")
            self.texto_resultados.insert(tk.END, f"  Solução Atual: {self.formatar_rota(solucao_atual)}\n")
            self.texto_resultados.insert(tk.END, f"  Distância Atual: {distancia_atual}\n")
            
            indice_pivo, vizinhos = self.gerar_vizinho_troca_uma_cidade(solucao_atual)
            
            melhor_vizinho_encontrado_na_iteracao = None
            melhor_distancia_na_iteracao = distancia_atual
            
            for vizinho in vizinhos:
                distancia = self.calcular_distancia_total(vizinho)
                if distancia < melhor_distancia_na_iteracao:
                    melhor_vizinho_encontrado_na_iteracao = vizinho
                    melhor_distancia_na_iteracao = distancia
            
            if melhor_vizinho_encontrado_na_iteracao is None:
                self.texto_resultados.insert(
                    tk.END, f"  Resultado: Nenhum vizinho melhor encontrado. Ótimo local atingido.\n")
                self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
                break
                
            solucao_atual = melhor_vizinho_encontrado_na_iteracao
            distancia_atual = melhor_distancia_na_iteracao

            self.texto_resultados.insert(
                tk.END, f"  Resultado: Melhoria encontrada! Nova distância: {distancia_atual}\n")
            self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
            self.texto_resultados.see(tk.END)
            self.mestre.update()

        self.texto_resultados.insert(
            tk.END, f"\nSOLUÇÃO FINAL (Subida de Encosta):\n")
        self.texto_resultados.insert(
            tk.END, f"Rota: {self.formatar_rota(solucao_atual)}\n")
        self.texto_resultados.insert(tk.END, f"Distância: {distancia_atual}\n")
        self.texto_resultados.insert(tk.END, f"Iterações totais: {iteracao}\n")
        melhoria = self.distancia_inicial - distancia_atual
        self.texto_resultados.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema ({self.distancia_inicial}): {melhoria}\n\n")
        return distancia_atual, solucao_atual

    def subida_encosta_alterada(self):
        try:
            t_max = int(self.var_max_tentativas.get())
            if t_max <= 0:
                self.texto_resultados.insert(tk.END, "AVISO: t_max inválido, usando valor padrão 1.\n")
                t_max = 1
        except ValueError:
            self.texto_resultados.insert(tk.END, "AVISO: Erro ao ler t_max, usando valor padrão 100.\n")
            t_max = 100
        
        atual = self.solucao_inicial[:]
        va = self.calcular_distancia_total(atual)

        t = 1
        iteracao = 0

        self.texto_resultados.insert(
            tk.END, f"Executando Subida Alterada:\n")
        self.texto_resultados.insert(
            tk.END, f"Máximo de passos sem melhoria (t_max): {t_max}\n")
        self.texto_resultados.insert(
            tk.END, f"Solução inicial para o algoritmo: {self.formatar_rota(atual)}\n")
        self.texto_resultados.insert(
            tk.END, f"Distância inicial para o algoritmo (VA): {va}\n\n")

        def avalia_um_vizinho(solucao_corrente):
            novo_vizinho = self.gerar_vizinho_troca_aleatoria(solucao_corrente)
            valor_novo_vizinho = self.calcular_distancia_total(novo_vizinho)
            return novo_vizinho, valor_novo_vizinho

        while True:
            iteracao += 1
            
            self.texto_resultados.insert(tk.END, f"Iteração {iteracao}:\n")
            self.texto_resultados.insert(tk.END, f"  Contador T (etapas sem melhoria): {t} (VA atual: {va})\n")

            novo, vn = avalia_um_vizinho(atual)

            self.texto_resultados.insert(tk.END, f"  Vizinho Gerado: Distância={vn}. {self.formatar_rota(novo)}\n")

            if vn >= va:
                t += 1
                self.texto_resultados.insert(
                    tk.END, f"  Resultado: Sem melhoria ou pior (VN >= VA). T incrementado para {t}.\n")
                
                if t > t_max:
                    self.texto_resultados.insert(
                        tk.END, f"  CONDIÇÃO DE PARADA: T ({t}) > t_max ({t_max}). Algoritmo encerrado.\n")
                    self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
                    break
            else:
                atual = novo
                va = vn
                t = 1
                self.texto_resultados.insert(
                    tk.END, f"  Resultado: Melhoria encontrada (VN < VA)!\n")
                self.texto_resultados.insert(
                    tk.END, f"    Nova Solução Atual: {self.formatar_rota(atual)}\n")
                self.texto_resultados.insert(
                    tk.END, f"    Novo Valor Atual (VA): {va}\n")
                self.texto_resultados.insert(
                    tk.END, f"    Contador T resetado para 1.\n")
            
            self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
            self.texto_resultados.see(tk.END)
            self.mestre.update()

            if iteracao >= 100000 and t_max > 200:
                self.texto_resultados.insert(tk.END, f"Parada de segurança: Número máximo de iterações ({iteracao}) atingido.\n")
                break
        
        self.texto_resultados.insert(
            tk.END, f"\nSOLUÇÃO FINAL:\n")
        self.texto_resultados.insert(
            tk.END, f"Rota Final: {self.formatar_rota(atual)}\n")
        self.texto_resultados.insert(tk.END, f"Distância Final: {va}\n")
        self.texto_resultados.insert(tk.END, f"Iterações Totais: {iteracao}\n")
        self.texto_resultados.insert(
            tk.END, f"Valor final do contador T: {t}\n")
        melhoria = self.distancia_inicial - va
        self.texto_resultados.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema ({self.distancia_inicial}): {melhoria}\n\n")
        return va, atual

    def tempera_simulada(self):
        try:
            temp_inicial = float(self.var_temp_inicial.get())
            temp_final = float(self.var_temp_final.get())
            taxa_resfriamento = float(self.var_taxa_resfriamento.get())
        except ValueError:
            messagebox.showwarning("Erro de Parâmetros", "Por favor, insira valores numéricos válidos para os parâmetros da Têmpera Simulada.")
            return None, None
            
        max_iteracoes = 10000

        solucao_atual = self.solucao_inicial[:]
        distancia_atual = self.calcular_distancia_total(solucao_atual)

        melhor_solucao = solucao_atual[:]
        melhor_distancia = distancia_atual

        temperatura = temp_inicial
        iteracao = 0
        movimentos_aceitos = 0

        self.texto_resultados.insert(tk.END, f"Parâmetros da Têmpera Simulada:\n")
        self.texto_resultados.insert(
            tk.END, f"Temperatura inicial: {temp_inicial:.2f}\n")
        self.texto_resultados.insert(
            tk.END, f"Temperatura final (critério de parada aprox.): {temp_final:.2f}\n")
        self.texto_resultados.insert(
            tk.END, f"Taxa de resfriamento (cooling_rate): {taxa_resfriamento}\n")
        self.texto_resultados.insert(
            tk.END, f"Máximo de iterações: {max_iteracoes}\n\n")

        self.texto_resultados.insert(
            tk.END, f"Solução inicial (para esta execução de TS): {self.formatar_rota(solucao_atual)}\n")
        self.texto_resultados.insert(
            tk.END, f"Distância inicial (para esta execução de TS): {distancia_atual}\n\n")

        while temperatura > temp_final and iteracao < max_iteracoes:
            iteracao += 1

            self.texto_resultados.insert(tk.END, f"Iteração {iteracao}:\n")
            self.texto_resultados.insert(tk.END, f"  Temperatura Atual: {temperatura:.2f}\n")
            self.texto_resultados.insert(tk.END, f"  Solução Atual: {self.formatar_rota(solucao_atual)}\n")
            self.texto_resultados.insert(tk.END, f"  Distância Atual: {distancia_atual}\n")


            vizinho = self.gerar_vizinho_troca_aleatoria(solucao_atual)
            distancia_vizinho = self.calcular_distancia_total(vizinho)

            delta_energia = distancia_vizinho - distancia_atual
            self.texto_resultados.insert(tk.END, f"  Vizinho Gerado: Distância={distancia_vizinho}. {self.formatar_rota(vizinho)}\n")
            self.texto_resultados.insert(tk.END, f"  Delta Energia (Vizinho - Atual): {delta_energia:.2f}\n")


            if delta_energia < 0:
                solucao_atual = vizinho
                distancia_atual = distancia_vizinho
                movimentos_aceitos += 1
                if distancia_atual < melhor_distancia:
                    melhor_solucao = solucao_atual[:]
                    melhor_distancia = distancia_atual
                self.texto_resultados.insert(tk.END, f"  Resultado: Melhoria encontrada! Movimento aceito.\n")
            else:
                if temperatura > 1e-9:
                    probabilidade_aceitacao = math.exp(-delta_energia / temperatura)
                    self.texto_resultados.insert(tk.END, f"  Probabilidade de Aceitação (movimento pior): {probabilidade_aceitacao:.4f}\n")
                    if random.random() < probabilidade_aceitacao:
                        solucao_atual = vizinho
                        distancia_atual = distancia_vizinho
                        movimentos_aceitos += 1
                        self.texto_resultados.insert(tk.END, f"  Resultado: Movimento pior aceito por probabilidade.\n")
                    else:
                        self.texto_resultados.insert(tk.END, f"  Resultado: Movimento pior rejeitado.\n")
                else:
                    self.texto_resultados.insert(tk.END, f"  Resultado: Movimento pior rejeitado (temperatura muito baixa).\n")


            temperatura *= taxa_resfriamento
            self.texto_resultados.insert(tk.END, f"  Nova Temperatura: {temperatura:.2f}\n")
            self.texto_resultados.insert(tk.END, f"  Melhor Distância Encontrada até agora: {melhor_distancia}\n")
            self.texto_resultados.insert(tk.END, "-" * 40 + "\n")
            self.texto_resultados.see(tk.END)
            self.mestre.update()

        taxa_aceitacao = (movimentos_aceitos / iteracao) * 100 if iteracao > 0 else 0

        self.texto_resultados.insert(
            tk.END, f"\nSOLUÇÃO FINAL (Têmpera Simulada):\n")
        self.texto_resultados.insert(
            tk.END, f"Rota: {self.formatar_rota(melhor_solucao)}\n")
        self.texto_resultados.insert(tk.END, f"Distância: {melhor_distancia}\n")
        self.texto_resultados.insert(tk.END, f"Iterações totais: {iteracao}\n")
        self.texto_resultados.insert(
            tk.END, f"Movimentos aceitos (incl. piores): {movimentos_aceitos} ({taxa_aceitacao:.1f}%)\n")
        self.texto_resultados.insert(
            tk.END, f"Temperatura final atingida: {temperatura:.2f}\n")
        melhoria = self.distancia_inicial - melhor_distancia
        self.texto_resultados.insert(
            tk.END, f"Melhoria sobre a solução inicial do problema ({self.distancia_inicial}): {melhoria}\n\n")
        return melhor_distancia, melhor_solucao

    def executar_todos_metodos(self):
        self.texto_resultados.insert(tk.END, "====== EXECUTANDO TODOS OS MÉTODOS ======\n\n")
        self.mestre.update()

        resultados = {}

        # Executa Subida de Encosta
        self.texto_resultados.insert(tk.END, "--- INICIANDO: SUBIDA DE ENCOSTA ---\n")
        dist_hc, rota_hc = self.subida_encosta()
        resultados["Subida de Encosta"] = {"distancia": dist_hc, "rota": rota_hc}
        self.texto_resultados.insert(tk.END, "--- SUBIDA DE ENCOSTA FINALIZADA ---\n\n")
        self.mestre.update()

        # Executa Subida de Encosta Alterada
        self.texto_resultados.insert(tk.END, "--- INICIANDO: SUBIDA DE ENCOSTA ALTERADA ---\n")
        dist_hca, rota_hca = self.subida_encosta_alterada()
        resultados["Subida de Encosta Alterada"] = {"distancia": dist_hca, "rota": rota_hca}
        self.texto_resultados.insert(tk.END, "--- SUBIDA DE ENCOSTA ALTERADA FINALIZADA ---\n\n")
        self.mestre.update()

        # Executa Têmpera Simulada
        self.texto_resultados.insert(tk.END, "--- INICIANDO: TÊMPERA SIMULADA ---\n")
        dist_ts, rota_ts = self.tempera_simulada()
        resultados["Têmpera Simulada"] = {"distancia": dist_ts, "rota": rota_ts}
        self.texto_resultados.insert(tk.END, "--- TÊMPERA SIMULADA FINALIZADA ---\n\n")
        self.mestre.update()

        self.texto_resultados.insert(tk.END, "====== RESUMO COMPARATIVO DOS MÉTODOS ======\n")
        self.texto_resultados.insert(tk.END, f"Distância Inicial do Problema: {self.distancia_inicial}\n\n")

        melhor_distancia_global = float('inf')
        melhor_metodo_global = "Nenhum"

        for nome_metodo, resultado in resultados.items():
            distancia = resultado["distancia"]
            rota = resultado["rota"]
            melhoria = self.distancia_inicial - distancia if distancia is not None else "N/A"
            
            self.texto_resultados.insert(tk.END, f"Método: {nome_metodo}\n")
            self.texto_resultados.insert(tk.END, f"  Distância Final: {distancia if distancia is not None else 'N/A'}\n")
            self.texto_resultados.insert(tk.END, f"  Rota Final: {self.formatar_rota(rota) if rota is not None else 'N/A'}\n")
            self.texto_resultados.insert(tk.END, f"  Melhoria sobre Inicial: {melhoria}\n\n")

            if distancia is not None and distancia < melhor_distancia_global:
                melhor_distancia_global = distancia
                melhor_metodo_global = nome_metodo

        self.texto_resultados.insert(tk.END, "------------------------------------------\n")
        self.texto_resultados.insert(tk.END, f"MELHOR RESULTADO GLOBAL: {melhor_metodo_global}\n")
        self.texto_resultados.insert(tk.END, f"COM DISTÂNCIA: {melhor_distancia_global}\n")
        self.texto_resultados.insert(tk.END, "==========================================\n\n")
        self.mestre.update()


if __name__ == "__main__":
    raiz = tk.Tk()
    app = AplicacaoPrincipal(raiz)
    raiz.mainloop()