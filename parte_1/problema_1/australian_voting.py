from time import time  # Biblioteca para marca o tempo computacional


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

    numero_de_eleicoes = int(dados[0])  # Receber quantidade de eleicoes/casos

    eleicoes = []  # Vetor de eleicoes/problemas

    posicao_inicial = 2
    # iterar cada eleicao/problema
    for _ in range(numero_de_eleicoes):
        quantidade_de_candidatos = int(dados[posicao_inicial])  # Ler quantidade de candidatos

        # Ler nomes dos Candidatos
        posicao_inicial += 1
        nomes_dos_candidatos = dict()
        for i in range(1, quantidade_de_candidatos + 1):
            nomes_dos_candidatos[i] = dados[posicao_inicial][:-1]  # Removendo \n
            posicao_inicial += 1

        # Ler votos
        votos = []
        voto = [int(v) for v in dados[posicao_inicial].split(" ")]
        while len(voto) == quantidade_de_candidatos:
            votos.append(voto)

            posicao_inicial += 1

            # conferir se chegou no final dos dados
            if posicao_inicial >= len(dados):
                voto = []
            else:
                voto = [int(v) for v in dados[posicao_inicial].split(" ")]

        eleicoes.append((nomes_dos_candidatos, votos))

    # Retornar o numero de eleicoes e os dados de cada uma
    return numero_de_eleicoes, eleicoes


def ganhou_eleicao(votos, quantidade_de_votos):
    """ Essa funcao recebe um dicionario com o numero
    de votos de cada candidato e a quantidade de votos
    da eleicao.
    Retorna o Candidato que ganhou a eleicao
    com mais de 50/100 dos votos, se houver.
    Caso contrario retorna None
    """

    # Obter maior quantidade de votos
    candidato, maior_quantidade_votos = max(votos.items(), key=lambda x: x[1])

    # Verificar se algum candidato obteve mais que 50/100 dos votos
    if maior_quantidade_votos > 0.5 * quantidade_de_votos:
        return candidato

    return None


def empate(votos):
    """ Essa funcao recebe um dicionario com o numero
    de votos de cada candidato.
    Retorna True caso haja empate na eleicao.
    Caso contrario retorna False
    """
    # Extrair votos sem repeticao
    return len(set(votos.values())) == 1


def regula_votacao(votos_contados, votos, nomes_dos_candidatos):
    """
    Essa funcao recebe, como referencia, um dicionario com o numero
    de votos de cada candidato, a lista de votos e os
    nomes dos candidatos que ainda disputam a eleicao.
    Ela remove os candidatos menos votados e reinicia a eleicao
    """

    # Extrair menor quantidade de votos
    menor_quantidade_votos = min(votos_contados.items(), key=lambda x: x[1])[1]

    # Adicionar candidatos, que serao eliminados, numa lista
    candidatos_eliminados = [candidato[0] for candidato in votos_contados.items() if
                             candidato[1] == menor_quantidade_votos]

    # Remover candidatos eliminados dos votos e dos nomes dos candidatos
    for candidato in candidatos_eliminados:
        for voto in votos:
            voto.remove(candidato)

        nomes_dos_candidatos.pop(candidato)

    # Obs.: A passagem dos objetos na funcao foi por referencia


def resolve_eleicoes(numero_de_eleicoes, eleicoes):
    """ Essa funcao recebe o numero de eleicoes
    e os dados de cada uma e retorna e retorna
    o resultado de cada uma"""
    campeoes = []
    for i in range(numero_de_eleicoes):

        nomes_dos_candidatos = eleicoes[i][0]
        votos = eleicoes[i][1]
        quantidade_de_votos = len(votos)
        decidiu_eleicao = False

        # Enquanto nao decidir a eleicao
        while not decidiu_eleicao:
            # Contar votos
            votos_contados = {i: 0 for i in nomes_dos_candidatos.keys()}
            for voto in votos:
                votos_contados[voto[0]] += 1

            # Conferir se algum candidato obteve mais que 50/100 dos votos
            candidato_campeao = ganhou_eleicao(votos_contados, quantidade_de_votos)
            if candidato_campeao is not None:
                campeoes.append([nomes_dos_candidatos[candidato_campeao]])
                decidiu_eleicao = True

            # Conferir se houve um empate generalizado
            elif empate(votos_contados):
                nomes = []
                for nome in nomes_dos_candidatos.values():
                    nomes.append(nome)

                campeoes.append(nomes)
                decidiu_eleicao = True

            # Caso contrario deve-se remover os candidatos menos votados e continuar o algoritmo
            else:
                regula_votacao(votos_contados, votos, nomes_dos_candidatos)
    return campeoes


if __name__ == '__main__':
    arquivos_de_teste = ["entrada.txt", "teste2.txt", "teste3.txt", "teste4.txt", "teste5.txt"]

    for arquivo_de_teste in arquivos_de_teste:
        tempo_inicial = time()
        numero_de_eleicoes, eleicoes = entrada(arquivo_de_teste)
        campeoes = resolve_eleicoes(numero_de_eleicoes, eleicoes)
        tempo_final = time()
        print("-" * 30, "Saida:", "-" * 30)
        for i in range(numero_de_eleicoes):
            for campeao in campeoes[i]:
                print(campeao)
            print()
        print("Tempo de execucao:", tempo_final-tempo_inicial, "s")
        print("-" * 68)
