from time import time  # Funcao para computar o tempo computacional

# Definindo uma classe Pais com os atributos necessarios para a classificacao
# Para posteriormente usar um metodo magico para sobrecarregar o operador >
# E usar a funcao bultin sort do python para ordenar esses paises
class Pais:
    def __init__(self, pontos, vitorias, saldo, gols_marcados, jogos_jogados, nome):  # Constutor
        self.pontos = pontos
        self.vitorias = vitorias
        self.saldo = saldo,
        self.gols_marcados = gols_marcados
        self.jogos_jogados = jogos_jogados
        self.nome = nome
        self.nome_minusculo = self.nome.lower()

    def __gt__(self, other):  # Metodo magico, operador >
        # O objeto eh maior que outro se
        if self.pontos > other.pontos:  # Tiver mais pontos
            return True
        elif self.pontos == other.pontos:  # Se a quantidade de pontos for igual
            if self.vitorias > other.vitorias:  # Se tiver mais vitorias
                return True
            elif self.vitorias == other.vitorias:  # Se a quantidade de vitorias for igual
                if self.saldo > other.saldo:  # Se tiver mais saldo de gol
                    return True
                elif self.saldo == other.saldo:  # Se a quantidade de saldo de gol for igual
                    if self.gols_marcados > other.gols_marcados:  # Se tiver mais gols marcados
                        return True
                    elif self.gols_marcados == other.gols_marcados:  # Se a quandidade de gols marcados for igual
                        if self.jogos_jogados < other.jogos_jogados:  # Se tiver menos jogos jogados
                            return True
                        elif self.jogos_jogados == other.jogos_jogados:  # Se a quantidade de jogos jogados for igual
                            if self.nome_minusculo < other.nome_minusculo:  # Se tiver um nome menor na ordem lexicografica
                                return True
                            else:  # Caso contrario nao eh maior
                                return False
                        else:
                            return False
                    else:
                        return False
                else:
                    return False
            else:
                return False
        else:
            return False

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

    qntd_torneios = int(dados[0])  # Recebe a quantidade de torneios que ocorreram
    torneios = []  # Vetor que irah armazenar os torneios

    posicao = 1  # posicao no vetor de dados
    for _ in range(qntd_torneios):  # Para cada torneio
        torneio = dict()  # inicializa um torneio

        torneio["nome"] = dados[posicao][:-1]  # recebe o nome do torneio
        posicao += 1

        qntd_paises = int(dados[posicao])  # recebe a quantidade de paises participantes
        posicao += 1

        paises = []  # vetor de paises participantes
        for _ in range(qntd_paises):  # para cada pais participante do torneio
            paises.append(dados[posicao][:-1])  # adiciona o pais no vetor de paises participantes
            posicao += 1

        torneio["paises"] = paises  # adiciona os paises ao torneio

        qntd_jogos = int(dados[posicao])  # recebe a quantidade de jogos que ocorreram ate entao no torneio
        posicao += 1

        # inicializa o vetor de jogos
        # o qual cada posicao eh uma tupla com 4 posicoes
        # 0-> Pais 1, 1-> Pais 2, 2-> Gols Pais 1, 3-> Gols Pais 2
        jogos = []
        for _ in range(qntd_jogos):
            jogo = dados[posicao].split("#")
            pais1 = jogo[0]
            pais2 = jogo[2][:-1]
            placar = jogo[1].split("@")
            gols_pais1 = int(placar[0])
            gols_pais2 = int(placar[1])

            jogos.append((pais1, pais2, gols_pais1, gols_pais2))

            posicao += 1

        torneio["jogos"] = jogos  # Adiciona os jogos ao torneio

        torneios.append(torneio)  # Adiciona o torneio ao vetor de torneio

    return torneios  # retorna os torneios


def calcula_v_d_e_p(pais, jogos, pontuacao_paises):
    """ Funcao que recebe o nome de um pais, os jogos do torneio,
    e o dicionario de dados de todos os paises,
    e retorna a quantidade de vitorias, derrotas, empates
     e a pontuacao desse pais dentro de pontucao paises"""

    pontuacao_paises[pais]["vitorias"] = 0  # incialmente a quantidade de vitorias eh 0
    pontuacao_paises[pais]["derrotas"] = 0  # incialmente a quantidade de derrotas eh 0
    pontuacao_paises[pais]["empates"] = 0  # incialmente a quantidade de empates eh 0
    pontuacao_paises[pais]["pontos"] = 0  # incialmente a quantidade de pontos eh 0

    for jogo in jogos:  # para cada jogo do torneio
        if pais in jogo:  # se o pais estiver no jogo
            if (pais == jogo[0] and jogo[2] > jogo[3]) or (pais == jogo[1] and jogo[3] > jogo[2]):
                pontuacao_paises[pais]["vitorias"] += 1
            elif (pais == jogo[0] and jogo[2] < jogo[3]) or (pais == jogo[1] and jogo[3] < jogo[2]):
                pontuacao_paises[pais]["derrotas"] += 1
            elif jogo[2] == jogo[3]:  # se a quantidade de gol de cada time eh igual entao houve um empate
                pontuacao_paises[pais]["empates"] += 1

    # Vitorias valem 3 pontos, empate 1 ponto e derrota 0 (nao precisa colocar derrota na conta), e nem multiplicar empates por 1
    pontuacao_paises[pais]["pontos"] = 3 * pontuacao_paises[pais]["vitorias"] + pontuacao_paises[pais]["empates"]


def calcula_sdg_gm_gc(pais, jogos, pontuacao_paises):
    """ Funcao que recebe o nome de um pais, os jogos do torneio,
        e o dicionario de dados de todos os paises,
        e retorna a quantidade de gols marcados, gols sofridos e o saldo de gols
        desse pais dentro de pontucao paises"""

    pontuacao_paises[pais]["gols_marcados"] = 0  # incialmente a quantidade de gols_marcados eh 0
    pontuacao_paises[pais]["gols_sofridos"] = 0  # incialmente a quantidade de gols sofridos eh 0

    for jogo in jogos:  # para cada jogo do torneio
        if pais in jogo:  # se o pais estiver no jogo
            if pais == jogo[0]:
                pontuacao_paises[pais]["gols_marcados"] += jogo[2]
                pontuacao_paises[pais]["gols_sofridos"] += jogo[3]
            else:
                pontuacao_paises[pais]["gols_marcados"] += jogo[3]
                pontuacao_paises[pais]["gols_sofridos"] += jogo[2]

    # O saldo de gol de um pais eh a quantidade de gols marcados menos a quantidade de gols sofridos
    pontuacao_paises[pais]["saldo_de_gol"] = pontuacao_paises[pais]["gols_marcados"] - pontuacao_paises[pais][
        "gols_sofridos"]


def calcula_classificacao(paises, pontuacao_paises):
    """ Funcao que recebe o nomes dos paises, e o dicionario de dados de todos os paises,
           e retorna a classificacao dentro de pontucao paises"""


    lista_de_paises = []  # Lista de paises a ser ordenada

    for pais in paises:
        lista_de_paises.append(Pais(pontuacao_paises[pais]["pontos"],
                                    pontuacao_paises[pais]["vitorias"],
                                    pontuacao_paises[pais]["saldo_de_gol"],
                                    pontuacao_paises[pais]["gols_marcados"],
                                    pontuacao_paises[pais]["jogos_jogados"],
                                    pais,))  # Cria os objetos com os atributos necessarios para classificacao, e operador > sobrecarregado

    lista_de_paises.sort(reverse=True)  # ordena em ordem decrescente, ou seja, o mais bem classificado para o pior classificado

    for i, pais in enumerate(lista_de_paises):  # para cada objeto Pais na lista de paises
        pontuacao_paises[pais.nome]["classificacao"] = i+1  # adiciona no dicionario de obejetos daquele pais a sua classificacao
        # como a lista de paises esta ordenada, a posicao 0, significa que o pais daquela posicao eh o primeiro classificado
        # dai vem o i+1


def resolve(torneio):
    """ Funcao que recebe um torneio e retorna:
    - O nome do Torneio
    - Os participante seguindo a ordem de classificacao do torneio,
    seguido dos dados de atuacao no torneio"""

    pontuacao_paises = {nome: {} for nome in torneio["paises"]}  # cria um dicionario de pontuacoes dos paises

    for pais in torneio["paises"]:  # para cada pais
        calcula_v_d_e_p(pais, torneio["jogos"],
                        pontuacao_paises)  # adicona a quantidade de vitorias, derrotas, empates e pontuacao de um pais
        calcula_sdg_gm_gc(pais, torneio["jogos"],
                          pontuacao_paises)  # adicona o saldo de gols, gols marcados e gols sofridos
        pontuacao_paises[pais]["jogos_jogados"] = len(
            [jogo for jogo in torneio["jogos"] if pais in jogo])  # adicona a quantidade de jogos jogados do pais

    calcula_classificacao(torneio["paises"],
        pontuacao_paises)  # recebe pontuacao_paises como referencia e calcula a classificacao de cada pais

    # ordenar o vetor de paises de acordo com a classificacao
    torneio["paises"].sort(key=lambda pais: pontuacao_paises[pais]["classificacao"])

    resultado = ""  # string contendo o resultado do torneio de acordo com a saida do problema

    resultado += torneio["nome"] + "\n"  # Adicionar nome do torneio

    for pais in torneio["paises"]:  # Para cada pais, sendo que esta ordenado para o mais bem classificado para o pior classificado
        resultado += f'{pontuacao_paises[pais]["classificacao"]}) {pais} {pontuacao_paises[pais]["pontos"]}p,' \
                     f' {pontuacao_paises[pais]["jogos_jogados"]}g ({pontuacao_paises[pais]["vitorias"]}-' \
                     f'{pontuacao_paises[pais]["empates"]}-{pontuacao_paises[pais]["derrotas"]}), ' \
                     f'{pontuacao_paises[pais]["saldo_de_gol"]}gd ({pontuacao_paises[pais]["gols_marcados"]}-' \
                     f'{pontuacao_paises[pais]["gols_sofridos"]})\n'

    return resultado
if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt"]  # O teste 2 verifica a questao do nome na classificacao

    for arquivo_de_teste in arquivos_de_teste:
        tempo_inicial = time()

        torneios = entrada(arquivo_de_teste)

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        for torneio in torneios:  # para cada torneio, resolve o problema e imprime a saida
            resultado = resolve(torneio)
            print(resultado)

        print()
        tempo_final = time()
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")  # marca o tempo de execucao
        print("-" * 68)
