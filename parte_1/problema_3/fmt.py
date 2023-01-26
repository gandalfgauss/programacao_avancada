from time import time  # Funcao para computar o tempo computacional
from math import ceil  # Funcao para arredondar para numero real para o inteiro superior


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

    return dados


def resolve(texto):
    """
    Funçao que recebe um texto e retorna um texto no formato do Unix
    """

    # Separar paragrafos e resolver individualmente
    # "paragrafos" é um vetor, onde cada posicao vetor contem um paragrafo, que por sua vez contem as linhas da entrada
    # Cada posicao do paragrafo, eh um vetor de linhas

    paragrafos = []  # vetor que armazenara os paragrafos do texto, ou seja, texto apos dois "\n" seguidos
    paragrafo = []  # vetor que armazenara as linhas de um paragrafo
    for indice_linha, linha in enumerate(texto):  # para cada linha no texto
        if linha == "\n":  # se achar um "\n" isolado, significa que terminou de achar um paragrafo
            paragrafos.append(paragrafo)  # entao o paragrafo eh adicionado a lista de paragrafos
            paragrafo = []  # e o marcador de paragrafo atual eh zerado
        elif indice_linha == len(texto) - 1:  # caso chegue no final do texto, ou seja, na ultima linha
            paragrafo += [linha]  # ela eh adicionada ao vetor de linha ("paragrafo")
            paragrafos.append(paragrafo)  # e o paragrafo completo eh adicionado no vetor de paragrafos
        else:  # caso nao encontre nenhum indicador de que acabou o texto ou de que eh um paragrafo
            paragrafo += [linha]  # entado adicona-se a linha no paragrafo atual


    # Como cada posicao do vetor de paragrafos, eh um paragrafo
    # E cada paragrafo eh um vetor de linhas, deve-se juntar todas as linhas dentro de um paragrafo
    # substituindo o '\n' do final de cada linha por espaco
    # vetor que armazenara esses novos paragrafos transformados
    novos_paragrafos = ["".join(paragrafo).replace("\n", " ") for paragrafo in paragrafos]

    # Finalmente, deve-se juntar as palavras de acordo com as regras
    novo_texto = ""  # essa string armazenara o texto transformado e que sera retornado

    # Eh calculado a quantidade de caracteres totais do texto
    tamanho_total = sum([len(paragrafo) for paragrafo in novos_paragrafos])

    # Dividindo a quantidade total de caracteres do texto por 72
    # Onde 72 eh a quantidade maxima de caracteres por linhas
    # Descobre-se a quantidade de linhas necessarias para armazenar o texto
    qnt_inteira_linhas_necessarias = ceil(tamanho_total / 72)  # Quantidade inteira de linhas necessarias

    # Finalmente, ao dividir a quantidade total de caracteres do texto pela quantidade de linhas que ele tera
    # Descobre-se a quantidade de caracteres que cada linha deve ter
    qnt_carac_por_linha = ceil(
        tamanho_total / qnt_inteira_linhas_necessarias)  # Quantidade de caracteres por paragrafo

    # Para cada paragrafo
    for indice_paragrafo, paragrafo in enumerate(novos_paragrafos):
        pedaco_do_texto = ""  # declara-se um pedaco de texto (linha) que sera inserido no novo texto
        lista_de_palavras = paragrafo.split(" ")  # separe-se as palavras do paragrafo
        for indice_palavra, palavra in enumerate(lista_de_palavras):  # para palavra
            if indice_palavra == len(lista_de_palavras) - 1:  # se for a ultima palavra do paragrafo
                pedaco_do_texto += palavra  # adiciona-se essa palavra ao pedaco de texto
                novo_texto += pedaco_do_texto  # e adiciona-se esse pedaco final no novo_texto
            elif len(
                    palavra) >= qnt_carac_por_linha:  # caso o tamanho da palavra a ser inserida for maior que a quantidade de caracteres por linha do problema
                novo_texto += pedaco_do_texto + "\n" + palavra + "\n"  # adiciona-se o pedaco de texto montado ate entao, e a palavra grande numa outra linha, dentro do novo texto
                pedaco_do_texto = ""  # E como o pedaco de texto ja foi adicionado no novo texto, entao ele e esvaziado
            elif len(palavra) + len(
                    pedaco_do_texto) <= qnt_carac_por_linha:  # se o pedaco do texto couber mais uma palavra na linha
                pedaco_do_texto += palavra + " "  # entao adiciona essa palavra ao pedaco do texto junto de um espaco
            elif len(palavra) + len(
                    pedaco_do_texto) >= qnt_carac_por_linha:  # se a palavra ultrapassar o tamanho da linha
                novo_texto += pedaco_do_texto + "\n"  # entao adiciona-se a linha ao texto
                pedaco_do_texto = ""
                pedaco_do_texto += palavra + " "  # e continua o processo inserindo a palavra numa nova linha

        if indice_paragrafo != len(novos_paragrafos) - 1:  # se nao for o ultimo paragrafo insere os '\n'
            novo_texto += "\n\n"

    return novo_texto  # retorna o texto transformado


if __name__ == '__main__':
    """ Menu principal do programa"""
    arquivos_de_teste = ["entrada.txt", "teste2.txt", "teste3.txt", "teste4.txt", "teste5.txt"]

    for arquivo_de_teste in arquivos_de_teste:
        tempo_inicial = time()

        texto = entrada(arquivo_de_teste)
        texto_ajustado = resolve(texto)

        # Imprimir resultado
        print("-" * 30, "Saida:", "-" * 30)
        print(texto_ajustado, end="")
        print()
        tempo_final = time()
        print()
        print("Tempo de execucao:", tempo_final - tempo_inicial, "s")
        print("-" * 68)
