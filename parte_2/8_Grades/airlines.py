from time import time  # Funcao para computar o tempo computacional
from heapq import heappush, heappop  # importa funções para lidar com o heap
import math  # Biblioteca para trabalhar com calculos matematicos
from itertools import permutations  # Biblioteca para trabalhar com permutacoes


def distancia_lat_long(lat1, lon1, lat2, lon2):
    """ Funcao que recebe a localizacao de duas cidades em latitude e longitude
    e retorna a distancia em km"""
    R = 6378  # raio da Terra em km
    pi = 3.141592653589793

    # converter graus para radianos
    lat1 = lat1 * pi / 180.0
    lon1 = lon1 * pi / 180.0
    lat2 = lat2 * pi / 180.0
    lon2 = lon2 * pi / 180.0

    # diferenças das coordenadas
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # fórmula de Haversine
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    return d


class Grafo:  # define a classe do grafo
    def __init__(self, vertices):  # define o construtor da classe
        self.vertices = vertices  # atribui o número de vértices à variável vertices
        self.grafo = [[] for i in range(vertices)]  # cria a lista de adjacência vazia para cada vértice

    def add_aresta(self, origem, destino, peso):  # define um método para adicionar uma aresta ao grafo
        self.grafo[origem].append((destino, peso))  # adiciona a aresta à lista de adjacência do vértice de origem

    def dijkstra(self, origem):  # define o método que implementa o algoritmo de Dijkstra
        dist = [float('inf')] * self.vertices  # inicializa a lista de distâncias com infinito para cada vértice
        dist[origem] = 0  # define a distância da origem para ela mesma como 0
        heap = []  # inicializa o heap vazio
        heappush(heap, (0, origem))  # adiciona a origem com distância 0 ao heap
        while heap:  # enquanto o heap não estiver vazio
            (peso, v) = heappop(heap)  # remove o vértice com a menor distância atual do heap
            if dist[v] < peso:  # se a distância atual para o vértice já for menor do que a distância registrada
                continue  # então não precisamos explorar esse vértice novamente
            for (u, w) in self.grafo[v]:  # para cada vizinho do vértice atual
                alt = dist[v] + w  # calcula a distância mínima até o vizinho
                if alt < dist[u]:  # se a distância calculada for menor do que a distância registrada
                    dist[u] = alt  # atualiza a distância mínima para o vizinho
                    heappush(heap, (alt, u))  # adiciona o vizinho ao heap com sua nova distância mínima
        return dist  # retorna a lista de distâncias mínimas calculadas


def entrada(nome_do_arquivo):
    """ Funcao que recebe o nome de um arquivo de entrada
     e vai computar a entrada do problema,
    e irah retornar os valores de entrada ajustados para o algoritmo"""

    # Ler dados do arquivo de Entrada
    with open(nome_do_arquivo, "r") as arquivo:
        dados = arquivo.readlines()

    # Imprimir dados de entrada na tela
    print("-" * 30, "Entrada:", nome_do_arquivo, "-" * 30)
    for dado in dados:
        print(dado, end="")
    print()

    # Ajustar dados de entrada

    # Posicao de leitura no dado
    posicao = 0

    problemas = []  # Inicializa o vetor de problemas

    while True:
        # Inicializando um problema
        # Um problema eh composto por N localizacoes de cidades
        # M voos diretos
        # Q pares de cidades que devem ser caculados a distancia entre elas
        problema = {"Localizacoes": [], "VoosDiretos": [], "CidadesCalcularDistancia": []}
        N, M, Q = [int(dado) for dado in dados[posicao].split(" ")]
        posicao += 1  # Avanca o ponteiro do arquivo

        # Ler localizacoes das cidades
        for _ in range(N):
            # Ler o nome da cidade, sua latitude e sua longitude
            cidade, latitude, longitude = [dado.strip() for dado in dados[posicao].split(" ")]

            # Conveter latitude e longitude para numeros reais
            latitude = float(latitude)
            longitude = float(longitude)

            # Adicionar no vetor de problema
            problema["Localizacoes"].append({"Cidade": cidade, "Latitude": latitude, "Longitude": longitude})

            posicao += 1  # Avanca o ponteiro do arquivo

        # Ler voos diretos
        for _ in range(M):
            # Ler o nome da cidade de origem e cidade de destino, voo direto
            cidadeOrigem, cidadeDestino = [dado.strip() for dado in dados[posicao].split(" ")]

            # Adicionar voo direto no vetor de problema
            problema["VoosDiretos"].append({"CidadeOrigem": cidadeOrigem, "CidadeDestino": cidadeDestino})
            posicao += 1  # Avanca o ponteiro do arquivo

        # Ler cidades as quais devem ser calculada a distancia
        for _ in range(Q):
            # Ler o nome da cidade de origem e cidade de destino
            cidadeOrigem, cidadeDestino = [dado.strip() for dado in dados[posicao].split(" ")]

            # Adicionar no vetor de problema
            problema["CidadesCalcularDistancia"].append({"CidadeOrigem": cidadeOrigem, "CidadeDestino": cidadeDestino})
            posicao += 1  # Avanca o ponteiro do arquivo

        # Adiciona o problema ao vetor de problemas
        problemas.append(problema)

        # Confere se a entrada terminou
        if dados[posicao] == "0 0 0\n":
            break  # Se terminou sai do loop

    return problemas  # Retorna os problemas que devem ser resolvidos


def resolve(problema, indice_problema):
    """
    Essa funcao recebe um problema e o indice do problema.
    O qual contem uma lista de cidades e suas respectivas latitudes e longitudes
    Seguido de uma lista que mostram os voos diretos existem de uma cidade para outra.
    Tambem eh recebido varios pares de cidade o qual deve-se encontrar a distancia entre essas duas cidades em km.
    Caso nao seja possivel ir de uma cidade para outra deve ser retornado que existe uma rota.
    A ideia seria montar um grafo direcionado onde cada vertice seria uma cidade, e cada aresta
    seria a possibilidade de transicao(voo) de um vertice para outro, ou seja,
    de uma cidade para outra.
    E depois calcular a distancia mínima dado um vertice de origem,
    utilizando o algoritmo de Djsktra.

    Segue o passo a passo abaixo:
    """

    # Cria-se o grafo com um numero de vertices definido (quantidade de cidades)
    grafo = Grafo(len(problema["Localizacoes"]))

    # Criar um id inteiro de identificacao para cidades
    identificacao = {}
    for indice, cidade in enumerate(problema["Localizacoes"]):
        identificacao[cidade["Cidade"]] = indice

    # Calcular a distancia entre as cidades e colocar em um objeto
    distancias = {}
    for cidade_origem, cidade_destino in permutations(problema["Localizacoes"], 2):
        distancias[(cidade_origem["Cidade"], cidade_destino["Cidade"])] = distancia_lat_long(cidade_origem["Latitude"],
                                                                                             cidade_origem["Longitude"],
                                                                                             cidade_destino["Latitude"],
                                                                                             cidade_destino[
                                                                                                 "Longitude"])

    # Para cada voo direto adicionar arestas
    for voo_direto in problema["VoosDiretos"]:
        # Adicionar uma aresta entre a cidade de origem e a de destino com o peso calculado no vetor de distancia
        grafo.add_aresta(identificacao[voo_direto["CidadeOrigem"]], identificacao[voo_direto["CidadeDestino"]],
                         distancias[(voo_direto["CidadeOrigem"], voo_direto["CidadeDestino"])])

    # Para cada par de cidade que deseja-se calcular a distancia
    # Deve-se rodar o algoritmo de Djsktra comecando da cidade de origem
    resultados = []  # Inicializa vetor de resultados
    # Para cada par de cidade que deseja calcular a distancia
    for cidades in problema["CidadesCalcularDistancia"]:
        try:
            # Calcula a distancia
            distancia = round(
                grafo.dijkstra(identificacao[cidades["CidadeOrigem"]])[identificacao[cidades["CidadeDestino"]]])
        except Exception:
            # Se der erro quer dizer que a distancia eh infinita, ou seja,
            # nao tem rota da cidade de origem ate a cidade de destino
            resultados.append("no route exists") # Adiciona a nao existencia de rota no problema
            continue # e repete o loop
        # Caso de certo, adiciona a distancia minima entre as cidade,
        # obtidas pelo algoritmo de Djsktra no vetor de resultados
        resultados.append(distancia)

    # Montar string de retorno de acordo com o problema
    retorno = f'Case #{indice_problema+1}\n'
    for resultado in resultados:
        if resultado == "no route exists":
            retorno += str(resultado) + "\n"
        else:
            retorno += str(resultado) + " km" + "\n"

    return retorno  # Retorna a solucao do problema formatada


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]
    for arquivo_de_teste in arquivos_de_teste:  # Para cada arquivo de teste
        tempo_inicial = time()  # Inicio a marcacao do tempo

        problemas = entrada(arquivo_de_teste)  # Le e imprime a entrada e retorna ela formatada
        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for indice, problema in enumerate(problemas):  # para cada problema
            resultado = resolve(problema, indice)  # resolve o problema
            print(resultado)  # E imprime o resultado na tela

        print()
        tempo_final = time()  # Para o tempo
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")  # imprime o tempo de execucao
        print("-" * 68)
