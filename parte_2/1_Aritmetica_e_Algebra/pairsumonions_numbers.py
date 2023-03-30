from time import time  # Funcao para computar o tempo computacional
from itertools import combinations  # Funcao para trabalhar com combinacoes
import numpy as np


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
    linhas = []  # Vetor de linhas
    for linha in dados:  # Para cada linha da entrada
        linha = [int(valor) for valor in linha.split(" ")]  # Transforma os valores em inteiros
        linhas.append((linha[0], linha[1:]))  # Adiciona o par (N, vetor de somas) no vetor de linhas

    return linhas  # Retorna todas as linhas do problema


def resolve(linha):
    """ Essa funcao recebe uma linha do problema contendo
    uma quantidade de números N e um vetor de inteiros.
     Retorna N números em ordem crescente
     que se somados de 2 em 2 resultam em todos os
     inteiros (somas) recebido no vetor de parametros"""

    N = linha[0]  # Recebe uma quantidade de numeros que devem ser retornados
    somas = linha[1]  # Recebe o vetor de inteiros (somas de 2 em 2)

    # Montar Sistema Linear
    b = np.asarray(somas.copy())  # O vetor de somas jah eh o vetor B
    # Falta montar a matriz A
    A = []
    combinacoes = list(combinations(range(1, N + 1), 2))  # Combinar as variaveis X1, X2, ..., Xn de 2 em 2
    for combinacao in combinacoes:
        linha = [0] * len(b)  # Linha que sera inserida na matriz, Obs: fazendo a matriz A ser quadrada
        for variavel in combinacao:
            linha[variavel - 1] = 1  # o coeficiente que acompanha as variaveis tem que ser 1
        A.append(linha)  # a linha eh adicionada a matriz A
    A = np.asarray(A)

    # Lembrando que: A ideia eh que X1 + X2 sejam iguais a primeira soma passada como argumento
    # X1 + X3 = segunda soma, e assim por diante.
    # Ao resolver o sistema linear, serah descoberto as variaveis que satisfazem aquelas somas em pares
    # Portanto descoberto a solucao do problema
    # Se o sistema nao tiver solucao, entao eh impossivel

    # Resolver sistema linear
    try:
        x = np.linalg.solve(A, b)  # resolve o sistema linear e armazena no vetor X
    except Exception: # Caso de erro, quer dizer que o sistema nao tem solucao ou tem infinitas solucoes
        try:
            x, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None) # Tenta pegar uma solucao das infinitas
        except Exception: # Se lancar uma excecao que dizer que o sistema nao tem solucao
            return "Impossible"  # entao retorna impossivel

    x = x[0:N]  # pegar somente o valor das variaveis do problema, sem as variaveis extras colocada para matriz ser
    # quadrada
    # Conferir se a solucao de X eh inteira
    if not np.allclose(x, np.rint(x)):  # Agora deve ser conferido se a solucao eh inteira
        return "Impossible" # Se nao for retorna impossibel

    # Se for
    return " ".join(sorted([str(round(n)) for n in x]))  # Eh retornado a solucao ordenada


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]  # Vetor de arquivos de teste
    for arquivo_de_teste in arquivos_de_teste:  # Para cada arquivo de teste
        tempo_inicial = time()  # Inicio a marcacao do tempo

        linhas = entrada(arquivo_de_teste)  # Le e imprime a entrada e retorna ela formatada

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for linha in linhas:  # para linha do problema
            resultado = resolve(linha)  # resolve o problema
            print(resultado)  # E imprime o resultado na tela

        print()
        tempo_final = time()  # Para o tempo
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")  # imprime o tempo de execucao
        print("-" * 68)
