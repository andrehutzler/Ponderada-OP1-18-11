import string
import random

def gerar_alfabetos():
    """Gera duas permutações aleatórias do alfabeto."""
    alfabeto = list(string.ascii_lowercase)

    linha1 = alfabeto[:]   # copia
    linha2 = alfabeto[:]   # copia

    random.shuffle(linha1)
    random.shuffle(linha2)

    return linha1, linha2


def criar_mapa(linha1, linha2):
    """Cria o dicionário de substituição da cifra Kamasutra."""
    mapa = {}

    # linha1 → linha2
    for a, b in zip(linha1, linha2):
        mapa[a] = b

    # linha2 → linha1
    for a, b in zip(linha2, linha1):
        mapa[a] = b

    return mapa


def cifrar_texto(texto, mapa):
    """Aplica a cifra (mesmo método serve para cifrar e decifrar)."""
    resultado = ""

    for caractere in texto.lower():
        if caractere in mapa:
            resultado += mapa[caractere]
        else:
            resultado += caractere

    return resultado


# -------------------------
#     PROGRAMA PRINCIPAL
# -------------------------

print("=== CIFRA KAMASUTRA ===")
print("Uma cifra histórica baseada em pares de letras.\n")

# Gera alfabetos e mapa
linha1, linha2 = gerar_alfabetos()
mapa = criar_mapa(linha1, linha2)

print("Alfabeto 1:", "".join(linha1))
print("Alfabeto 2:", "".join(linha2))
print()

# Pede texto ao usuário
texto_usuario = input("Digite o texto para cifrar: ")

# Cifra
texto_cifrado = cifrar_texto(texto_usuario, mapa)

print("\nTexto cifrado:", texto_cifrado)
