from scipy.special import gamma
import numpy as np
import statistics

def x():

    vetor_x = np.zeros((3,))
    
    x1 = int(input("Escolha x1: "))
    x2 = int(input("Escolha x2: "))
    x3 = int(input("Escolha x3: "))

    vetor_x[0] = x1
    vetor_x[1] = x2
    vetor_x[2] = x3
    
    return vetor_x

def y():
    
    vetor_y = np.zeros((3,))
    
    y1 = int(input("Escolha y1: "))
    y2 = int(input("Escolha y2: "))
    y3 = int(input("Escolha y3: "))

    vetor_y[0] = y1
    vetor_y[1] = y2
    vetor_y[2] = y3
    
    return vetor_y


def theta(n, x, y):
    
    params = x + y

    vetor_theta = np.random.dirichlet(params, n)

    return vetor_theta

def f(theta, x, y):
    
    params = x + y
    
    beta = np.prod(gamma(params))/ gamma(np.sum(params))
    
    resul = (1/beta)*np.prod(theta**(x + y - 1), axis = 1)
    
    return resul

def hitu(v1, v2, n, theta, x, y):
    
    est_w = 1/n*len(np.argwhere((f(theta, x, y) <= v2) & (f(theta, x, y) >= v1)))
    
    return est_w

def u():
    
    vetor_x = x()
    vetor_y = y()
    
    k = int(input("Escolha k: "))
    
    vk = float(input("Escolha v: "))
    
    n_inicial = 50000
    
    erro = 1
    
    ints = []
    
    while erro > 0.0005:
        
        n_inicial = n_inicial*2
    
        for i in range(5):

            vetor_theta = theta(n_inicial, vetor_x, vetor_y)
        
    
            ff = f(vetor_theta, vetor_x, vetor_y)
        
    
            cort = np.zeros((1,))
            cortes = statistics.quantiles(ff, n = k)
            cortes = np.concatenate((cort, cortes), axis = 0)
            maxi = np.array([np.max(ff)])
            cortes = np.concatenate((cortes, maxi), axis = 0)
            
            
            v = cortes[cortes <= vk]
            area = 1/k*(len(v) - 1)
            if vk not in v and len(v) < k + 1:
                area += hitu(v[-1], vk, n_inicial, vetor_theta, vetor_x, vetor_y) 
        
            ints.append(area)
        
    
        var = np.var(np.array(ints), ddof = 1)
        
        erro = 2.575*np.sqrt(var)/np.sqrt(len(ints))
        
    vetor_theta = theta(n_inicial, vetor_x, vetor_y)
    
    ff = f(vetor_theta, vetor_x, vetor_y)
    
    cort = np.zeros((1,))
    cortes = statistics.quantiles(ff, n = k)
    cortes = np.concatenate((cort, cortes), axis = 0)
    maxi = np.array([np.max(ff)])
    cortes = np.concatenate((cortes, maxi), axis = 0)
    
    v = cortes[cortes <= vk]
    area = 1/k*(len(v) - 1)
    if vk not in v and len(v) < k + 1:
        area += hitu(v[-1], vk, n_inicial, vetor_theta, vetor_x, vetor_y) 

        
    print(erro)
    print(n_inicial)    
    print(area)
def umcmc():
    
    vetor_x = x() # chama o vetor x para o usu??rio escolher
    vetor_y = y() # chama o vetor y para o usu??rio escolher
    
    k_inicial = 2000 # ARRUMAR ISSO
    
    vk = float(input("Escolha v: ")) # pede pro usu??rio escolher o corte v (at?? onde a integral ser?? calculada)
    
    n_inicial = 100000 
    
    # calcula estimativa
    
    vetor_theta = theta(n_inicial, vetor_x, vetor_y) # calcula o vetor theta
        
    
    ff = f(vetor_theta, vetor_x, vetor_y) # calcula a fun????o densidade de probabilidade posteriori de Dirichlet 
        
    # aqui come??a a se calcular a lista de cortes
    cort = np.zeros((1,)) # primeiro corte v = 0
    cortes = statistics.quantiles(ff, n = k_inicial) # segundo corte at?? o k-??simo corte (sem os extremos, sem o primeiro e ??ltimo corte)
    cortes = np.concatenate((cort, cortes), axis = 0) # junta o primeiro com o resto
    maxi = np.array([np.max(ff)]) # (k+1)-??simo corte, ou seja, ??ltimo corte, v  = sup(f)
    cortes = np.concatenate((cortes, maxi), axis = 0) # junta todos os cortes
    # a lista tem k + 1 elementos, pontos de corte, resultando em k bins
    # de modo que a ??rea em cada bin ?? 1/k
            
    v = cortes[cortes <= vk] # considera apenas os elementos at?? o corte escolhido pelo usu??rio
    # calcula a ??rea: soma da ??rea de todos os bins da lista
    # como a ??rea em cada bin ?? 1/k basta multiplicar 1/k pelo n??mero total de bins (comprimento da lista - 1 no caso)
    area = 1/k_inicial*(len(v) - 1)
    if vk not in v and len(v) < k_inicial + 1: # se o corte escolhido n??o esta na lista e o comprimento da lista diminuiu
        # calcula a ??rea do ultimo valor da lista at?? o corte escolhido e soma na ??rea
        area += hitu(v[-1], vk, n_inicial, vetor_theta, vetor_x, vetor_y)
    
    n_novo = int((area*(1 - area))*(2.575/0.0005)**2)
    k_novo = int(4*(2*n_novo**2/2.575)**(1/5))
    if n_novo < n_inicial:
        n_novo = n_inicial
    if k_novo < k_inicial:
        k_novo = k_inicial
    # ap??s ter achado n
    
    vetor_theta = theta(n_novo, vetor_x, vetor_y) # calcula o vetor theta com n certo
    
    ff = f(vetor_theta, vetor_x, vetor_y) # calcula a fun????o densidade de probabilidade posteriori de Dirichlet

    # calcula de novo os cortes, do mesmo modo que anteriormente
    cort = np.zeros((1,)) # primeiro corte v = 0
    cortes = statistics.quantiles(ff, n = k_novo) # segundo corte at?? o k-??simo corte (sem os extremos, sem o primeiro e ??ltimo corte)
    cortes = np.concatenate((cort, cortes), axis = 0) # junta o primeiro com o resto
    maxi = np.array([np.max(ff)]) # (k+1)-??simo corte, ou seja, ??ltimo corte, v  = sup(f)
    cortes = np.concatenate((cortes, maxi), axis = 0) # junta todos os cortes
    # a lista tem k + 1 elementos, pontos de corte, resultando em k bins
    # de modo que a ??rea em cada bin ?? 1/k

    # calcula a area (estimativa da integral) do mesmo modo
    v = cortes[cortes <= vk] # considera apenas os elementos at?? o corte escolhido pelo usu??rio
    # calcula a ??rea: soma da ??rea de todos os bins da lista
    # como a ??rea em cada bin ?? 1/k basta multiplicar 1/k pelo n??mero total de bins (comprimento da lista - 1 no caso)
    area = 1/k_novo*(len(v) - 1)
    if vk not in v and len(v) < k_novo + 1: # se o corte escolhido n??o esta na lista e o comprimento da lista diminuiu
        # calcula a ??rea do ultimo valor da lista at?? o corte escolhido e soma na ??rea
        area += hitu(v[-1], vk, n_inicial, vetor_theta, vetor_x, vetor_y) 
        
    # printa o valor da ??rea
    print(n_novo)
    print(area)
umcmc()