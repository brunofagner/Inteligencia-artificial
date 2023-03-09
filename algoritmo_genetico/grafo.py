from array import *
import random
import matplotlib.pyplot as plt
import numpy as np
Gen = np.array([])
Fit = np.array([])

'''Create grafo'''
n = 40
grafo = []
for i in range(n):
	vertice = []
	for j in range(n):
		vertice.append(random.randint(0, 1))
	grafo.append(vertice)
for i in range(n):
	for j in range(0, i):
		grafo[i][j] = grafo[j][i]
for i in range(n):
	grafo[i][i] = 0
for v in grafo:
	print(v)

'''Limite superior para colorir'''
max_cores = 1
for i in range(n):
	if sum(grafo[i]) > max_cores:
		max_cores = sum(grafo[i]) + 1
print(max_cores)


'''Cria o individuo usando o numero de cores'''
numero_cores = max_cores
'''Algoritmo Genetico'''
condicao = True
while(condicao and numero_cores > 0):
	def criar_individuo():
		individuo = []
		for i in range(n):
			individuo.append(random.randint(1, numero_cores))
		return individuo
	'''Create populacao'''
	tamanho_populacao = 200
	geracao = 0
	populacao = []
	for i in range(tamanho_populacao):
		individuo = criar_individuo()
		populacao.append(individuo)

	'''Fitness'''
	def fitness(grafo, individuo):
		fitness = 0
		for i in range(n):
			for j in range(i, n):
				if(individuo[i] == individuo[j] and grafo[i][j] == 1):
					fitness += 1
		return fitness

	'''crusamento'''
	def crusamento(pai, mae):
		posicao = random.randint(2, n-2)
		filho1 = []
		filho2 = []
		for i in range(posicao+1):
			filho1.append(pai[i])
			filho2.append(mae[i])
		for i in range(posicao+1, n):
			filho1.append(mae[i])
			filho2.append(pai[i])
		return filho1, filho2

	def mutacao1(individuo):
		probabilidade = 0.4
		mutou = random.uniform(0, 1)
		if(mutou <= probabilidade):
			posicao = random.randint(0, n-1)
			individuo[posicao] = random.randint(1, numero_cores)
		return individuo

	def mutation2(individuo):
		probabilidade = 0.2
		mutou = random.uniform(0, 1)
		if(mutou <= probabilidade):
			posicao = random.randint(0, n-1)
			individuo[posicao] = random.randint(1, numero_cores)
		return individuo

	'''Torneio'''
	def selecao_por_torneio(populacao):
		nova_populacao = []
		for j in range(2):
			random.shuffle(populacao)
			for i in range(0, tamanho_populacao-1, 2):
				if fitness(grafo, populacao[i]) < fitness(grafo, populacao[i+1]):
					nova_populacao.append(populacao[i])
				else:
					nova_populacao.append(populacao[i+1])
		return nova_populacao

	'''Selecao por roleta'''
	def selecao_por_roleta(populacao):
		fitness_total = 0
		for individuo in populacao:
			fitness_total += 1/(1+fitness(grafo, individuo))
		comulativo_fitness = []
		comulativo_fitness_sum = 0
		for i in range(len(populacao)):
			comulativo_fitness_sum += 1 / \
				(1+fitness(grafo, populacao[i]))/fitness_total
			comulativo_fitness.append(comulativo_fitness_sum)

		nova_populacao = []
		for i in range(len(populacao)):
			roleta = random.uniform(0, 1)
			for j in range(len(populacao)):
				if (roleta <= comulativo_fitness[j]):
					nova_populacao.append(populacao[j])
					break
		return nova_populacao
	melhor_fitness = fitness(grafo, populacao[0])
	fittest_individuo = populacao[0]
	gen = 0
	
	while(melhor_fitness != 0 and gen != 10000):
		gen += 1
		populacao = selecao_por_roleta(populacao)
		nova_populacao = []
		random.shuffle(populacao)
		for i in range(0, tamanho_populacao-1, 2):
			filho1, filho2 = crusamento(populacao[i], populacao[i+1])
			nova_populacao.append(filho1)
			nova_populacao.append(filho2)
		for individuo in nova_populacao:
			if(gen < 200):
				individuo = mutacao1(individuo)
			else:
				individuo = mutation2(individuo)
		populacao = nova_populacao
		melhor_fitness = fitness(grafo, populacao[0])
		fittest_individuo = populacao[0]
		for individuo in populacao:
			if(fitness(grafo, individuo) < melhor_fitness):
				melhor_fitness = fitness(grafo, individuo)
				fittest_individuo = individuo
		if gen % 10 == 0:
			print("Geracao: ", gen, "melhor_fitness: ",
				melhor_fitness, "individuo: ", fittest_individuo)
		Gen = np.append(Gen, gen)
		Fit = np.append(Fit, melhor_fitness)
	print("Usando ", numero_cores, " cores : ")
	print("Geracao: ", gen, "melhor_fitness: ",
		melhor_fitness, "individuo: ", fittest_individuo)
	print("\n\n")
	if(melhor_fitness != 0):
		condicao = False
		print("O grafo é ", numero_cores+1, " coloravel")
	else:
		Gen = np.append(Gen, gen)
		Fit = np.append(Fit, melhor_fitness)
		plt.plot(Gen, Fit)
		plt.xlabel("Geração")
		plt.ylabel("Melhores-fitness")
		plt.show()
		Gen = []
		Fit = []
		numero_cores -= 1
