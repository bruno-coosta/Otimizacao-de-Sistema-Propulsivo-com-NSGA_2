# -*- coding: utf-8 -*-
"""
Created on Mon Dec 14 18:10:49 2020

@author: Bruno Costa
"""

import population
import random
import math
import equations as eq


# #---------------------------------- Entradas do Programa ----------------------------------
# deltav = 6600 # m/s - Acréscimo de velocidade
# mpay = 400 # kg - massa da payload

# #---------------------------------- Entradas do Programa ----------------------------------


def binary_tournament_so(pop, resample=False):

    if not resample:
        # print(f'POPULACAO VIAVEL {len(pop)}')
        competitors = random.sample(pop, 2)
        while competitors[0] == competitors[1]:
            competitors[1] = random.sample(pop, 1)
        try:
            if competitors[0].rank < competitors[1].rank:
                return competitors[0]

            elif competitors[0].rank > competitors[1].rank:
                return competitors[1]
            
            elif competitors[0].rank == competitors[1].rank:
                return random.choice([competitors[0], competitors[1]])
            
        except:
            print(f'individuo bugado é o: {competitors[0].name} ou o {competitors[1].name} \n  genes: {competitors[0].genes} e {competitors[1].genes}')

    else:
        pass
    
    
def sbx(parent1, parent2, etac):

    child1 = population.Individual()
    child2 = population.Individual()

    for gene in parent1.genes:

        u = random.random()
        # print('u:', u)
        if u <= 0.5:
            betaq = (2*u)**(1/(etac+1))
        else:
            betaq = (1/(2*(1-u)))**(1/(etac+1))

  
        gene_child1 = round(0.5 * ((1+betaq)*gene + (1-betaq)*parent2.genes[parent1.genes.index(gene)]), 5)
        gene_child2 = round(0.5 * ((1-betaq)*gene + (1+betaq)*parent2.genes[parent1.genes.index(gene)]), 5)

        
        # Restrição da OF
        
        if parent1.genes.index(gene) == 0:
            if gene_child1 < parent1.genes_lower[0]: gene_child1 = parent1.genes_lower[0]
            if gene_child2 < parent1.genes_lower[0]: gene_child2 = parent1.genes_lower[0]
            
            if gene_child1 > parent1.genes_upper[0]: gene_child1 = parent1.genes_upper[0]
            if gene_child2 > parent1.genes_upper[0]: gene_child2 = parent1.genes_upper[0]
        
        
        # Restrição da pressao de Camara
        
        if parent1.genes.index(gene) == 1:
            if gene_child1 < parent1.genes_lower[1]: gene_child1 = parent1.genes_lower[1]
            if gene_child2 < parent1.genes_lower[1]: gene_child2 = parent1.genes_lower[1]
            if gene_child1 > parent1.genes_upper[1]: gene_child1 = parent1.genes_upper[1] # nao tinha
            if gene_child2 > parent1.genes_upper[1]: gene_child2 = parent1.genes_upper[1]
            
        # Restrição da At
        
        if parent1.genes.index(gene) == 2:
            if gene_child1 < parent1.genes_lower[2]: gene_child1 = parent1.genes_lower[2]
            if gene_child2 < parent1.genes_lower[2]: gene_child2 = parent1.genes_lower[2]
            
            if gene_child1 > parent1.genes_upper[2]: gene_child1 = parent1.genes_upper[2]
            if gene_child2 > parent1.genes_upper[2]: gene_child2 = parent1.genes_upper[2]
        
        # Restrição de P2
        
        if parent1.genes.index(gene) == 3:
            if gene_child1 < parent1.genes_lower[3]: gene_child1 = parent1.genes_lower[3]
            if gene_child2 < parent1.genes_lower[3]: gene_child2 = parent1.genes_lower[3]
            if gene_child1 > parent1.genes_upper[3]: gene_child1 = parent1.genes_upper[3]
            if gene_child2 > parent1.genes_upper[3]: gene_child2 = parent1.genes_upper[3]
        
        child1.genes.append(gene_child1)
        child2.genes.append(gene_child2)
        
        # print(child1.genes, child2.genes)
        # print('depois',f'gene = {parent1.genes.index(gene)}', gene_child1, gene_child2)
    # print()
    return [child1, child2]


def poly_mutation(individual, eta_m):

    for i, gene in enumerate(individual.genes):

        if random.random() <= 0.2: # Era 0.2

            r = random.random()
            if r >= 0.5:
                delta = 1 - (2*(1-r))**(1/(eta_m+1))
            else:
                delta = (2*r)**(1/(eta_m+1)) - 1

            gene += round(delta*(individual.genes_upper[i] - individual.genes_lower[i]), 5)
            #gene += delta*(individual.genes_upper[i] - individual.genes_lower[i])
            # print(delta)
            if gene > individual.genes_upper[i]:
                gene = individual.genes_upper[i]
            elif gene < individual.genes_lower[i]:
                gene = individual.genes_lower[i]
            # print('mut')
        else:
            pass
        



def fast_nondominated_sort(populacao):
    ''' Descobrir as frentes de Pareto, baseado no criteriode nao dominacao'''
    frentes = {} #frentes de pareto 
    frentes[1] = []   
    for p in populacao:
        p.calcula_objetivos()
        p.dominated_solutions = []
        p.domination_count = 0
        for q in populacao:
            q.calcula_objetivos()
            # print(p.isp, p.preco_total)
            # print(q.isp, q.preco_total)
            # print('--' *30)
            if p != q:
                if domina(p, q) == True: # se p domina q
                    # print('p domina q')
                    # print(f'{p.isp} e {p.massa_total} com np = {p.domination_count} dominam {q.isp} e {q.massa_total}')
                    # print('--' * 30)
                    p.dominated_solutions.append(q) # Adicionando q no conjunto de soluções dominadas por p
                elif domina(q, p) == True: # se q domina p
                    # print('q domina p')    
                    # print(f'{q.isp} e {q.massa_total} com np = {q.domination_count} dominam {p.isp} e {p.massa_total}')
                    # print('--' * 30)
                    p.domination_count +=1 # incrementando o contador de dominação de p
        if p.domination_count == 0: #verificando se pertence a primeira frente
            p.rank = 1        
            frentes[1].append(p)
    #         print(f'Rank {p.rank}: {p.name} -----> Isp = {p.isp} , massa = {p.massa_total} e np = {q.domination_count} ')
            
    # print('--' * 50)
    i = 1
    while len(frentes[i]) != 0:
        next_frente = [] #usando para armazenar os membros da próxima frente
        for p in frentes[i]:
            for q in p.dominated_solutions:
                q.domination_count -= 1
                if q.domination_count == 0:
                    q.rank = i + 1
                    next_frente.append(q)
        #             print(f'Rank {q.rank}: {q.name} -----> Isp = {q.isp} , massa = {q.massa_total} e np = {q.domination_count} ')
        # print('--' * 50)
                    
        i += 1
        frentes[i] = next_frente

        
    return frentes
                



def sort_crowding(P):
    for i in range(len(P) - 1, -1, -1):
        for j in range(1, i + 1):
            s1 = P[j - 1]
            s2 = P[j]
            
            if s1.rank > s2.rank:
                P[j - 1] = s2
                P[j] = s1
                
            elif s1.rank == s2.rank:
                if s1.crowding_distance < s2.crowding_distance:
                    P[j - 1] = s2
                    P[j] = s1
    



def crowding_distance(P):
    s_isp = 0
    s_massa = 0
    ''' Atribuir uma crowding distance para cada solucao em uma frente'''    
    for i in range(len(P) - 1, -1, -1):
        for j in range(1, i + 1):
            s1 = P[j - 1]
            s2 = P[j]
            
            if s1.isp > s2.isp:
                P[j - 1] = s2
                P[j] = s1
        
    P[0].crowding_distance = float('inf')
    P[len(P) - 1].crowding_distance = float('inf')
    
    for i in range(1, len(P) -1 ):
        P[i].crowding_distance = (P[i + 1].isp - P[i - 1].isp)/((350) - (240))
    #     print(f'cd ISP {P[i].crowding_distance}')
    #     s_isp +=P[i].crowding_distance
    # print(f'Soma IsP {s_isp}')
    for i in range(len(P) - 1, -1, -1):
            for j in range(1, i + 1):
                s1 = P[j - 1]
                s2 = P[j]
                
                if s1.massa_total > s2.massa_total:
                    P[j - 1] = s2
                    P[j] = s1
        
    P[0].crowding_distance = float('inf')
    P[len(P) - 1].crowding_distance = float('inf')
    
    for i in range(1, len(P) -1):
        P[i].crowding_distance += (P[i + 1].massa_total - P[i - 1].massa_total)/(189000 - 2400) 
    #     print(f' cd massa {P[i].crowding_distance}')
    #     s_massa +=P[i].crowding_distance
    # print(f'Soma massa {s_massa}')

def domina(solucao_A, solucao_B):
    '''Verifica qual solucao é dominante'''
    
    if solucao_A.isp >= solucao_B.isp and solucao_A.massa_total < solucao_B.massa_total :
        dominacao = True
        
    elif solucao_A.isp > solucao_B.isp and solucao_A.massa_total <= solucao_B.massa_total :
        dominacao = True
        
    else: 
        dominacao = False 
        
        
    return dominacao