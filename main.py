# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:45:04 2020

@author: Bruno Costa

O objetivo desse código é desenvolver um algoritmo de otimização multiobjetivo utilizando NSGA2 que 
maximize o Isp do propulsor e minimize os custos de propelente e pressurizante


"""
# Algoritmo de otimizacao multiobjetivo utilizando Nondominated Sorting Genetic Algorithm II (NSGA 2)
import init
import otimizacao_multiobjetivo as moga
import population
import random
import time
import matplotlib.pyplot as plt
#import shutil
from datetime import date
import numpy as np
from mpl_toolkits.mplot3d import axes3d


inicio = time.time()

#----------------------- Entradas do algoritmo de Otimização -----------------------

num_geracoes = 10
pop_size = 40
eta_sbx = 4
eta_poly_mutation = 20

#----------------------- Entradas do algoritmo de Otimização -----------------------


#---------------------------------- Loop Principal----------------------------------

geracoes = []
P = [] # Populacao 
Q = [] # População de filhos

teste1_list = []


# # Criando uma população inicial
povoamento = init.first_gen(pop_size)
P.append(povoamento.population)

teste1 = povoamento.population
teste1_list.append(povoamento)

# # Criando a primeira população de filhos
povoamento = init.next_gen(1, pop_size, povoamento, eta_sbx, eta_poly_mutation) # mudei de 1 para 0
Q.append(povoamento.population)

teste2 = povoamento.population
teste1_list.append(povoamento)

geracao = 1
while geracao < num_geracoes:
    R = [] # População de Pais e Filhos    
    R.extend(P[geracao - 1])
    R.extend(Q[geracao - 1])
    geracoes.append(R)
    
    frentes = moga.fast_nondominated_sort(R)

    i = 1
    P_novo = [] 
            
    while len(P_novo) + len(frentes[i]) <= pop_size:
        moga.crowding_distance(frentes[i])
        P_novo.extend(frentes[i])
        i += 1
    moga.crowding_distance(frentes[i]) 
    moga.sort_crowding(frentes[i])
    
    for solucoes in frentes[i]:      
        P_novo.extend([solucoes])
        if (pop_size - len(P_novo)) == 0:
            break
    
    povoamento = population.Population(pop_size)
    povoamento.population = P_novo[:]
    P.append(povoamento.population)
    
    del P_novo[:]
    
    geracao = geracao + 1
    
    povoamento = init.next_gen(geracao, pop_size, povoamento, eta_sbx, eta_poly_mutation)
    Q.append(povoamento.population)
    
    teste1_list.append(povoamento)
    
#---------------------------------- Loop Principal----------------------------------


#------------------------------ Tempo de processamento------------------------------
fim = time.time()
print(f' Tempo de Processamento = {fim - inicio}')
#------------------------------ Tempo de processamento------------------------------

 
#-------------------------------- Armazenando no txt--------------------------------

now = str(date.today())

local = '/home/bruno/Documentos/GitHub/Abordagem-2_Otimizacao-de-Sistema-Propulsivo-com-NSGA_2/banco_dados/'
nome_arquivo = str(f'{now}_{num_geracoes}_{pop_size}')
endereco = local + nome_arquivo + '.txt'

with open(endereco,'w') as arquivo:
    arquivo.write('--' * 90 + '\n')
    arquivo.write('\n')
    arquivo.write(f'Otimização Multiobjetivo de sistema um propulsivo Bi-propelente utilizando NSGA2 ' + '\n')
    arquivo.write(f'Objetico 1 = Maximizar Isp' + '\n')
    arquivo.write(f'Objetico 2 = Minimizar Massa Total do Sistema Propulsivo' + '\n')
    arquivo.write('\n')

    arquivo.write(f'Parâmetros do Algoritmo Genético de otimização:' + '\n')
    arquivo.write(f'Tamanho da população = {pop_size}' + '\n')
    arquivo.write(f'Número de gerações  = {num_geracoes}' + '\n')
    arquivo.write(f'Eta SBX  = {eta_sbx}' + '\n')
    arquivo.write(f'Eta Poly mutation = {eta_poly_mutation}' + '\n')
    arquivo.write('\n')

    arquivo.write(f'Informações de Entrada do Programa ' + '\n')
    arquivo.write(f'Par propelente = {povoamento.fuel} e {povoamento.oxidizer} '+ '\n')
    arquivo.write(f'Delta V = {povoamento.deltav} m/s '+ '\n')
    #arquivo.write(f'Massa do Lançador = {povoamento.m_rocket} Kg'+ '\n')
    arquivo.write(f'Massa da Carga útil = {povoamento.mpay} Kg'+ '\n')

    arquivo.write('\n')
    arquivo.write(f'Tempo de Processamento: {(fim - inicio)} segundos' + '\n')

    arquivo.write('--' * 90 + '\n')
    arquivo.write('--' * 90 + '\n')
    arquivo.write('--' * 90 + '\n')
    for geracao in range(0, num_geracoes):
        arquivo.write(f' GERACAO {geracao}' + '\n' + '-$$' * 60 + '\n' * 2)
        for b in P[geracao]:
            arquivo.write(f'Rank ( {b.rank} ) | ISP = {round(b.isp)} s | Cf = {round(b.Cf, 2)} | cstar = {round(b.cstar, 2)} m/s | F = {round(b.empuxo)} N | O/F = {round(b.genes[0], 1)} | Pc = {round(b.genes[1] * 14.504, 1)} psi | Temp = {round(b.temperaturaCC)} K | dt = {round(b.genes[2], 1)} mm | R_exp = {round(b.Razao_Expansao, 1)} | tb = {round(b.t_burn, 1)} s ' + '\n')
            arquivo.write(f'             DeltaP injetor = {round(b.deltaP_inj * 14.504, 1)} psi | M_prop= {round(b.massa_propelente, 1)} Kg | M_sistema = {round(b.massa_total, 1)} Kg ' + '\n' + '--' * 90 + '\n' ) 
#-------------------------------- Armazenando no txt--------------------------------


#-------------------------------- Plotando graficos --------------------------------

isp = []
massa_total = []

isp_g1 = []
massa_total_g1 = []


for individuo in P[num_geracoes-1]:
    isp.append(individuo.isp)
    massa_total.append(individuo.massa_total)

for individuo in P[1]:
    isp_g1.append(individuo.isp)
    massa_total_g1.append(individuo.massa_total)


plt.title('Etanol - LOX(Geração 1)', fontsize = 20, color='#0c2356')
plt.scatter(isp_g1, massa_total_g1, color='r')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


# plt.figure()
plt.scatter(isp, massa_total, color='#27a9e1')
plt.title('Etanol - LOX', fontsize = 20, color='#0c2356')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 20, color='#0c2356')
plt.scatter(isp_g1, massa_total_g1, color='r')
plt.scatter(isp, massa_total, color='#27a9e1')
plt.xlabel('isp [s]', fontsize = 15, color='#0c2356')
plt.ylabel('Massa Total do Sistema Prpulsivo [kg]', fontsize = 15, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

#-------------------------------- Plotando graficos --------------------------------