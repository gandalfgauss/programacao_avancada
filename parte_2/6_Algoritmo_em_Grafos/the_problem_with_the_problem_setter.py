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
    problemas = []  # Inicializa vetor de problemas

    while "0" not in dados[posicao]:  # Enquanto nao tiver 0 no dado
        problema = []  # Inicializa o vetor para um problema de entrada

        # Obtem o numero de categorias e numero de problemas
        numero_de_categorias, numero_de_problemas = [int(dado) for dado in dados[posicao].split(" ")]
        problema.append([numero_de_categorias, numero_de_problemas])  # Adiciona-os no vetor de problema
        posicao += 1  # Aumenta um na posicao de leitura dos dados

        # Obtem a quantidade problemas que cada categoria deve ter
        problemas_por_categoria = [int(dado) for dado in dados[posicao].split(" ")]
        # Adiciona no vetor de problema, a quantidade de problemas por categoria
        problema.append(problemas_por_categoria)
        posicao += 1  # Aumenta um na posicao de leitura dos dados

        for _ in range(numero_de_problemas):  # Para cada problema
            # Adiciona as categorias desse problema no vetor de problema
            problema.append([int(dado) for dado in dados[posicao].split(" ")][1:])
            posicao += 1  # Aumenta um na posicao de leitura dos dados

        problemas.append(problema)  # Adiciona o problema no vetor de problemas

    return problemas  # Retorna os problemas que devem ser resolvidos


def resolve(problema):
    """
    Essa funcao recebe um problema.
    O problema baseia-se em um concurso de programação.
    E nesse concurso existem diversos problemas.
    E cada problema esta classificado em uma ou mais categorias.
    Recebendo a quantidade de categorias que existem,
    a quantidade de problemas na base de dados,
    as categorias de cada problema,
    e a quantidade de problemas que cada categoria deve ter nessa maratona de programacao,
    deve-se obter quais problemas vao ser atribuidos as categorias,
    de maneira esses problemas nao aparecam mais de uma vez em cadd categoria,
    ou seja, o mesmo problema nao aparece duas vezes na maratona.
    A saida deve se 0 caso nao haja solucao,
    e 1 caso haja solucao
    seguido dos problemas atribuidos a cada categoria.

    Para resolver o problema primeiro foi calculado a quantidade de cada
    problemas por categoria armazenando num grafo.
    E depois foi observado qual a raridade das categorias, ou seja,
    quantas em quantos problemas cada categorias aparece no concurso.
    Entao, para escolher o problema a ser atribuido a categoria
    escolhe-se o que representa a menor raridade, ou seja, que possui
    uma categoria que aparece mais vezes.

    Segue o passo a passo abaixo:
    """

    # Obter a quantidade de categoria e a quantidade de problemas do problemas
    quantidade_de_categorias, quantidade_de_problemas = problema[0]

    # Obter a quantidade de problemas que devem ser escolhidos por cada categoria
    quantidade_de_problemas_por_categoria = problema[1]

    # Obter as categorias de cada problema
    categorias_por_problemas = problema[2:]

    # Agora deve-se obter o inverso da linha de codigo acima
    # Deve-se obter os problemas de cada categoria

    # Atribuir problemas a categorias

    # Cria-se um grafo de N ramos
    # Onde cada ramo possui um vertice que representada cada categoria
    # E sao criados outros vertices ligados aos vertices das categorias
    # Eles representam os problemas ligados as categorias
    problemas_por_categoria = {i + 1: [] for i in range(quantidade_de_categorias)}
    # Para cada problema
    for indice_problema, categorias in enumerate(categorias_por_problemas):
        for categoria in categorias:  # E para cada categoria do problema
            problemas_por_categoria[categoria].append(indice_problema + 1)  # O problema eh adicionado no grafo

    # Agora deve-se contar quantos problemas cada categoria possui
    quantidade_de_problemas_por_categoria_real = [[categoria + 1, 0] for categoria in range(quantidade_de_categorias)]
    for categoria in range(quantidade_de_categorias):  # Para cada categoria
        # A quantidade de problemas relacionado a aquela categoria eh simplesmente o numero
        # de vertices de cada ramo
        quantidade_de_problemas_por_categoria_real[categoria][1] = len(problemas_por_categoria[categoria + 1])

    # Apos obter a quantidade de problemas que cada categoria possui
    # Deve-se ordenar por de maneira decresnte esse vetor
    quantidade_de_problemas_por_categoria_real.sort(key=(lambda x: x[1]), reverse=True)

    # Isso eh feito no intuito de obter as categorias mais raras
    # Ou seja, as categorias de problemas que menos aparecem
    raridade_das_categorias = {}  # Inicializa o dicionario de raridade de categorias
    # E para cada categoria
    for raridade, categoria in enumerate(quantidade_de_problemas_por_categoria_real):
        # Eh atribuido uma raridade
        # Sendo a mais frequente com raridade 0
        # A segunda mais frequente com raridade 1
        # A assim por diante
        raridade_das_categorias[categoria[0]] = raridade

    # Calculado a raridade de cada categoria
    # E sabendo que problemas possuem N categorias
    # Deve-se determinar a raridade de um problema
    # Um problema eh raro se possui pelo menos uma categoria rara
    # Nao importa se possui categorias menos raras
    raridade_problemas = []  # Inicializa o vetor de raridade
    for categorias in categorias_por_problemas:  # Para cada conjunto de categoria de um problema
        # Eh calculado a raridade maxima desse conjunto
        # E entao o problema possui esta raridade
        raridade_problemas.append(
            raridade_das_categorias[max(categorias, key=(lambda categoria: raridade_das_categorias[categoria]))])

    # Inicializa o dicionario de solucao
    solucao = {i + 1: [] for i in range(quantidade_de_categorias)}

    # Agora deve-se tentar atribuir a cada quantidade de categorias requerida
    # os seus respectivos problemas
    # Para cada categoria e a quantidade requerida de problemas nessa categoria
    for categoria, quantidade_problemas_nessa_categoria in enumerate(quantidade_de_problemas_por_categoria):
        categoria = categoria + 1  # Configurando o rotulo da categoria ja que comeca do 1
        # Para cada quantidade de problemas que essa categoria deve ter
        # Tenta-se encaixar um problema
        for _ in range(quantidade_problemas_nessa_categoria):
            # Para encaixar um problema em determinada categoria
            # Deve-se procurar os problemas candidatos
            # Que sao justamentes os vertices(problemas) que estao ligados a aquela categoria
            vertices_candidatos = problemas_por_categoria[categoria]

            # Se nao tiver nenhum candidato entao o problema nao tem solucao
            if vertices_candidatos == []:
                return 0  # Entao retorna 0

            # Agora deve-se encontrar o melhor vertice para ser atribuido a aquela categoria
            # Que eh o que possui a menor raridade
            melhor_vertice = min(vertices_candidatos, key=(lambda vertice: raridade_problemas[vertice - 1]))

            # Apos encontrar o melhor vertice (problema)
            # Ele deve ser removido do grafo
            for cat in range(quantidade_de_categorias):
                if melhor_vertice in problemas_por_categoria[cat + 1]:
                    problemas_por_categoria[cat + 1].remove(melhor_vertice)

            # E eh adicionado ao vetor de solucao
            solucao[categoria].append(melhor_vertice)

    # Monta a string de retorno com base no problema
    string_de_retorno = "1\n"  # Retorna o 1 de sucesso
    for categoria in solucao.keys():  # Para cada categoria na solucao
        for problema in solucao[categoria]:  # Adiciona a string de retorno os problemas atribuidos
            string_de_retorno += str(problema) + " "
        string_de_retorno += "\n"

    return string_de_retorno[:-1]  # Retorna sem o \n final


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
