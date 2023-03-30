from time import time  # Funcao para computar o tempo computacional
from math import sqrt  # Funcao para calcular a raiz quadrada

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

    # Ler quantidade de problemas
    qntd_problemas = int(dados[0])

    # Inicializar vetor de problemas
    # Cada vetor de problemas é composto por um número que eh o numero de pinos disponiveis no jogo,
    problemas = []
    for i in range(1, qntd_problemas + 1):  # Para cada problema
        problemas.append(int(dados[i]))  # Adiciona a quantidade de pinos no vetor de problemas

    # Retorna o vetor de pinos da torre de hanoi
    return problemas


def resolve(qntd_pinos):
    """
        Essa funcao recebe a quantidade de pinos que torre de hanoi terah.
        Ela cria um grafo desconexo para cada pino.
        E para cada bola de 1 a N.
        Tenta-se encaixar no primeiro ramo do gafo (pino)
        Se o primeiro pino estiver vazio(nó 0 no grafo)
        entao a bola eh encaixada, caso contrario eh observado
        se a soma da bola a ser inserida com a ultima bola (vertice) inserida no subgrafo,
        resulta em um quadrado perfeito. Se sim a bola eh inserida.
        Caso a bola nao consiga ser inserida nesse ramo do grafo o processo
        se repete para os demais ramos (pinos).
        Caso nao consiga inserir a bola em nenhum ramo, entao eh retornado
        ate que numero de bola consegui-se inserir,
        Obs: caso o numero de bolas inseridas ultrapasse o quadrado do número
        de pinos, então é retornado -1, pois as bolas podem ser inseridas infinitamente.
    """

    # Inicialmente cria-se um grafo
    # Esse grafo eh um grafo desconexo formados por N subgrafos
    # A quantidade de subgrafos é N (quantidade de pinos)
    # Inicialmente esse subgrafo possuem somente um vertice
    # Esse vertice possui um rotulo 0
    grafo = [[0] for pino in range(qntd_pinos)]  # Iniciando o grafo

    # Apos a criacao do grafo deve-se tentar inserir as bolas a partir da numero 1
    bola = 1  # Primeira bola a ser inseria
    while True:  # Inicializa um loop infinito
        encaixou_bola = False  # E inicialmente a bola nao foi inserida
        for subgrafo in grafo:  # Para cada subgrafo(pino) no grafo
            if subgrafo[-1] == 0:  # Se ele possuir no ultimo vertice inserido, o vertice de inicializacao (vertice 0)
                subgrafo.append(bola)  # Entao eh adicionado a esse ramo(pino) a bola correspondente
                encaixou_bola = True  # Eh marcado que a bola foi inserida
                break  # E sai do loop "for" (loop de insercao de uma bola no grafo)
            # Caso o ramo nao esteja somente com o vertice de inicializacao
            # Entao eh conferirido se o ultimo vertice inserido somado com o valor da bola a ser inserida
            # Forma um quadrado perfeito
            # Para isso eh tirado a raiz quadrada da soma
            # E eh extraido atraves do operador "//" a parte inteira
            # Se a parte inteira do resultado da raiz for igual o proprio resultado da raiz
            # Entao o resultado da raiz quadrada da soma entre o ultimo vertice e a nova bola
            # Eh um quadrado perfeito
            elif sqrt(subgrafo[-1] + bola) // 1 == sqrt(subgrafo[-1] + bola):
                subgrafo.append(bola)  # Entao essa bola eh adicionada a esse ramo do grafo
                encaixou_bola = True  # E eh marcado que a bola foi encontrada
                break  # E sai do loop "for" (loop de insercao de uma bola no grafo)
        if not encaixou_bola:  # Apos sair do loop de insercao verifica-se se a ultima bola nao foi encaixada
            break  # Se nao foi sai do loop "while" pois nao eh possivel encaixar mais bolas
        elif bola > qntd_pinos ** 2:  # Caso a bola a ser inserida seja maior que o quadrado da quantidade de pinos
            return -1  # Entao pode-se inserir bolas infinitamente, entao eh retornado -1
        else:  # Caso a bola foi encaixada, e respeite o limite (nao esta inserindo infinitamente)
            bola += 1  # Entao tenta-se inserir a proxima bola

    # Ao sair do loop eh retornado a quantidade de bola que foram encaixadas
    # Lembrando que a variavel "bola" armazena a bola que nao inserida
    # E "bola -1" a quantidade que foi inserida
    return bola - 1


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]
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
