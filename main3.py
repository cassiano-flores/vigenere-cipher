import collections
import math

def indice_coincidencia(texto):
    total_caracteres = len(texto)
    frequencia = collections.Counter(texto)
    ic = 0
    for letra in frequencia:
        ic += (frequencia[letra] * (frequencia[letra] - 1))
    ic /= (total_caracteres * (total_caracteres - 1))
    return ic

def dividir_texto(texto, tamanho):
    partes = [''] * tamanho
    for i, caracter in enumerate(texto):
        partes[i % tamanho] += caracter
    return partes

def calcular_ic_medio(texto, tamanho_chave):
    partes = dividir_texto(texto, tamanho_chave)
    ic_medio = sum(indice_coincidencia(parte) for parte in partes) / len(partes)
    return ic_medio

def encontrar_tamanho_chave(texto_cifrado):
    ic_minimo = float('inf')
    tamanho_chave = 0
    for tamanho in range(2, 21):  # Testar tamanhos de chave de 2 a 20
        ic_medio = calcular_ic_medio(texto_cifrado, tamanho)
        if abs(ic_medio - 0.065) < ic_minimo:  # IC esperado para o inglês é de aproximadamente 0.065
            ic_minimo = abs(ic_medio - 0.065)
            tamanho_chave = tamanho
    return tamanho_chave

def decifrar_vigenere(texto_cifrado, tamanho_chave):
    partes = dividir_texto(texto_cifrado, tamanho_chave)
    chave = ''
    for parte in partes:
        frequencia = collections.Counter(parte)
        letra_mais_frequente = max(frequencia, key=frequencia.get)
        chave += chr((ord(letra_mais_frequente) - ord('E')) % 26 + ord('A'))  # Supondo que 'E' seja a letra mais frequente em inglês
    texto_decifrado = ''
    for i, caracter in enumerate(texto_cifrado):
        chave_atual = chave[i % tamanho_chave]
        texto_decifrado += chr((ord(caracter) - ord(chave_atual)) % 26 + ord('A'))
    return texto_decifrado


# Texto cifrado
with open("plaintext-english.txt", "r") as file:
  texto_cifrado = file.read().replace('\n', '')

tamanho_chave = encontrar_tamanho_chave(texto_cifrado)
print("Tamanho da chave:", tamanho_chave)
texto_decifrado = decifrar_vigenere(texto_cifrado, tamanho_chave)
print("Texto decifrado:", texto_decifrado)
