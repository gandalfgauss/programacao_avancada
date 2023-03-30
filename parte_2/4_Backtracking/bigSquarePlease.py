from time import time  # Funcao para computar o tempo computacional
import copy  # Funcao para gerar uma copia de objetos


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
    # Cada vetor de problemas é composto por um número que eh o lado do quadrado de papel que deseja-se formar,
    # atraves de pedacos menores
    problemas = []
    for i in range(1, qntd_problemas + 1):  # Para cada problema
        problemas.append(int(dados[i]))  # Adiciona o lado do quadrado que deseja-se formar no vetor de problemas

    # Retorna o vetor de problemas contendo os lados dos quadrados que deseja-se formar atraves de pedacos menores
    return problemas


# Esse vetor armazenara a melhor solucao ate o momento
# Cada posicao do vetor eh composto por (i,j,l)
# Onde i e j são as coordenadas no ponto superior esquerdo do quadrado dentro da matriz
# E l é o lado do quadrado inserido dentro da matriz.
melhor_solucao = []

# Já esse vetor armazena a solucao atual ate o momento e os dados dentro dele sao (i,j,l) também.
solucao_atual = []


def matrizEhCompleta(matriz_N):
    """ Essa função recebe uma matriz de tamanho NXN, onde N é
    o tamanho do quadrado que deseja-se formar.
    Cada posicao dessa matriz representa um espaço para um quadrado de tamanho 1.
    Ou seja, cada posicao da matriz representa um quadrado de lado 1.
    Essa matriz contém inteiros, dentro dela.
    Se um elemento da matriz for 0, quer dizer que há um espaço no local,
    se for diferente de 0 quer dizer que a posição está ocupada por outro quadrado.
    Essa função retorna se a matriz está completa ou não (True ou False).
    Sendo verdadeiro se o quadrado maior que deseja-se forma está todo preenchido,
    e falso caso contrario."""
    nao_tem_zeros = all([0 not in linha for linha in matriz_N])  # Verificando se todas as linhas nao contem 0
    return nao_tem_zeros  # Retorna verdadeiro ou falso


def tentaEncaixar(matriz_N, lado):
    """ Essa função recebe a matriz NXN (quadrado maior) do problema
    e o lado do quadrado que deseja-se encaixar dentro dela.
    Ela tenta encaixar o quadrado de lado passado como parâmetro dentro da matriz.
    Caso consiga encaixar é retornado True, (i,j,l), nova_matriz
    onde True representa que foi possível encaixar, (i,j,l) representa
    as posicao do topo superior esquerdo da matriz e o lado l do quadrado encaixado,
    e nova_matriz representa a matriz_N com o quadrado encaixado dentro dela.
    Caso não seja possível encaixar o quadrado em nenhum lugar da matriz é retornado
    False, None, [].
    """

    # Gera uma cópia da matriz_N do problema com os quadrados encaixados ate entao
    nova_matriz = copy.deepcopy(matriz_N)

    # Deve-se tentar encaixar o quadrado de determinado "lado" nessa nova_matriz
    for i in range(len(matriz_N)):  # Para cada posicao i de indice de linhas da matriz original
        for j in range(len(matriz_N[0])):  # Para cada posicao j de indice de colunas da matriz original
            if matriz_N[i][j] == 0:  # Verifica se a posicao atual está vazia, ou seja, nenhum quadrado a ocupa
                # Se verdadeiro tenta encaixa esse quadrado nessa posição

                # Entao eh gerado uma cópia da matriz que deseja-se inserir o quadrado
                # com determinado ladona posicao (i,j)
                nova_matriz_tentativa = copy.deepcopy(nova_matriz)

                try:  # Entao eh feito a seguinte rotina para encaixar o quadrado
                    for posicaoX in range(i, i + lado):  # Para cada posicao em linhas que o quadrado ira ocupar
                        for posicaoY in range(j, j + lado):  # Para cada posicao em colunas em que o quadrado ira ocupar
                            if matriz_N[posicaoX][posicaoY] == 0:  # Se a posicao estiver vazia
                                # Entao insere um quadradinho de lado 1 dentro da matriz
                                # Obs: Esse algoritmo insere um quadrado de tamanho 1 por vez ate completar o
                                # quadrado que deseja-se inserir
                                nova_matriz_tentativa[posicaoX][posicaoY] = lado
                            else:  # Caso a seja acessado uma posicao já ocupada por outro quadrado
                                raise ValueError("Acessando posicao ocupada")  # Eh lançado uma exceção
                    # Caso consiga inserir todo o quadrado dentro da matriz, entao a nova matriz recebe a matriz
                    # que foi alterada, ou seja, a matriz que tentou inserir o quadrado e deu certo
                    nova_matriz = copy.deepcopy(nova_matriz_tentativa)
                    # E eh retornado que deu certo (True), a posicao do topo superior esquerdo do quadrado inserido
                    # e seu lado (i,j, lado), e a nova matriz (matriz com o novo quadrado encaixado.
                    return True, (i, j, lado), nova_matriz
                except Exception:  # Caso receba uma excecao
                    # O que pode acontece devido ao acesso a uma posicao invalida, ou seja,
                    # tentando criar um quadrado maior que os limites da matriz
                    # Ou pode acontecer devido esta sendo acessada a um posicao ocupada por outro quadrado
                    # Entao tenta-se encaixar o quadrado em outra posicao livre, proseguindo com o loop
                    continue
    # Caso saia do loop quer dizer que nao tem posicao valida, entao nao tem como encaixar o quadrado na matriz
    return False, None, []


def backtracking(matriz_N, lado):
    """ Essa funcao recebe a matriz que deseja-se encaixar os quadrados
    e o lado maximo do quadrado que tem-se em mãos para inserir dentro da matriz.
    Atraves do backtracking (recursivo) tenta-se varrer o espaço de solucoes em busca
    da quantidade minima de quadrado que preencha a matriz."""

    global melhor_solucao  # Obtem o vetor global de melhor solucao
    global solucao_atual  # Obtem o vetor global de solucao atual

    # Se a solucao atual for menor que a melhor solucao ou a melhor solucao ainda for vazia(o que acontece inicialmente)
    # Entao a solucao atual tem potencial para ser menor que a melhor solucao ate o momento
    if len(melhor_solucao) > len(solucao_atual) or len(melhor_solucao) == 0:
        if not matrizEhCompleta(matriz_N):  # Se a matriz nao esta completa, pode tentar encaixar quadrados dentro dela
            # Tenta-se encaixar quadrados de tamanho N-1 (lado), até quadrado de tamanho 1
            lado_aux = lado  # lado_aux eh o lado maximo que pode ser encaixado ate o momento
            for i in range(lado, 0, -1):
                # Tenta encaixar na matriz o quadrado de lado i
                encaixou, encaixe, nova_matriz = tentaEncaixar(matriz_N, i)
                if encaixou:  # Se encaixou (i,j,l)
                    solucao_atual.append(encaixe)  # Entao adiciona esse encaixe na solucao atual
                    # E realiza o backtracking na matriz com o quadrado encaixado (nova_matriz)
                    backtracking(copy.deepcopy(nova_matriz), lado_aux)
                    solucao_atual.pop()  # Ao voltar da recursao deve-se remover o encaixe da solucao
                    # Obs: a matriz sem o quadrado encaixado se chamada matriz_N, e com o quadrado encaixado nova_matriz
                else:  # Caso nao consiga encaixar
                    lado_aux -= 1  # Entao se conseguir numa proxima iteracao podera encaixar com lados menores
        # Caso contrario a matriz esta completa, verificase se a solucao atual eh menor que a melhor solucao do momento
        elif len(solucao_atual) < len(melhor_solucao) or len(melhor_solucao) == 0:
            melhor_solucao = copy.deepcopy(solucao_atual)  # Se for atualizar a melhor solucao


def resolve(N):
    """
        Essa funcao recebe o valor do lado do quadrado de papel (N) que deseja-se formar.
        Deve retornar a quantidade minima de papeis com lado menor que N que devem ser
        utilizados para formar um quadrado de papel de lado N.
        Deve retornar tambem as coordenadas (X,Y) no canto superior esquerdo de cada quadrado de papel.
        De forma geral a saida deve ser: (X, Y, L), onde X e Y sao as coordenadas no canto superior esquerdo
        e tamanho do lado do quadrado.

        Para isso sera utilizado Backtracking,
        Inicialmente sera tentado encaixar quadrados de lado N-1, e se nao couber,
        sera colocado quadrados de lado N-2, e assim por diante ate quadrados de lado 1.

        A melhor solucao eh aquela que resultar numa quantidade menor de quadrados utilizados
    """

    # Para issso, inicialmente eh criado uma matriz inicializado com 0
    # Essa matriz representara o quadrado de papel que esta sendo formado
    # Se ela estiver com valor diferente de 0 significa que ela esta ocupada com um quadrado naquela area
    # Cada posicao dessa matriz representa um quadrado de lado 1
    # Se por exemplo a posicao (0,0) dessa matriz for 1, entao um quadrado de lado 1
    # esta inserido na matriz na posicao (0,0)
    # Se por exemplo as posicoes (0,0), (0, 1), (1,0) (1,1) forem 2, entao juntando todas essas posicoes
    # tem-se um quadrado de lado 2, que nada mais sao que 4 quadrados de lado 1
    matriz_N = [[0] * (N) for i in range(N)]

    global melhor_solucao  # Obtem o vetor de melhor solucao
    global solucao_atual  # Obtem o vetor de solucao atual
    # Obs: Cada elemento desses vetores eh do tipo (i,j,l)
    # Onde (i,j) representa a posicao do canto superior esquerdo do quadrado na matriz
    # E l o lado do quadrado inserido na posicao (i,j)

    melhor_solucao = []  # Inicialmente a melhor solucao esta vazia
    solucao_atual = []  # E a solucao atual é vazia também
    # É feito o backtracking sendo possível encaixar no matriz só quadrados menores que o tamanho da propria matriz
    backtracking(matriz_N, lado=N - 1)

    melhor_solucao_real = []  # Inicializar vetor de melhor solucao para saida
    for solucao in melhor_solucao:
        # Na saida do problema nao tem posicao 0, por isso deve-se somar 1
        # E aparentemente, na saída do problema, o eixo x, y estao trocados
        melhor_solucao_real.append((solucao[1] + 1, solucao[0] + 1, solucao[2]))

    # Montar string de retono
    retorno = ""
    retorno += str(
        len(melhor_solucao_real)) + "\n"  # Adicionar quantidade de quadrados utilizados para atingir a solucao
    for quadrado in melhor_solucao_real:  # Para cada (i,j,l)
        retorno += str(quadrado[0]) + " " + str(quadrado[1]) + " " + str(quadrado[2]) + "\n"  # Formatar para saida

    return retorno[:-1]  # Retorna a string de saida


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]  # Testes duram por volta de 15 segundos
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
