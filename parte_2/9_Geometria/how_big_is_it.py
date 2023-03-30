from time import time  # Funcao para computar o tempo computacional
from copy import deepcopy  # Funcao que vai gerar uma copia profunda de um objeto
from math import sqrt  # Funcao matematica que calcula a raiz quadrada


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

    # Ler quantidade de problemas
    qnt_problemas = int(dados[posicao])
    posicao += 1  # Avanca o ponteiro do arquivo

    problemas = []  # Inicializa o vetor de problemas

    # Para cada problema
    for _ in range(qnt_problemas):
        # Inicializando um problema
        # Cada problema possui em um linha, separado por espaco, a quantidade de circulos seguido dos raios dos circulos
        # Adiciona os raios dos circulos no problema transformando em numeros reais
        problema = [float(dado) for dado in dados[posicao].split(" ")[1:]]

        problemas.append(problema)  # Adiciona o problema no vetor de problemas

        posicao += 1  # Avanca o ponteiro do arquivo

    return problemas  # Retorna os problemas a serem resolvidos


def bissecao(ultimo_circulo_inserido, novo_circulo_a_ser_inserido):
    """ Essa funcao recebe dois Circulos (Centro e Raio),
        posicionados no plano, de maneira tal que, ambos toquem a mesma reta horizontal
        em um unico ponto abaixo deles (Fundo da caixa) e onde um acaba o outro
        termina, ou seja, um ao lado do outro, sem necessariamente se tocarem.
        Atraves do metodo da bissecao tenta-se deslocar o novo circulo a ser inserido
        de maneira que a distancia entre os centros seja igual ou bem proxima
        a soma dos raios, o que significa que eles agora vao ser tocar em um unico ponto."""

    # O limite inferior para a bissecao eh o x do centro do ultimo circulo inserido
    inf = ultimo_circulo_inserido["Centro"][0]
    # O limite superior para a bissecao eh x do centro onde ele esta inicialmente
    sup = novo_circulo_a_ser_inserido["Centro"][0]

    # Deve-se achar um deslocamento tal que a distancia entre os centros dos circulos seja igual
    # a soma dos raios

    while True:  # Loop infinito
        # A nova localizacao em X do circulo a ser inserido é
        # a metade do caminho entre o X do centro do ultimo circulo inserido e o X do centro atual
        novo_x = (inf + sup) / 2

        # Atualiza, por referencia(objeto), a localizacao do novo circulo
        novo_circulo_a_ser_inserido["Centro"][0] = novo_x

        # Calcula a distancia entre os centros do ultimo circulo inserido na caixa e o que vai ser inserido
        distancia = distancia_dois_pontos(
            {"x": ultimo_circulo_inserido["Centro"][0], "y": ultimo_circulo_inserido["Centro"][1]},
            {"x": novo_circulo_a_ser_inserido["Centro"][0], "y": novo_circulo_a_ser_inserido["Centro"][1]})

        # Calcula a soma dos raios entre o ultimo circulo a ser inserido e o novo circulo
        soma_dos_raios = (ultimo_circulo_inserido["Raio"] + novo_circulo_a_ser_inserido["Raio"])

        # Se a distancia entre os centros dos circulos e a soma dos raios for minima
        if abs(distancia - soma_dos_raios) < 0.000000001:
            # Entao o novo circulo a ser inserido esta com as coordenadas do centro certa
            break  # Portanto sai do loop

        elif distancia < soma_dos_raios:  # Caso a distancia entre os centro dos circulos for menor que a soma dos raios
            inf = novo_x  # Entao deve-se atualizar o limite inferior o qual o centro do novo circulo pode chegar
        elif distancia > soma_dos_raios:  # Caso a distancia entre os centro dos circulos for maior que a soma dos raios
            sup = novo_x  # Entao deve-se atualizar o limite superior o qual o centro do novo circulo pode chegar


def distancia_dois_pontos(p1, p2):
    """ Essa funcao recebe dois pontos no plano e calcula a distancia em linha reta entre eles"""
    return sqrt((p1["x"] - p2["x"]) ** 2 + (p1["y"] - p2["y"]) ** 2)


def inserir_circulo(circulos_inseridos, raio_circulo):
    """ Essa funcao recebe o vetor de circulos inseridos na caixa
    e o raio do novo circulo que sera inserido,
    e insere esse raio na caixa minimizando o espaço entre o ultimo circulo inserido
    e o novo circulo que vai ser inserido"""

    # Se o vetor de circulos inseridos for vazio
    # Entao eh a primeira iteracao
    # A Heuristica utilizada insere o primeiro circulo no centro
    # E ele sempre é o maior circulo dentre os passados no problema
    if circulos_inseridos == []:
        # Insere o maior circulo no centro do plano
        circulos_inseridos.append({"Centro": [0, 0], "Raio": raio_circulo})
        return  # Termina a funcao

    # Caso contrario deve-se inserir um circulo ao lado do outro
    # Ou seja, deve-se inserir o novo circulo ao lado do ultimo circulo ja inserido
    # Entao extrai o ultimo circulo já inserido e suas caracteristicas (Raio e posicao (x,y) do centro)
    ultimo_circulo_inserido = circulos_inseridos[-1]
    # Entao extrai o primeiro circulo já inserido e suas caracteristicas (Raio e posicao (x,y) do centro)
    # Isso eh feito pois o primeiro circulo eh o maior de todos
    primeiro_circulo_a_ser_inserido = circulos_inseridos[0]

    # O novo circulo a ser inserido tem o X do centro posicionado logo apos sair do centro do ultimo circulo
    # e ir para a beirada do circulo, ou seja, sair do centro do ultimo circulo e percorrer o raio
    # somado ao raio do circulo que sera inserido

    # O novo circulo a ser inserido tem o Y do centro posicionado abaixo do eixo X
    # e o valor de Y do centro do novo circulo eh -R + r
    # Onde R eh o raio do maior circulo e r eh o raio do circulo a ser inserido
    novo_circulo_a_ser_inserido = {
        "Centro": [ultimo_circulo_inserido["Centro"][0] + ultimo_circulo_inserido["Raio"] + raio_circulo,
                   -primeiro_circulo_a_ser_inserido["Raio"] + raio_circulo], "Raio": raio_circulo}

    # Realizar metodo da bissecao o qual vai encontrar as coordenadas
    # em X do novo circulo de maneira que toque em um unico ponto o circulo anterior já inserido
    # Obs: A posicao em Y do novo circulo se mantem fixa
    bissecao(ultimo_circulo_inserido, novo_circulo_a_ser_inserido)

    # Por fim insere-se esse novo circulo no vetor de circulos
    circulos_inseridos.append(novo_circulo_a_ser_inserido)


def resolve(problema):
    """
    Essa funcao recebe um problema.
    Essse problema eh composto por N raios de circulos,
    os quais devem ser colocados numa caixa um ao lado do outro encostando no fundo da caixa.
    Deve ser retornado a largura mínima dessa caixa de maneira que todos os circulos
    fiquem dentro dela.
    Obs: Obviamente a altura da caixa é o diâmetro do maior circulo.
    A ideia eh tentar inserir um circulo maior e depois um menor para minimizar a largura da caixa.
    O primeiro circulo eh inserido no centro do plano e o segundo na frente do primeiro, assim sucessivamente,
    ate inserir todos os circulos
    """
    # Obtem os raios do problema
    raios = deepcopy(problema)

    # Tenta-se inserir o maior e depois o menor circulo, sempre alternando entre eles
    vez = "Maior"
    # Inicializa o vetor de circulos inseridos o qual contem a localizacao do centro dos circulos inseridos
    # e seus respectivos raios
    circulos_inseridos = []
    while len(raios) != 0:  # Enquanto tiver circulo a ser inserido
        if vez == "Maior":  # Se for a vez de inserir o maior circulo
            raio_circulo = max(raios)  # Extrai o maior circulo do problema
            raios.remove(raio_circulo)  # E o remove
            vez = "Menor"  # Passa a vez para o menor circulo na proxima iteracao
        elif vez == "Menor":  # Se for a vez de inserir o menor circulo
            raio_circulo = min(raios)  # Extrai o menor circulo do problema
            raios.remove(raio_circulo)  # E o remove
            vez = "Maior"  # Passa a vez para o maior circulo na proxima iteracao

        # Agora deve-se inserir o circulo extraido do problema na caixa
        inserir_circulo(circulos_inseridos, raio_circulo)

    # O tamanho da caixa a projecao em x (ou seja y=0) da beirada da esquerda do primeiro circulo (Xc - R)
    # Onde Xc é o x do centro
    # Até o Xc + R do ultimo circulo
    # O resultado eh arredondado em 3 casa decimais
    resultado = f'{distancia_dois_pontos({"x": circulos_inseridos[0]["Centro"][0] - circulos_inseridos[0]["Raio"], "y": 0}, {"x": circulos_inseridos[-1]["Centro"][0] + circulos_inseridos[-1]["Raio"], "y": 0}) : .3f}'

    return resultado


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
