from time import time  # Funcao para computar o tempo computacional
from math import ceil  # Funcao para arredondar para cima


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
    pares = []  # Vetor de pares de numeros
    for par in dados[1:]:  # Para cada par de numero
        par = [int(valor) for valor in par.split(" ")]  # Transforma os valores em inteiros
        pares.append((par[0], par[1]))  # Adiciona o par (X, Y) no vetor de pares

    return pares  # Retorna os pares de numero X e Y do problema


encontrou = False  # Variavel de controle que infdica se encontrou ou nao a solucao para o problema


# Essa funcao varre o espaco de busca e funciona corretamente
def search(inf, x, y, step, step_anterior, solucoes, passos_dados):
    """ Essa funcao recebe um limite inferior, do qual,
    partindo o mesmo deve-se chegar a y,
    o tamanho do salto atual(step), o tamanho do salto anterior,
    o vetor de solucao unica, e a quantidade de passos dados.
    Apos encontrar a melhor solucao, ou seja, a quantidade minima
    de passos para chegar de inf a y, ela eh retorna por referencia
    dentro do vetor de solucoes"""

    global encontrou  # Variavel global de controle
    if not encontrou:  # Se nao encontrou a melhor solucao (menor numero de passos)
        if inf == y:  # Se o limite inferior atingir y
            if step_anterior == 1:  # E na etapa anterior o passo foi 1
                solucoes.append(passos_dados)  # entao foi encontrada a melhor solucao
                encontrou = True  # Marca que a melhor solucao foi encontrada
        elif inf < y:  # Caso contrario, se o limite inferior ainda nao ultrapassou e y
            if inf + step <= (x + y) // 2:  # Caso nao tenha ultrapasse a metade do caminho
                search(inf + step, x, y, step + 1, step, solucoes,
                       passos_dados + 1)  # Faz a busca aumentando o tamanho do salto(step) em 1

            search(inf + step, x, y, step, step, solucoes,
                   passos_dados + 1)  # Faz a busca aumentando mantendo constante o tamanho do salto(step)
            if step - 1 > 0:  # E se diminuir o tamanho do salto nao o deixa <= 0
                search(inf + step, x, y, step - 1, step, solucoes,
                       passos_dados + 1)  # Faz a busca diminuindo o tamanho do salto(step) em 1
    # Obs: ao varrer o espaco de solucoes o algoritmo tenta sempre ir avancando em 1 o salto
    # Caso nao consiga tenta manter o passo constante
    # E por ultimo diminuir o passo
    # Entao a primeira solucao encontrada, com certeza eh a melhor solucao para o problema
    # Tendo um melhor desempenho cortando o espaco de combinacoes


# Essa funcao foi uma segunda versao usando PA,
# Quase funciona erra por 1 as vezes, deve ser estudada para generalizar
def search2(x, y, solucoes):
    """ Essa funcao recebe o valor de x e y, e retorna uma solucao
    , por referencia, a qual se refere ao menor numero de passos
    indo de x a y

        Exemplo: X=2 e Y = 20
    2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20

    Sabendo que os passos devem aumentar para o caminho ser minimo
    E deve chegar ate a metade
    (2+20)/2 = 11

    Partindo do 2 para chegar ao 11 sao 11-2 = 9 unidades
    Ou seja, aumentando o numero de passos

    Outra forma: (20-2)/2 = 9

    logo:
    1+2+3+4+...+ n <= 9

    Sendo uma PA de razao 1

    (1+an)*n/2 <= 9
    (1+an)*n <= 18

    an = a1+(n-1)*r
    an = 1+(n-1)*1
    an = 1+ n -1
    an = n

    (1+n)*n <= 18

    n2 + n - 18 <= 0
    n = 3.772 ou n = -4.772
    Considerando n como natural
    n = 3

    Ou seja, em 3 passos chaga-se quase na metade
    Depois eh necessario diminiur os passos

    logo 1+2+3+..+n -> em 3 passos chegam na metade
    ou seja, os passos sao de 1+2+3, pois n = 3 para chegar na metade
    e foram percorrida 1+2+3= 6 unidades

    basta repetir a equacao a partir daí
    Se queremos ir de 2 a 20.
    E em 3 passos chegamos a metade percorrendo 1+2+3= 6 unidades
    Ou seja ainda faltam 20 - 2 - 6 = 12 unidades para ser percorridas

    Repetindo a equacao sabe-se que 1+2+3+4+...+n <= 12

    logo (1+n)*n/2 <= 12
    n^2 + n -24 <=0

    Resolvendo a expressao acima
    n = 4.42 ou n = -5.42

    Nessa segunda parte eh necessario se atentar a um detalhe
    n=4.42
    Esses 0.42 a mais significa um passo a mais de tamanho menor que deve ser dado
    entao n = 5

    Somando as solucoes 3 e 5 do sitemas acima, resulta em 8, ou seja,
    São necessários 8 passos para ir de 2 ate 20.

    """
    if y - x == 0:  # Se a diferenca entre os numeros for 0
        return solucoes.append(0)  # Entao nao precisa de passo algum
    elif y - x == 1:  # Se for 1, precisa de 1 passo
        return solucoes.append(1)
    elif y - x == 2:  # Se for 2, precisa de 2 passos
        return solucoes.append(2)
    else:
        # Montar equacao do segundo grau para ser resolvida
        a = 1
        b = 1
        c = None

        # Calcular o valor de c
        # Que eh justamente a -2*d -> onde 'd', inteiro, é a distancia de x até a metade do caminho de y
        # d = (x+y)/2 -x = x/2 + y/2 -x = y/2 -x/2 = (y-x)/2
        d = (y - x) // 2
        c = -2 * d

        # Resolver a equacao do segundo grau a*x^2 + b*x + c = 0
        D = (b ** 2 - 4 * a * c)  # Delta
        x1 = (-b + D ** (1 / 2)) / (2 * a)  # X1
        x2 = (-b - D ** (1 / 2)) / (2 * a)  # X2

        # Atribuir metade do caminho a solucao positiva
        solucao = max(x1, x2)
        solucao1 = int(solucao)

        # Fazer a mesma coisa para o restante do caminho
        # Montar equacao do segundo grau para ser resolvida
        c = None

        # Calcular o valor de c
        # Que eh justamente a -2*d -> onde 'd', inteiro, é a distancia entre y e ate onde ja foi chegado
        d = y - x - (1+solucao1)*solucao1/2  # sum(range(1, solucao1 + 1))
        c = -2 * d

        # Resolver a equacao do segundo grau a*x^2 + b*x + c = 0
        D = (b ** 2 - 4 * a * c)  # Delta
        x1 = (-b + D ** (1 / 2)) / (2 * a)  # X1
        x2 = (-b - D ** (1 / 2)) / (2 * a)  # X2

        solucao = max(x1, x2)
        solucao2 = ceil(solucao)  # Lembrar de arredondar para cima a solucao 2, por conta do passo a mais

        solucoes.append(int(solucao1 + solucao2))


def resolve(par):
    """ Essa funcao recebe um par de numeros, X e Y, tais que  X<=Y,
    do problema e retorna a quantidade mínima de passos para ir de X a Y,
     tendo que sair de X em 1 unidade e chegar em Y em 1 unidade,
     e podendo caminhar 1 a mais, a menos ou a mesma quantidade a cada passo"""

    # Recebendo X e Y
    x = par[0]  # Recebendo x
    y = par[1]  # Recenbo y

    step = 1  # Inicial a etapa inicial eh 1, ou seja vai de x a x+1 com 1 passo
    inf = x  # Inicialmente inicia o algoritmo do valor X
    solucoes = []  # Vetor de solucao unica, so para salvar como referencia

    global encontrou  # Variavel global booleana de controle que indica se achou ou nao a solucao para o problema
    encontrou = False  # Inicialmente nao foi encontrada solucao
    # search(inf, x, y, step, 1, solucoes, 0)  # Inicia a busca pelo espaco de solucao
    search2(x, y, solucoes)  # Inicia a busca pelo espaco de solucao
    return solucoes[0]  # Apos a busca retorna a soucao encontrada


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt", "teste3.txt"]  # Vetor de arquivos de teste
    for arquivo_de_teste in arquivos_de_teste:  # Para cada arquivo de teste
        tempo_inicial = time()  # Inicio a marcacao do tempo

        pares = entrada(arquivo_de_teste)  # Le e imprime a entrada e retorna ela formatada

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for par in pares:  # para cada par
            resultado = resolve(par)  # resolve o problema
            print(resultado)  # E imprime o resultado na tela

        print()
        tempo_final = time()  # Para o tempo
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")  # imprime o tempo de execucao
        print("-" * 68)
