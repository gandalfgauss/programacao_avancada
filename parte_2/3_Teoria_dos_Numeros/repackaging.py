from time import time  # Funcao para computar o tempo computacional
import math  # Pacote para calculos matematicos

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
    problemas = []  # Vetor de problemas

    quantidade_embalagens = int(dados[0])  # Inicialmente a quantidade de embalagens fica na posicao 0
    indice = 1  # Indice da entrada
    while quantidade_embalagens != 0:  # Enquanto a entrada nao tiver 0
        embalagens = [] # Vetor que armazena os tipos de embalagem
        for i in range(quantidade_embalagens):
            embalagens.append(list(map(int, dados[indice].split(" "))))  # Adiciona no vetor de embalagens uma embalagem como lista
            indice += 1  # acrescenta um no indice

        problemas.append(embalagens)
        quantidade_embalagens = int(dados[indice])
        indice += 1

    return problemas

def resolve(embalagens):
    """ Essa funcao recebe um lista com N embalagens
    no formato (S1, S2, S3), onde Si representa a quantidade
    de xicaras do tipo i, sendo entao 3 tipos de xicaras.
    Essa funcao retorna 'Yes' se eh possivel desenpacotar
     uma quantidade de cada embalgem de maneira que, sem sobrar,
     xicaras, elas podem ser juntadas em uma nova embalagem, com
     S1 = S2 = S3, caso nao seja possivel retorna 'No'.

    A solução é baseada em uma observação geométrica:
    se considerarmos cada pacote como um ponto no espaço tridimensional,
    com as coordenadas (S1, S2, S3), onde S1, S2 e S3 representam o número de copos de cada tamanho,
    então podemos desenhar um triângulo para cada pacote conectando as coordenadas.
    O problema se resume a determinar se é possível encontrar um ponto no espaço que seja equidistante
    de todos os vértices dos triângulos.
    Para resolver esse problema, podemos primeiro transformar cada triângulo em um vetor,
    calculando o ângulo que ele faz com um eixo arbitrário. O vetor correspondente a um triângulo é dado por:
        (S2 - S1, S3 - S1)

    Calculamos o ângulo em radianos entre cada par de vetores consecutivos
    e ordenamos esses ângulos em ordem crescente.
    Em seguida, encontramos o maior intervalo entre os ângulos consecutivos
    e verificamos se esse intervalo é maior que pi (o que significa que não há ponto equidistante).
    Se o intervalo for menor ou igual a pi,
    podemos encontrar um ponto equidistante usando a média dos pontos dos triângulos.

    Implementacao em c++ no link: https://github.com/morris821028/UVa/blob/master/volume100/10089%20-%20Repackaging.cpp
    """

    A = []
    for embalagem in embalagens:
        S1, S2, S3 = embalagem
        A.append(math.atan2(S2 - S1, S3 - S1))

    A.sort()
    gap = 0
    n = len(A)
    for i in range(1, n):
        gap = max(gap, A[i] - A[i - 1])
    gap = max(gap, 2 * math.pi - (A[n - 1] - A[0]))

    if gap > math.pi:
        return "No"
    else:
        return "Yes"

if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]  # Vetor de arquivos de teste
    for arquivo_de_teste in arquivos_de_teste:  # Para cada arquivo de teste
        tempo_inicial = time()  # Inicio a marcacao do tempo

        problemas = entrada(arquivo_de_teste)  # Le e imprime a entrada e retorna ela formatada

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for problema in problemas:  # para cada problema
            resultado = resolve(problema)  # resolve o problema
            print(resultado)  # E imprime o resultado na tela

        print()
        tempo_final = time()  # Para o tempo
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")  # imprime o tempo de execucao
        print("-" * 68)
