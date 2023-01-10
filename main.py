# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 14:45:04 2020

@author: Bruno Costa

O objetivo desse código é desenvolver um algoritmo de otimização multiobjetivo utilizando NSGA2 que 
maximize o Isp do propulsor e minimiza a massa total do sistema


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

num_geracoes = 61
pop_size = 100
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

isp = []
massa_total = []

F = []

for individuo in P[num_geracoes-1]:
    isp.append(individuo.isp)
    massa_total.append(individuo.massa_total)
    F.append(individuo.empuxo)


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
    arquivo.write(f'Empuxo Médio da última geração: {np.mean(F)}' + '\n')
    arquivo.write(f'Isp Médio da última geração: {np.mean(isp)}' + '\n')
    arquivo.write(f'Massa Total Média da última geração: {np.mean(massa_total)}' + '\n')


    arquivo.write('\n')
    arquivo.write(f'Tempo de Processamento: {(fim - inicio)} segundos' + '\n')
    

   

    arquivo.write('--' * 90 + '\n')
    arquivo.write('--' * 90 + '\n')
    arquivo.write('--' * 90 + '\n')
    for geracao in range(0, num_geracoes):
        arquivo.write(f' GERACAO {geracao}' + '\n' + '-$$' * 60 + '\n' * 2)
        for b in P[geracao]:
            arquivo.write(f'Rank ( {b.rank} ) | ISP = {round(b.isp, 2)} s | Cf = {round(b.Cf, 2)} | cstar = {round(b.cstar, 2)} m/s | F = {round(b.empuxo)} N | O/F = {round(b.genes[0], 2)} | Pc = {round(b.genes[1], 2)} bar | Pressão na saída do bocal = {round(b.genes[3], 4)} bar| Temp = {round(b.temperaturaCC)} K | dt = {round(b.genes[2], 2)} mm | R_exp = {round(b.Razao_Expansao, 2)} | tb = {round(b.t_burn, 1)} s ' + '\n')
            arquivo.write(f'             DeltaP injetor = {round(b.deltaP_inj, 2)} bar | M_prop= {round(b.massa_propelente, 1)} Kg | M_gas= {round(b.massa_pressurizante, 1)} Kg | M_tank_fuel= {round(b.massa_tank_fuel, 1)} Kg | M_tank_oxi= {round(b.massa_tank_oxi, 1)} Kg | M_tank_pressurizante= {round(b.massa_tank_pressurizante, 1)} Kg | M_motor= {round(b.massa_motor, 1)} Kg |  M_sistema = {round(b.massa_total, 1)} Kg |  M_final_sistema = {round(b.massa_estrutural, 1)} Kg |  Relação Empuxo/Peso inicial = {round(b.relacao_empuxo_peso_inicial, 2)} |  Relação Empuxo/Peso final = {round(b.relacao_empuxo_peso_final, 2)} ' + '\n' + '--' * 90 + '\n' ) 
#-------------------------------- Armazenando no txt--------------------------------


#-------------------------------- Plotando graficos --------------------------------

isp = []
massa_total = []

isp_g0 = []
massa_total_g0 = []

isp_g10 = []
massa_total_g10 = []

isp_g20 = []
massa_total_g20 = []

isp_g60 = []
massa_total_g60 = []

isp_geral = []
massa_total_geral = []

F = []



for individuo in P[0]:
    isp_g0.append(individuo.isp)
    massa_total_g0.append(individuo.massa_total)

plt.title('Etanol - LOX (Geração 0)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g0, massa_total_g0, color='r')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

for individuo in P[10]:
    isp_g10.append(individuo.isp)
    massa_total_g10.append(individuo.massa_total)

for individuo in P[20]:
    isp_g20.append(individuo.isp)
    massa_total_g20.append(individuo.massa_total)

for individuo in P[num_geracoes-1]:
    isp.append(individuo.isp)
    massa_total.append(individuo.massa_total)
    F.append(individuo.empuxo)

    

print('Empuxo Médio da última geração: ', np.mean(F))
print('Isp Médio da última geração: ', np.mean(isp))
print('Massa Total Média da última geração: ', np.mean(massa_total))

plt.rcParams['xtick.labelsize'] = 15
plt.rcParams['ytick.labelsize'] = 15



plt.title('Etanol - LOX (Geração 0)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g0, massa_total_g0, color='r')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.title('Etanol - LOX (Geração 10)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g10, massa_total_g10, color='green')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.title('Etanol - LOX (Geração 20)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g20, massa_total_g20, color='gray')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.scatter(isp, massa_total, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 26, color='#0c2356')
plt.scatter(isp_g0, massa_total_g0, color='r', label='Ger 0')
plt.scatter(isp, massa_total, color='#27a9e1', label='Ger 63')
plt.legend()
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 26, color='#0c2356')
plt.scatter(isp_g10, massa_total_g10, color='green', label='Ger 10')
plt.scatter(isp_g20, massa_total_g20, color='gray', label='Ger 20')
plt.scatter(isp, massa_total, color='#27a9e1', label='Ger 63')
plt.legend()
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


for conjunto in P:
    for individuo in conjunto:
        isp_geral.append(individuo.isp)
        massa_total_geral.append(individuo.massa_total)


plt.title('Etanol - LOX ', fontsize = 26, color='#0c2356')
plt.scatter(isp_geral, massa_total_geral, color='gray')
plt.scatter(isp, massa_total, color='#27a9e1')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



for individuo in P[60]:
    isp_g60.append(individuo.isp)
    massa_total_g60.append(individuo.massa_total)

plt.title('Etanol - LOX (Geração 60)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g60, massa_total_g60, color='#27a9e1')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.scatter(F, massa_total, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Empuxo [N]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

plt.scatter(F, isp, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Empuxo [N]', fontsize = 19, color='#0c2356')
plt.ylabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


#-------------------------------- Plotando graficos --------------------------------


plt.title('Etanol - LOX (Geração 0)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g0, massa_total_g0, color='r')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.title('Etanol - LOX (Geração 10)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g10, massa_total_g10, color='green')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.title('Etanol - LOX (Geração 20)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g20, massa_total_g20, color='gray')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



plt.scatter(isp, massa_total, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 26, color='#0c2356')
plt.scatter(isp_g0, massa_total_g0, color='r', label='Ger 0')
plt.scatter(isp, massa_total, color='#27a9e1', label='Ger 63')
plt.legend()
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.title('Etanol - LOX', fontsize = 26, color='#0c2356')
plt.scatter(isp_g10, massa_total_g10, color='green', label='Ger 10')
plt.scatter(isp_g20, massa_total_g20, color='gray', label='Ger 20')
plt.scatter(isp, massa_total, color='#27a9e1', label='Ger 63')
plt.legend()
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


for conjunto in P:
    for individuo in conjunto:
        isp_geral.append(individuo.isp)
        massa_total_geral.append(individuo.massa_total)


plt.title('Etanol - LOX ', fontsize = 26, color='#0c2356')
plt.scatter(isp_geral, massa_total_geral, color='gray')
plt.scatter(isp, massa_total, color='#27a9e1')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()



for individuo in P[60]:
    isp_g60.append(individuo.isp)
    massa_total_g60.append(individuo.massa_total)

plt.title('Etanol - LOX (Geração 60)', fontsize = 26, color='#0c2356')
plt.scatter(isp_g60, massa_total_g60, color='#27a9e1')
plt.xlabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()


plt.scatter(F, massa_total, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Empuxo [N]', fontsize = 19, color='#0c2356')
plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

plt.scatter(F, isp, color='#27a9e1')
plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
plt.xlabel('Empuxo [N]', fontsize = 19, color='#0c2356')
plt.ylabel('Isp [s]', fontsize = 19, color='#0c2356')
plt.grid(alpha=0.4)
plt.show()

# plt.scatter(P, massa_total, color='#27a9e1')
# plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
# plt.xlabel('Pressão na Câmara de Combustão [bar]', fontsize = 19, color='#0c2356')
# plt.ylabel('Massa Total do Sistema Propulsivo [kg]', fontsize = 19, color='#0c2356')
# plt.grid(alpha=0.4)
# plt.show()

# plt.scatter(P, isp, color='#27a9e1')
# plt.title('Etanol - LOX (Última geração)', fontsize = 26, color='#0c2356')
# plt.xlabel('Pressão na Câmara de Combustão [bar]', fontsize = 19, color='#0c2356')
# plt.ylabel('Isp [s]', fontsize = 19, color='#0c2356')
# plt.grid(alpha=0.4)
# plt.show()