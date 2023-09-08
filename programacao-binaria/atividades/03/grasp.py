# -*- coding: utf-8 -*-
"""GRASP

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ahfDd_QW6B_o_hbMzGF447tASaCdU9f-
"""

#################################################################################################
# GRASP
#Copyright 2023 Mateus Chacon Danielle Gomes e Quézia Maia

# Este programa é um software livre, você pode redistribuí-lo e/ou modificá-lo
# sob os termos da Licença Pública Geral GNU como publicada pela Fundação do Software Livre (FSF),
# na versão 3 da Licença, ou (a seu critério) qualquer versão posterior.

# Este programa é distribuído na esperança de que possa ser útil, mas SEM NENHUMA GARANTIA,
# e sem uma garantia implícita de ADEQUAÇÃO a qualquer MERCADO ou APLICAÇÃO EM PARTICULAR.

# Veja a Licença Pública Geral GNU para mais detalhes
#################################################################################################
import time
import random
##================================================================
## CLASSE DO GRASP
##================================================================
class Grasp:
    ##-----------------------------
    ## CONTRUTOR DA CLASSE GRASP
    ##-----------------------------
    def __init__(self,alpha,max_iter,time_limit_seconds, matrix):
        self.alpha = alpha
        self.max_iter = max_iter
        self.time_limit_seconds = time_limit_seconds
        self.matrix = matrix
        self.N = len(self.matrix)
    ##-------------------------------------------------
    ## CRIA SOLUÇÃO ALEATÓRIA COM CRL
    ##-------------------------------------------------
    def construir_solucao_com_crl(self):
        solucao = [0] * self.N
        candidatos = list(range(self.N))
        
        while candidatos:
            # Seleciona aleatoriamente um subconjunto de candidatos com base em alfa
            tamanho_candidatos = max(1, int(self.alpha * len(candidatos)))
            subconjunto_candidatos = random.sample(candidatos, tamanho_candidatos)
            
            melhor_contribuicao = float('-inf')
            melhor_candidato = None
            
            solucao_current = [0] * self.N
            for candidato in subconjunto_candidatos:
                solucao_current[candidato] = 1
                contribuicao = self.evaluate_solution(solucao_current)

                if contribuicao > 0 and contribuicao > melhor_contribuicao:
                    melhor_contribuicao = contribuicao
                    melhor_candidato = candidato

            if (melhor_candidato!=None):      
                solucao[melhor_candidato] = 1
                candidatos.remove(melhor_candidato)
            else:
                break
        return solucao
    ##-------------------------------------------------
    ## CRIA SOLUÇÃO GULOSA PELO FITNES COM CRL
    ##-------------------------------------------------
    def construir_crl(self):
        # Calcular fitness das colunas e linhas
        fitness_colunas = [0] * self.N
        fitness_linhas = [0] * self.N
        for i in range(self.N):
            for j in range(self.N):
                fitness_colunas[j] += self.matrix[i][j]
                fitness_linhas[i] += self.matrix[i][j]
        
        # Criar uma lista de candidatos (CRL) ordenada por fitness total (coluna + linha)
        fitness = [(i, fitness_colunas[i] + fitness_linhas[i]) for i in range(self.N)]
        fitness.sort(key=lambda x: x[1], reverse=True)
        candidatos = []
        for candidato,fitness in fitness:
            candidatos.append(candidato)

        return candidatos

    def construir_solucao_com_crl_gulosa(self):
        solucao = [0] * self.N
        candidatos = self.construir_crl()
        
        while candidatos:
            # Seleciona aleatoriamente um subconjunto de candidatos com base em alfa
            tamanho_candidatos = max(1, int(self.alpha * len(candidatos)))
            subconjunto_candidatos = []
            for i in range(tamanho_candidatos):
                subconjunto_candidatos.append(candidatos[i])
            
            melhor_contribuicao = float('-inf')
            melhor_candidato = None
            
            solucao_current = [0] * self.N
            for candidato in subconjunto_candidatos:
                solucao_current[candidato] = 1
                contribuicao = self.evaluate_solution(solucao_current)

                if contribuicao > 0 and contribuicao > melhor_contribuicao:
                    melhor_contribuicao = contribuicao
                    melhor_candidato = candidato

            if (melhor_candidato!=None):      
                solucao[melhor_candidato] = 1
                candidatos.remove(melhor_candidato)
            else:
                break
        return solucao
    ##-----------------------------
    ## FUNÇÃO QUE CALCULA FO
    ##-----------------------------
    def evaluate_solution(self,solution):
        score = 0
        for i in range(self.N):
            for j in range(self.N):
                score += solution[i] * self.matrix[i][j] * solution[j]
        return score
    ##-----------------------------
    ## FUNÇÃO PERTUBAÇÃO
    ##-----------------------------
    def first_improvement(self,solution):
        best_score = self.evaluate_solution(solution)

        for i in range(self.N):
            current_solution = list(solution)
            current_solution[i] = 1 - current_solution[i]  # Flip the bit

            current_score = self.evaluate_solution(current_solution)
            if current_score > best_score:
                solution = current_solution
                best_score = current_score

        return solution, best_score
    ##-----------------------------
    ## METODO PRINCIPAL DO GRASP
    ##-----------------------------
    def solve(self):
        random.seed(int(time.time()))
        # best_solution = self.construir_solucao_com_crl()
        best_solution = self.construir_solucao_com_crl_gulosa()
        best_score = self.evaluate_solution(best_solution)
        start_time = time.time()

        for _ in range(1, self.max_iter + 1):
            current_solution = self.construir_solucao_com_crl_gulosa()
            current_solution, current_score = self.first_improvement(current_solution)

            if current_score > best_score:
                best_solution = current_solution
                best_score = current_score

            elapsed_time = time.time() - start_time
            if elapsed_time >= self.time_limit_seconds:
                break

        return best_solution, best_score, elapsed_time 
##================================================================
## CLASSE PARA LEITURA
##================================================================
class Read:
    def __init__(self,name):
        self.name = name
    def getMatriz(self):
        with open("./instances/"+self.name, "r") as file:
            linhas = file.readlines()
            linhas = linhas[1:]
        listas = []
        for linha in linhas:
            valores = linha.strip().split()
            numeros = [float(valor) for valor in valores]
            listas.append(numeros)
        tamanho_matriz = len(listas)
        matriz1 = []
        for i in range(tamanho_matriz):
            linha = [0] * i + listas[i]
            matriz1.append(linha)
        return matriz1
##================================================================
## CLASSE PARA EXECUTAR EM PARALELO
##================================================================
import threading

class Thread:
    ##-----------------------------
    ## CONTRUTOR DA CLASSE GRASP
    ##-----------------------------
    def __init__(self,executions=[]):
        self.results = {}
        self.executions = executions
    ##-----------------------------
    ## GERAR IDENTIFICADOR DO PROCESSO
    ##-----------------------------
    def generateKey(self,grasp):
        return str(grasp.alpha)+"|"+str(grasp.max_iter)
    ##-----------------------------
    ## EXETCUTA PROCESSO
    ##-----------------------------
    def process(self,grasp,id=0):
        print('Iniciando_Processo_'+str(id))
        best_solution, best_score, elapsed_time = grasp.solve()
        self.results[self.generateKey(grasp)] = {
            'alpha':grasp.alpha,
            'max_iter':grasp.max_iter,
            'melhor_solucao':best_solution,
            'melhor_pontuacao':best_score,
            'tempo':elapsed_time
        }
        print('Finalizando_Processo_'+str(id))
    ##-----------------------------
    ## EXECUTA AS THREADS
    ##-----------------------------
    def executa(self):
        self.results.clear()
        threads = []
        id = 0
        
        for grasp in self.executions:
            thread = threading.Thread(target=self.process, args=(grasp,id))
            threads.append(thread)
            thread.start()
            id=id+1
        
        for thread in threads:
            thread.join() 

    def getResults(self):
        return self.results
##================================================================
## CLASSE PARA GERAR GRAFICOS
##================================================================
import matplotlib.pyplot as plt
import json
class Graphic:
    def __init__(self, results = {}, name=""):
        self.results = results
        self.name = name
        self.c = []
        self.fo = []
        self.time = []
        for chave in self.results.keys():
            s = self.results[chave]
            self.c.append(str(chave))
            self.fo.append(s['melhor_pontuacao'])
            self.time.append(s['tempo'])

    def ploatFOs(self):
        plt.figure(figsize=(20, 10)) 
        plt.bar(self.c,self.fo)
        plt.title('Gráfico de soluções')
        plt.xlabel('Paramêtros (alpha|maxIter)')
        plt.ylabel('Valores (FO)')
        for i in range(len(self.c)):
            plt.text(self.c[i], self.fo[i] +0.5, str(self.fo[i]), ha='center', va='bottom')
        plt.savefig('./graficos/FO_graphic_'+self.name+'.png')

    def ploatTimes(self):
        plt.figure(figsize=(20, 10)) 
        plt.plot(self.c,self.time)
        plt.title('Gráfico de Tempos')
        plt.xlabel('Paramêtros (alpha|maxIter)')
        plt.ylabel('Tempo')
        plt.savefig('./graficos/TE_graphic_'+self.name+'.png')
    
    def salveResultsJson(self):
        lp = "./resultados/resultados_"+self.name+".json"
        with open(lp, 'a') as arquivo:
            arquivo.write(json.dumps(self.results)) 
##===========================================
## FUNÇÃO MAIN
##===========================================
# Instância |x| MAX-QBF (Z∗)    MAX-QBFAC (Z∗)
# qbf020 20     151             104
# qbf040 40     429             251
# qbf060 60     > 572           > 396
# qbf090 80     > 965           > 586
# qbf100 100    > 1451          > 862
def __main__():
    files = ['qbf020','qbf040','qbf060','qbf080','qbf100']
    # files = ['qbf100']
    alpha = [0.2,0.4,0.6,0.8,1]
    # max_iter = [1,500,1000]
    max_iter = [1]
    time_limit_seconds = 1800

    # read = Read(files[0])
    # matrix = read.getMatriz()
    # graps = Grasp(alpha=alpha[4],max_iter=max_iter[0],time_limit_seconds=time_limit_seconds,matrix=matrix)
    # print(graps.solve())

    for file in files:
        print(" *** ")
        print("Resolvendo_Instancia_",file)
        read = Read(file)
        matrix = read.getMatriz()

        executions=[]
        for j in range(len(max_iter)):
            for i in range(len(alpha)):
                executions.append(Grasp(alpha=alpha[i],max_iter=max_iter[j],time_limit_seconds=time_limit_seconds,matrix=matrix))

        thread = Thread(executions=executions)
        thread.executa()

        graphic = Graphic(thread.getResults(),file)
        graphic.ploatFOs()
        graphic.ploatTimes()
        graphic.salveResultsJson()

__main__()