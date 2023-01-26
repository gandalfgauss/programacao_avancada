from time import time  # Biblioteca para marca o tempo computacional

# Uma solucao é um vetor de 13 posicoes,
# onde cada posicao representa uma categoria
# e cada valor é a rodada referente a categoria
# inicialmente a melhor solucao é um vetor de 0 a 12
melhor_solucao = list(range(13))


def entrada(nome_do_arquivo):
    """ Funcao que recebe o nome de um arquivo de entrada
     que vai computar a entrada do problema,
    e irah retornar os valores de entrada ajustados para o algoritmo"""

    # Ler dados do arquivo de Entrada
    with open(nome_do_arquivo, "r") as arquivo:
        dados = arquivo.readlines()

    # Imprimir dados de entrada na tela
    print("-" * 30, "Entrada:", nome_do_arquivo, "-" * 30)
    for dado in dados:
        print(dado, end="")
    print()

    jogos = []  # vetor de jogos

    # Armazenar jogos de 13 em 13 rodadas
    inf = 0
    sup = 13
    while inf < len(dados):
        # Para cada rodada em um jogo
        # Tranformar os valores da rodada em uma lista de inteiros
        jogo = []
        for rodada in dados[inf:sup]:
            jogo.append([int(dado) for dado in rodada.split(" ")])

        inf += 13
        sup += 13

        jogos.append(jogo)

    return jogos


def confere_ones(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 1's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 1:
            pontuacao += 1

    return pontuacao


def confere_twos(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 2's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 2:
            pontuacao += 2

    return pontuacao


def confere_threes(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 3's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 3:
            pontuacao += 3

    return pontuacao


def confere_fours(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 4's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 4:
            pontuacao += 4

    return pontuacao


def confere_fives(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 5's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 5:
            pontuacao += 5

    return pontuacao


def confere_sixes(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao de 6's'"""

    pontuacao = 0
    for dado in rodada:
        if dado == 6:
            pontuacao += 6

    return pontuacao


def confere_chance(rodada):
    """ Essa funcao recebe uma rodada e
    retorna a pontuacao total dos 5 dados"""

    return sum(rodada)


def confere_three_of_kind(rodada):
    """ Essa funcao recebe uma rodada
    e retorna a pontuacao como a soma dos
    valores dos 5 dados, se pelo menos 3
    valores sao iguais, caso contrario retorna 0"""

    for i in range(1, 7):  # Para os valores de 1 a 6
        if rodada.count(i) >= 3:  # Se aparecer pelo menos 3 vezes um valor
            return sum(rodada)  # Retorna a soma dos valores

    return 0  # Caso contrario retorna 0


def confere_four_of_kind(rodada):
    """ Essa funcao recebe uma rodada
    e retorna a pontuacao como a soma dos
    valores dos 5 dados, se pelo menos 4
    valores sao iguais, caso contrario retorna 0"""

    for i in range(1, 7):  # Para os valores de 1 a 6
        if rodada.count(i) >= 4:  # Se aparecer pelo menos 4 vezes um valor
            return sum(rodada)  # Retorna a soma dos valores

    return 0  # Caso contrario retorna 0


def confere_five_of_kind(rodada):
    """ Essa funcao recebe uma rodada
        e retorna a pontuacao como 50,
        se todos os 5 valores forem iguais"""

    # Se remover os elementos repetidos e sobrar 1 elemento
    # Quer dizer que todos os elementos eram iguais
    if len(set(rodada)) == 1:
        return 50  # Entao retorna 50 pontos

    return 0  # Caso contrario retorna 0 pontos


def confere_short_straight(rodada):
    """ Essa funcao recebe uma rodada
        e retorna a pontuacao como 25,
        desde que quatro dos dados formem uma sequencia,
        ou seja:
        [1,2,3,4]
        [2,3,4,5]
        ou [3,4,5,6]"""

    if 1 in rodada and 2 in rodada and 3 in rodada and 4 in rodada:
        return 25
    elif 2 in rodada and 3 in rodada and 4 in rodada and 5 in rodada:
        return 25
    elif 3 in rodada and 4 in rodada and 5 in rodada and 6 in rodada:
        return 25

    return 0


def confere_long_straight(rodada):
    """ Essa funcao recebe uma rodada
        e retorna a pontuacao como 35,
        desde que cinco dos dados formem uma sequencia,
        ou seja:
        [1,2,3,4,5]
        [2,3,4,5,6]
        """

    if 1 in rodada and 2 in rodada and 3 in rodada and 4 in rodada and 5 in rodada:
        return 35

    elif 2 in rodada and 3 in rodada and 4 in rodada and 5 in rodada and 6 in rodada:
        return 35

    return 0


def confere_full_house(rodada):
    """ Essa funcao recebe uma rodada
    e retorna 40 ponto desde que três
    dos dados sejam iguais e os outros
    dois dados também seja, caso cotrario
    retorna 0"""

    for i in range(1, 7):  # Para os valores de 1 a 6
        if rodada.count(i) >= 3:  # Se aparecer pelo menos 3 vezes um valor
            # Remover esses valores e conferir se aparecem dois valores iguais
            copia_rodada = rodada.copy()

            for _ in range(3):
                copia_rodada.remove(i)

            if len(set(copia_rodada)) == 1:
                return 40

    return 0


def confere_bonus(categoria_one_six):
    """ Essa funcao recebe a pontuacao
    do usuario na categoria de 1 a 6
    e retorna 35 pontos caso a soma
    nas categorias seja maior
    ou igual a 63.
    Caso contrario retorna 0"""

    if sum(categoria_one_six) >= 63:
        return 35

    return 0


def calcula_pontuacao_solucao_parcial(solucao, jogo):
    """ Essa funcao recebe uma solucao, seja parcial ou completa,
    e o jogo com 13 rodadas, e retorna a pontuacao estimada para aquele jogo
    dado a solucao em andamento"""

    pontuacoes = []  # declarado o vetor de pontuacoes, que vai conter a pontuacao de cada rodada

    # Vetor de funcoes, onde cada funcao eh uma categoria,
    # elas recebem uma rodada e retornam a pontuacao da mesma relativa a categoria(funcao) chamada
    funcoes = [confere_ones, confere_twos, confere_threes, confere_fours, confere_fives, confere_sixes,
               confere_chance, confere_three_of_kind, confere_four_of_kind, confere_five_of_kind,
               confere_short_straight, confere_long_straight, confere_full_house]

    # extrair as rodadas que nao sairam para realizar
    # a estimativa de pontuacao dentre as categorias restantes
    rodadas_nao_sairam = [rodada for rodada in range(13) if rodada not in solucao]

    # percorre-se o vetor de solucao
    # o qual o indice "i" indica a categoria
    # e o "valor" indica a rodada que aquela categoria vai ser aplicada
    # Obs: "_" dentro do vetor de solucao significa que
    # dali para frente nao foi calculada as rodadas das categorias
    for i, valor in enumerate(solucao):
        if valor == "_":  # se nao foi calculado a rodada da categoria i
            # Entao deve-se percorrer as rodadas que nao sairam
            # e colocar como uma pontuacao estimada a rodada que maxima a categoria
            pontuacoes.append(max([funcoes[i](jogo[x]) for x in rodadas_nao_sairam]))  # aplica a categoria a cada
            # rodada restante e extrai o valor maximo
        else:  # caso a rodada tenha sido escolhido para categoria
            pontuacoes.append(funcoes[i](jogo[valor]))  # basta adicionar a pontuacao daquela categoria no vetor de
            # pontuacao

    # apos definir e estimar as pontuacoes, eh adicionado tambem se o jogador recebe ou nao o bonus
    pontuacoes.append(confere_bonus(pontuacoes[:6]))

    return pontuacoes  # retorna as pontuacoes


def eh_viavel(solucao_atual, jogo):
    """ Essa funcao recebe uma solucao completa ou nao,
     e o jogo, ou seja as rodadas.
     Retorna se a solucao atual eh viavel, ou seja,
    se a solucao atual pode chegar a ser melhor que a melhor solucao atual,
    retorna True se verdadeiro, False caso contrario."""

    global melhor_solucao

    # Calcula a pontuacao relativa a solucao atual e a melhor solucao atual
    pontuacao_melhor_solucao = sum(calcula_pontuacao_solucao_completa(melhor_solucao, jogo))
    pontuacao_solucao_atual = sum(calcula_pontuacao_solucao_parcial(solucao_atual, jogo))

    if pontuacao_solucao_atual > pontuacao_melhor_solucao:
        return True

    return False


def eh_completa(solucao_atual):
    """ Essa funcao recebe uma solucao e retorna se ela eh completa ou nao.
    Ou seja, retorna True se todos as rodadas das categorias foram definidas,
    e False caso contrario"""
    return all([False if valor == "_" else True for valor in solucao_atual])


def calcula_pontuacao_solucao_completa(solucao, jogo):
    """ Essa funcao recebe uma solucao completa e as rodadas de um jogo,
    e retorna as pontucoes.
    Bem semelhante a funcao calcula_pontucao_solucao_parcial,
    porem nao precisa fazer estimativas."""

    pontuacoes = []
    funcoes = [confere_ones, confere_twos, confere_threes, confere_fours, confere_fives, confere_sixes,
               confere_chance, confere_three_of_kind, confere_four_of_kind, confere_five_of_kind,
               confere_short_straight, confere_long_straight, confere_full_house]
    for i, valor in enumerate(solucao):
        pontuacoes.append(funcoes[i](jogo[valor]))

    pontuacoes.append(confere_bonus(pontuacoes[:6]))

    return pontuacoes


def branch_and_bound(jogo, solucao_atual, categoria):
    """ Essa funcao recebe as 13 rodadas de um jogo,
    a solucao inicial, e a categoria a qual uma rodada
    sera inserida.
    Ela busca dentro das possibilidades, utilizando
    branch and bound para poda, uma solucao melhor que
    a melhor solucao atual,
    e atualizar o vetor de melhor solucao"""

    global melhor_solucao  # recebendo o vetor de melhor solucao atual

    if eh_completa(solucao_atual):  # se a solucao for completa
        # entao foi encontrado uma solucao melhor que a melhor solucao atual
        melhor_solucao = solucao_atual.copy()  # e o vetor de melhor solucao eh atualizado
    else:  # caso contrario
        for i in range(13):  # tenta-se atribuir as rodadas ("i") dentro da "categoria"
            if i not in solucao_atual:  # Desde que uma rodada nao tenha sido atribuida anteriormente (consistencia)
                solucao_atual[categoria] = i  # atribui-se a rodada a categoria
                # entao verifica-se a solucao atual (parcial ou completa) consegue ser melhor que a melhor solucao
                if eh_viavel(solucao_atual, jogo):
                    # Caso positivo, entao eh feita uma chamada recursiva para gerar a rodada da proxima categoria
                    branch_and_bound(jogo, solucao_atual, categoria + 1)
        solucao_atual[categoria] = "_"  # ao retornar limpa a rodada da categoria


def resolve_jogo(jogo):
    """ Essa funcao recebe um jogo com 13 rodadas e encontra a melhor solucao utilizando branch_bound.
    Retorna a solucao final com a pontuacao de cada categoria, bonus e pontucao final.
    Obs.: Caso nao seja percorrido todas as permutacoes, seriam 13! = 6.227.020.800 possibilidades,
    o que demoraria muito tempo dependendo do computador.
    Mas nos testes, o algorimto encontra a melhor solucao muito rapido, em alguns em menos de 1 segundo,
    o que indica que o algoritmo implementado funciona muito bem.
    """

    solucao_atual = list(13 * "_")  # inicial cada categoria contem "_" indicando que as rodadas nao foram escolhidas
    branch_and_bound(jogo, solucao_atual, 0)  # inicia o branch_bound
    solucao_final = calcula_pontuacao_solucao_completa(melhor_solucao, jogo)  # calcula a melhor solucao
    solucao_final.append(sum(solucao_final))  # adiciona no vetor de pontuacoes a soma das pontuacoes
    return solucao_final  # retorna a solucao de acordo com a saida do problema


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]  # Obs. Paciencia: o teste 2 demora 8 minutos.

    for arquivo_de_teste in arquivos_de_teste:
        tempo_inicial = time()
        jogos = entrada(arquivo_de_teste)

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for jogo in jogos:
            resultado = resolve_jogo(jogo)
            for valor in resultado:
                print(valor, end=" ")
            print()
        print()
        tempo_final = time()
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")
        print("-" * 68)
