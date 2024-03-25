def calcular_IC(texto):
    total_letras = contar_letras(texto)
    frequencias = contar_frequencias(texto)
    ic = 0

    for letra, frequencia in frequencias:
        ic += (frequencia * (frequencia - 1)) / (total_letras * (total_letras - 1))

    return ic


def dividir_texto_em_grupos(texto, tamanho):
  grupos = []

  for i in range(0, len(texto), tamanho):
    grupos.append(texto[i:i+tamanho])

  return grupos


def descobrir_tamanho_chave(texto_cifrado):
    ic_esperado = 0.0727
    tamanho_chave = 0
    melhor_ic = 0

    for tamanho_chave_teste in range(1, 20):
        grupos = dividir_texto_em_grupos(texto_cifrado, tamanho_chave_teste)
        soma_ic = 0

        for grupo in grupos:
            ic_grupo = calcular_IC(grupo)
            soma_ic += ic_grupo

        ic_medio = soma_ic / tamanho_chave_teste
        if abs(ic_medio - ic_esperado) < abs(melhor_ic - ic_esperado):
            melhor_ic = ic_medio
            tamanho_chave = tamanho_chave_teste
    
    return tamanho_chave


# teste
texto_cifrado = "WKXVJWJFQZT"
tamanho_chave = descobrir_tamanho_chave(texto_cifrado)
print("Tamanho da chave:", tamanho_chave)
