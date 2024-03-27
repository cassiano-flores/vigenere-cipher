global TAMANHO_CHAVE_MAXIMO
global LETRA_MAIS_FREQUENTE_INGLES
#global LETRA_MAIS_FREQUENTE_PORTUGUES
global TEXTO_CIFRADO_INGLES
#global TEXTO_CIFRADO_PORTUGUES

TAMANHO_CHAVE_MAXIMO = 20
LETRA_MAIS_FREQUENTE_INGLES = 'E'
#LETRA_MAIS_FREQUENTE_PORTUGUES = 'A'

with open("plaintext-english.txt", "r") as file:
  TEXTO_CIFRADO_INGLES = file.read().replace('\n', '')

# with open("plaintext-portuguese.txt", "r") as file:
  # TEXTO_CIFRADO_PORTUGUES = file.read().replace('\n', '')

#----------#----------#----------#----------#----------#----------#----------#----------#----------#----------#----------#
# O Índice de Coincidência (IC) é uma medida estatística que indica a probabilidade de dois caracteres aleatórios
# em um texto serem iguais. Em outras palavras, ele mede a tendência de repetição de caracteres em um texto.
# O resultado do cálculo é um valor entre 0 e 1. Quanto mais próximo de 1, maior é a repetição de caracteres no texto e
# maior a probabilidade de ser uma cifra de Vigenère.
def calcular_ic(texto):
    total_caracteres = len(texto)
    frequencias = {}

    texto = texto.lower()

    # conta a frequência de cada caractere no texto
    for caractere in texto:
        if caractere.isalpha():  # só letra
            if caractere in frequencias:
                frequencias[caractere] += 1
            else:
                frequencias[caractere] = 1

    # calcula o índice de coincidência
    ic = 0
    for frequencia in frequencias.values():
        ic += (frequencia * (frequencia - 1)) / (total_caracteres * (total_caracteres - 1))

    return ic


def calcular_ic_medio(texto):
    ic_medio = []

    # calcula o IC médio para cada tamanho de chave possível (suposição)
    for tamanho_chave in range(1, TAMANHO_CHAVE_MAXIMO + 1):
        ic_total = 0
        num_subtextos = len(texto) // tamanho_chave

        # divide o texto em subtextos de acordo com o tamanho da chave desta suposição
        for i in range(tamanho_chave):
            # pega todos os caracteres a cada 'tamanho_chave' de distância, ou seja, pega o i-ésimo caractere de cada subtexto,
            # resultando assim em um novo texto formado apenas por caracteres cifrados com o mesmo caractere dada uma chave
            subtexto = texto[i::tamanho_chave]
            ic_total += calcular_ic(subtexto)

        ic_medio.append(ic_total / num_subtextos)

    return ic_medio


def tamanho_chave_provavel(ic_medio):
    # encontra o maior valor de IC médio e sua posição no array
    maior_ic = max(ic_medio)
    indice_maior_ic = ic_medio.index(maior_ic)

    return indice_maior_ic + 1  # adiciona 1 porque começa em 0
