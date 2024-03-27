def contar_frequencias(texto):
  frequencias = {}

  for letra in texto:
    if letra in frequencias:
      frequencias[letra] += 1
    else:
      frequencias[letra] = 1

  return frequencias


def calcular_IC(texto):
  total_letras = len(texto)
  frequencias = contar_frequencias(texto)
  letras_ic = {}

  for frequencia in frequencias:
    letras_ic[frequencia] = (frequencias[frequencia] * (frequencias[frequencia] - 1)) / (total_letras * (total_letras - 1))

  return letras_ic


def dividir_texto_em_grupos(texto, tamanho):
  grupos = []

  for i in range(0, len(texto), tamanho):
    grupos.append(texto[i:i+tamanho])

  if len(grupos[-1]) != tamanho:
    grupos.pop()

  return grupos


def descobrir_tamanho_chave(texto_cifrado):
  english_ic = 0.0686
  melhor_ic = 0
  melhor_tamanho_chave = 0

  for tamanho_chave_teste in range(2, 21):
    grupos = dividir_texto_em_grupos(texto_cifrado, tamanho_chave_teste)

    for grupo in grupos:
      ic_grupo = calcular_IC(grupo)
      media_ic_grupo = sum(ic_grupo.values()) / len(ic_grupo)

      if abs(media_ic_grupo - english_ic) < abs(melhor_ic - english_ic):
        melhor_ic = media_ic_grupo
        melhor_tamanho_chave = tamanho_chave_teste
  
  return melhor_tamanho_chave


# TESTANDO
with open("plaintext-english.txt", "r") as file:
  texto = file.read().replace('\n', '')

# with open("plaintext-portuguese.txt", "r") as file:
  # texto = file.read().replace('\n', '')

def descobrir_chave(tamanho_da_chave):
    texto_dividido = dividir_texto_em_grupos(texto,tamanho_da_chave)
    letras_melhor_ic = {}
    
    for grupo in texto_dividido:
        for i in range(tamanho_da_chave):
            if i in letras_melhor_ic:
                letras_melhor_ic[i] += grupo[i]
            else:
                letras_melhor_ic[i] = grupo[i]
    
    for i in letras_melhor_ic:
        letras_melhor_ic[i] = contar_frequencias(letras_melhor_ic[i])

    

    for i in letras_melhor_ic:
       letras_melhor_ic[i] = chr(ord(get_dict_max(letras_melhor_ic[i])))
    
    
    return letras_melhor_ic

def get_dict_max(dict):
   max = -1;
   letter = "";
   for e in dict.keys():
    if(dict[e] >= max):
       max = dict[e]
       letter = e

    return letter


print(descobrir_tamanho_chave(texto))
print(descobrir_chave(descobrir_tamanho_chave(texto)))