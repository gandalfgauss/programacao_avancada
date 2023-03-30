from time import time  # Funcao para computar o tempo computacional


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

    quantidade_de_problemas = int(dados[posicao])  # Obtem a quantidade de problemas
    posicao += 2  # Pula o dado ja lido e o \n da entrada

    # Inicializa o vetor que conteram os problemas
    # Ou seja, a distancia ate a cidade grande,
    # e os postos de gasolinas com sua respectiva distancia do ponto de partida e o preco da gasolina
    problemas = []

    for i in range(quantidade_de_problemas):  # Para cada problema
        problema = []  # Inicializa o vetor de problemas

        # Le a distancia da cidade de partida ate a cidade de origem(cidade grande)
        distancia_da_cidade_grande = int(dados[posicao])
        problema.append(distancia_da_cidade_grande)  # Adiciona essa distancia no problema
        posicao += 1  # Adiciona um na posicao de leitura dos dados

        # Obter informacoes sobre os postos de gasolina no caminho
        while dados[posicao] != "\n":  # Enquanto o dado nao for "\n"
            # Obtem a distancia do posto de gasoliina do local de partida
            # E o preco da gasolina nesse posto
            distancia_posto, preco_gasolina = [int(dado) for dado in dados[posicao].split(" ")]
            # Adiciona as informacoes sobre o posto no problema
            problema.append([distancia_posto, preco_gasolina])
            posicao += 1  # Adiciona um na posicao de leitura dos dados

        posicao += 1  # Adiciona um na posicao de leitura dos dados

        problemas.append(problema)

    return problemas  # Retorna os problemas que devem ser resolvidos


def resolve(problema):
    """
    Essa funcao recebe um problema.
    O problema baseia-se em um caminhao de mudanca com um tanque de capacidade de 200 litros
    e parte de uma cidade inicial para uma cidade grande com um tanque na metade.
    Essa caminhao faz 1km por litro.
    E para nao pagar taxa para empresa que emprestou o caminhao ele deve chegar na
    cidade com o tanque na metade, do jeito que estava inicialmente.
    No caminho existem varios postos de gasolina.
    O objetivo eh falar se eh possivel ou nao chegar na cidade de destino,
    com o tanque de gasolina na metade, partindo da cidade de origem,
    E se for possivel deve ser retornado o quanto sera gasto de gasolina.

    Para resolver o problema serah utilizado programacao dinamica:

    Segue o algoritmo abaixo:
    """

    # Obtem-se do problema a distancia da cidade original ate a cidade de destino
    distancia_da_cidade_de_partida = problema[0]

    # Cria um vetor de tuplas
    # Onde cada tupla possui: a distancia entre a ponto em questao e cidade de origem e o valor da gasolina no ponto
    # Inicialmente, o primeiro ponto é [0,0]
    # Ou seja, eh a cidade de origem, com distancia entre ela mesmo de 0, e 0 no preco da gasolina pois nao eh posto
    distancia_postos_e_preco_gasolina = [[0, 0]]
    # Depois eh adicionado os outros postos no caminho
    distancia_postos_e_preco_gasolina.extend(problema[1:])
    # Por fim eh adicionado a cidade de destino
    # Cuja distancia da cidade de origem eh passado pelo problema acim
    # E o preco da gasolina eh considerado infinito
    distancia_postos_e_preco_gasolina.append([distancia_da_cidade_de_partida, float("INF")])

    # Depois eh criado a matriz dp de memorizacao para o programacao dinamica
    # A qual possui i linhas (cada linha representa um ponto)
    # E j colunas (de 0 a 200) que representa o valor da gasolina no veiculo
    # E dp[i][j] representa o custo minimo de chegar na cidade i com o valor de gasolina j
    # Inicialmente todos os valores da matriz sao infinitos
    # O que indica um custo infinito em cada d[i][j]
    # O que representa uma impossibilidade de chegar em i com gasolina j
    dp = [[float("INF")] * 201 for _ in range(len(distancia_postos_e_preco_gasolina))]

    # Inicialmente o custo de chegar na cidade inicial e com 100 de gasolina eh 0
    # Pois, segundo o problema, o veiculo comeca com 100 de gasolina na cidade inicial
    dp[0][100] = 0

    # Depois deve-se preencher a matriz de memorizacao com o custo minimo
    # Para cara parada a partir do primeiro posto de gasolina
    for indice, parada in enumerate(distancia_postos_e_preco_gasolina[1:]):
        indice = indice+1 # Atualiza o indice para representar o indice correto no vetor

        # Eh extraido da parada a distancia da cidade inicial e o preco da gasolina nessa parada
        distancia_parada, preco_gasolina = parada

        # Em seguida eh calcula a distancia da parada atual ate a parada anterior
        distancia = distancia_parada - distancia_postos_e_preco_gasolina[indice - 1][0]

        # Eh atualizado os custos
        for j in range(distancia, 201):
            # O custo de chegar na parada atual eh o minimo entre:
            # O custo de estar nessa parada e o custo de estar na parada anterior
            # com gasolina para ir para a proxima parada
            dp[indice][j - distancia] = min(dp[indice][j - distancia], dp[indice - 1][j])

        # Por fim
        for j in range(1, 201):
            # O custo de chegar na parada atual com gasolina j
            # Eh o minimo entre:
            # chegar na parada atual com gasolina j
            # e chegar na parada atual com gasolina j-1 e colocar uma unidade de gasolina
            dp[indice][j] = min(dp[indice][j], dp[indice][j - 1] + preco_gasolina)


    # O resultado final é o menor custo de ter chegado na ultima cidade([-1])
    # com gasolina pelo menos a metade do tanque, ou seja, de 100 até 200
    resultado = min(dp[-1][100:])

    if resultado == float("INF"):  # Se o resultado for infinito
        return "Impossible"  # Entao eh impossivel e eh retornado Impossible
    else:
        return resultado  # Caso contrario eh retornado o resultado


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
