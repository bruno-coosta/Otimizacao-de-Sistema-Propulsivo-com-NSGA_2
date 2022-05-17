import population
import random
import otimizacao_multiobjetivo as moga


def first_gen(pop_size, gen=0):

    povoamento = population.Population(pop_size) # Povamento é da classe Population 

    while len(povoamento.population) < povoamento.max_pop: # # Cria todos os indivíduos da população com seus genes distribuidos aleatoriamente dentro das faixas fornecidas. Enquanto o tamanho do vetor popualtion for menor que o tamanho da poulação

        individual = population.Individual()  
        individual.name = 'solucao ' + str(len(povoamento)+1)
        #individual.geracao = 1
        for i in range(len(individual.genes_lower)):
            gene = round(random.uniform(individual.genes_lower[i], individual.genes_upper[i]), 5)
            individual.genes.append(gene)
        povoamento.population.append(individual)
        

    return povoamento



def next_gen(gen, pop_size, populacao, eta_sbx, eta_poly_mutation):

    progenitores = populacao
    descendentes = population.Population(pop_size)
    descendentes.generation = gen

    # Enquanto a população de descendentes for menor do que N, aplicam-se os operadores genéticos:
    num = 1
    while len(descendentes.population) < descendentes.max_pop:
        progenitor1 = 0
        progenitor2 = 0
        while progenitor1 == progenitor2:
            progenitor1 = moga.binary_tournament_so(progenitores.population)
            progenitor2 = moga.binary_tournament_so(progenitores.population)

        children = moga.sbx(progenitor1, progenitor2, eta_sbx) # eta = 4

        children[0].name = f'solucao {pop_size*gen + (num*2 - 1)} '
        children[1].name = f'solucao {pop_size*gen + (num*2)}'
        children[0].parentes = [progenitor1.name, progenitor2.name]
        children[1].parentes = [progenitor1.name, progenitor2.name]

        moga.poly_mutation(children[0], eta_poly_mutation) # eta_poly = 20
        moga.poly_mutation(children[1], eta_poly_mutation)
        descendentes.population.extend(children)
        num += 1
    return descendentes
