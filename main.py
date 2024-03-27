# Autores:
# Cassiano Luis Flores Michel  (20204012-7)
# José Eduardo Rodrigues Serpa (20200311-7)

import collections
import math

global TAMANHO_CHAVE_MAXIMO
global TEXTO_CIFRADO_INGLES
global COINCIDENCIA_INGLES
global LETRA_FREQUENTE_INGLES
global TEXTO_CIFRADO_PORTUGUES
global COINCIDENCIA_PORTUGUES
global LETRA_FREQUENTE_PORTUGUES

TAMANHO_CHAVE_MAXIMO = 20
COINCIDENCIA_INGLES = 0.065
COINCIDENCIA_PORTUGUES = 0.072
LETRA_FREQUENTE_INGLES = 'E'
LETRA_FREQUENTE_PORTUGUES = 'A'

#----------#----------#----------#----------#----------#----------#----------#----------#----------#----------#
# cálculo do índice de coincidência
def indice_coincidencia(texto):
    total_caracteres = len(texto)
    frequencia = collections.Counter(texto)
    ic = 0

    for letra in frequencia:
        ic += (frequencia[letra] * (frequencia[letra] - 1))

    ic /= (total_caracteres * (total_caracteres - 1))
    return ic

# dividir o texto em partes
def dividir_texto(texto, tamanho):
    partes = [''] * tamanho

    for i, caracter in enumerate(texto):
        partes[i % tamanho] += caracter

    return partes

# cálculo do índice de coincidência médio
def calcular_ic_medio(texto, tamanho_chave):
    partes = dividir_texto(texto, tamanho_chave)
    ic_medio = sum(indice_coincidencia(parte) for parte in partes) / len(partes)

    return ic_medio

# encontrar o tamanho da chave
def encontrar_tamanho_chave(texto_cifrado, idioma):
    ic_minimo = float('inf')
    tamanho_chave = 0

    for tamanho in range(2, TAMANHO_CHAVE_MAXIMO + 1):
        ic_medio = calcular_ic_medio(texto_cifrado, tamanho)

        if idioma == 'us':
          if abs(ic_medio - COINCIDENCIA_INGLES) < ic_minimo:
              ic_minimo = abs(ic_medio - COINCIDENCIA_INGLES)
              tamanho_chave = tamanho
        elif idioma == 'pt':
            if abs(ic_medio - COINCIDENCIA_PORTUGUES) < ic_minimo:
              ic_minimo = abs(ic_medio - COINCIDENCIA_PORTUGUES)
              tamanho_chave = tamanho

    return tamanho_chave

# decifrar o texto cifrado com cifra de Vigenère
def decifrar_vigenere(texto_cifrado, tamanho_chave, idioma):
    partes = dividir_texto(texto_cifrado, tamanho_chave)
    chave = ''

    for parte in partes:
        frequencia = collections.Counter(parte)
        letra_mais_frequente = max(frequencia, key=frequencia.get)

        if idioma == 'us':
          chave += chr((ord(letra_mais_frequente) - ord(LETRA_FREQUENTE_INGLES)) % 26 + ord('A'))
        elif idioma == 'pt':
          chave += chr((ord(letra_mais_frequente) - ord(LETRA_FREQUENTE_PORTUGUES)) % 26 + ord('A'))

    texto_decifrado = ''
    for i, caracter in enumerate(texto_cifrado):
        chave_atual = chave[i % tamanho_chave]
        texto_decifrado += chr((ord(caracter) - ord(chave_atual)) % 26 + ord('A'))

    return texto_decifrado

#----------#----------#----------#----------#----------#----------#----------#----------#----------#----------#
# execução do programa
with open("plaintext-english.txt", "r") as file:
  TEXTO_CIFRADO_INGLES = file.read().replace('\n', '')

with open("plaintext-portuguese.txt", "r") as file:
  TEXTO_CIFRADO_PORTUGUES = file.read().replace('\n', '')

texto_decifrado_ingles = decifrar_vigenere(TEXTO_CIFRADO_INGLES, encontrar_tamanho_chave(TEXTO_CIFRADO_INGLES, 'us'), 'us')
texto_decifrado_portugues = decifrar_vigenere(TEXTO_CIFRADO_PORTUGUES, encontrar_tamanho_chave(TEXTO_CIFRADO_PORTUGUES, 'pt'), 'pt')

with open("texto-claro-ingles.txt", "w") as file:
  file.write(texto_decifrado_ingles)

with open("texto-claro-portugues.txt", "w") as file:
  file.write(texto_decifrado_portugues)
