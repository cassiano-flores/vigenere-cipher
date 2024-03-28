# Autores:
# Cassiano Luis Flores Michel  (20204012-7)
# José Eduardo Rodrigues Serpa (20200311-7)

import string
from math import sqrt

ALPHABET = string.ascii_lowercase
english_monofrequencies = [8.17, 1.49, 2.78, 4.25, 12.70, 2.23, 2.02, 6.09, 6.97, 0.15, 0.77, 4.03, 2.41, 6.75, 7.51, 1.93, 0.10, 5.99, 6.33, 9.06, 2.76, 0.98, 2.36, 0.15, 1.97, 0.07]
portuguese_monofrequencies = [14.63, 1.04, 3.88, 5.01, 12.57, 1.02, 1.30, 1.28, 6.18, 0.40, 0.02, 2.78, 4.74, 5.05, 10.73, 2.52, 1.20, 6.53, 7.81, 4.34, 4.63, 1.67, 0.01, 0.21, 0.01, 0.47]


def index_of_coincidence(text):
    counts = [0]*26
    for char in text:
        counts[ALPHABET.index(char)] += 1
    
    number = 0
    total = 0
    for i in range(26):
        number += counts[i]*(counts[i]-1)
        total += counts[i]
    
    return 26*number / (total*(total-1))


def cosangle(x,y):
    numerator = 0
    lengthx2 = 0
    lengthy2 = 0
    for i in range(len(x)):
        numerator += x[i]*y[i]
        lengthx2 += x[i]*x[i]
        lengthy2 += y[i]*y[i]
    
    return numerator / sqrt(lengthx2*lengthy2)


def find_period_slices(ciphertext, idiom):
    found = False
    period = 0
    while not found:
        period += 1
        slices = ['']*period
        for i in range(len(ciphertext)):
            slices[i%period] += ciphertext[i]
        
        sum = 0
        for i in range(period):
            sum += index_of_coincidence(slices[i])
        
        ioc = sum / period
        # English = 1.73 (0.066) | Portuguese = 1,94 (0,074)
        if ioc > 1.6:
          found = True

    return period, slices


def find_key(ciphertext, idiom):
    period, slices = find_period_slices(ciphertext, idiom)
    frequencies = []
    for i in range(period):
        frequencies.append([0]*26)
        for j in range(len(slices[i])):
            frequencies[i][ALPHABET.index(slices[i][j])] += 1
    
        for j in range(26):
            frequencies[i][j] = frequencies[i][j] / len(slices[i])

    key = ['A']*period
    for i in range(period):
        for j in range(26):
            testtable = frequencies[i][j:]+frequencies[i][:j]
            # 0.9 is a good match to determine if a monogram frequency table is close to the a language table
            if cosangle(english_monofrequencies,testtable) > 0.9:
                key[i] = ALPHABET[j]

    return key


def encrypt(plaintext,key):
    ciphertext = ''
    for i in range(len(plaintext)):
        p = ALPHABET.index(plaintext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p + k) % 26
        ciphertext += ALPHABET[c]
    
    return ciphertext


def decrypt(ciphertext,key):
    plaintext = ''
    for i in range(len(ciphertext)):
        p = ALPHABET.index(ciphertext[i])
        k = ALPHABET.index(key[i%len(key)])
        c = (p - k) % 26
        plaintext += ALPHABET[c]
    
    return plaintext


def main():
    with open("ciphertext-english.txt", "r") as file:
      english_ciphertext = file.read().replace('\n', '')

    with open("ciphertext-portuguese.txt", "r") as file:
      portuguese_ciphertext = file.read().replace('\n', '')

    plaintext_english = decrypt(english_ciphertext,find_key(english_ciphertext, "us"))
    plaintext_portuguese = decrypt(portuguese_ciphertext,find_key(portuguese_ciphertext, "pt"))

    with open("plaintext-english.txt", "w") as file:
      file.write(plaintext_english)

    with open("plaintext-portuguese.txt", "w") as file:
      file.write(plaintext_portuguese)


if __name__ == "__main__":
  main()
