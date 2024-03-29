# Autores:
# Cassiano Luis Flores Michel  (20204012-7)
# José Eduardo Rodrigues Serpa (20200311-7)

import string
from math import sqrt

global ALFABETO
global FREQUENCIAS_INGLES
global FREQUENCIAS_PORTUGUES

ALFABETO = string.ascii_lowercase
FREQUENCIAS_INGLES = [8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
FREQUENCIAS_PORTUGUES = [14.63, 1.04, 3.88, 5.01, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]


def calcular_IC(texto_cifrado):
  count = [0]*26
  for letra in texto_cifrado: # conta a frequencia de cada letra
    count[ALFABETO.index(letra)] += 1
  
  numerador = 0
  total = 0
  for i in range(26): # calcula o indice de coincidencia
    numerador += count[i]*(count[i]-1)
    total += count[i]
  
  return 26*numerador / (total*(total-1)) # formula do indice de coincidencia


def calcular_cosseno(x,y):
  numerador = 0
  comprimento_x2 = 0
  comprimento_y2 = 0
  for i in range(len(x)): # calcula o cosseno entre dois vetores
    numerador += x[i]*y[i]
    comprimento_x2 += x[i]*x[i]
    comprimento_y2 += y[i]*y[i]
  
  return numerador / sqrt(comprimento_x2*comprimento_y2) # formula do cosseno


def calcular_periodos(texto_cifrado):
  aux = False
  periodo = 0
  while not aux: # calcula o periodo do texto cifrado
    periodo += 1
    subtextos = ['']*periodo
    for i in range(len(texto_cifrado)): # divide o texto cifrado em subtextos, do tamanho do periodo proposto
      subtextos[i%periodo] += texto_cifrado[i]
    
    soma = 0
    for i in range(periodo): # calcula o indice de coincidencia medio dos subtextos
      soma += calcular_IC(subtextos[i])
    
    ic = soma / periodo # indice de coincidencia medio, ingles = 1.73 (0.066) | portugues = 1.94 (0.074)
    if ic > 1.6:
      aux = True

  return periodo, subtextos


def calcular_chave(texto_cifrado):
  periodo, subtextos = calcular_periodos(texto_cifrado)
  frequencias = []
  for i in range(periodo): # calcula a tabela de frequencia de cada subtexto
    frequencias.append([0]*26) # inicializa a tabela de frequencia para cada letra
    for j in range(len(subtextos[i])): # conta a frequencia de cada letra
      frequencias[i][ALFABETO.index(subtextos[i][j])] += 1

    for j in range(26): # normaliza a tabela de frequencia
      frequencias[i][j] = frequencias[i][j] / len(subtextos[i])

  chave = ['A']*periodo # inicializa a chave com o tamanho do periodo, partindo do ascii de 'A'
  for i in range(periodo):
    for j in range(26):
      tabela_teste = frequencias[i][j:]+frequencias[i][:j] # rotaciona a tabela de frequencia para testar a proximidade com a tabela de idioma
      if calcular_cosseno(FREQUENCIAS_INGLES,tabela_teste) > 0.9: # 0.9 eh um bom match para determinar se uma tabela de frequencia esta proxima de uma tabela de idioma
        chave[i] = ALFABETO[j]

  return chave


def criptografar(texto_claro, chave): # funcao de criptografia de vigenere
  texto_cifrado = ''
  for i in range(len(texto_claro)):
    p = ALFABETO.index(texto_claro[i])
    k = ALFABETO.index(chave[i%len(chave)])
    c = (p + k) % 26
    texto_cifrado += ALFABETO[c]
  
  return texto_cifrado


def descriptografar(texto_cifrado, chave): # funcao de descriptografia de vigenere
  texto_claro = ''
  for i in range(len(texto_cifrado)):
    p = ALFABETO.index(texto_cifrado[i])
    k = ALFABETO.index(chave[i%len(chave)])
    c = (p - k) % 26
    texto_claro += ALFABETO[c]
  
  return texto_claro


def main(): # funcao principal, le os arquivos de texto cifrado, calcula a chave e escreve descriptografado o plaintext
  with open("ciphertext-english.txt", "r") as file:
    ciphertext_english = file.read().replace('\n', '')

  with open("ciphertext-portuguese.txt", "r") as file:
    ciphertext_portuguese = file.read().replace('\n', '')

  plaintext_english = descriptografar(ciphertext_english, calcular_chave(ciphertext_english))
  plaintext_portuguese = descriptografar(ciphertext_portuguese, calcular_chave(ciphertext_portuguese))

  with open("plaintext-english.txt", "w") as file:
    file.write(plaintext_english)

  with open("plaintext-portuguese.txt", "w") as file:
    file.write(plaintext_portuguese)


if __name__ == "__main__":
  main()
