import math
import random
import struct
import wave
from pathlib import Path


TAXA = 22050
PASTA = Path(__file__).resolve().parent / "assets" / "audio"


def limitar(valor):
    return max(-1.0, min(1.0, valor))


def salvar(nome, amostras):
    PASTA.mkdir(parents=True, exist_ok=True)
    with wave.open(str(PASTA / nome), "w") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(TAXA)
        dados = b"".join(
            struct.pack("<h", int(limitar(amostra) * 32767))
            for amostra in amostras
        )
        arquivo.writeframes(dados)


def envelope(tempo, duracao, ataque=0.04, queda=0.15):
    entrada = min(1.0, tempo / ataque) if ataque else 1.0
    saida = min(1.0, max(0.0, duracao - tempo) / queda) if queda else 1.0
    return entrada * saida


def gerar_trilha():
    duracao = 16.0
    total = int(TAXA * duracao)
    notas = [110.0, 130.81, 146.83, 164.81, 146.83, 130.81, 123.47, 98.0]
    amostras = []

    for indice in range(total):
        tempo = indice / TAXA
        nota = notas[int(tempo / 2) % len(notas)]
        onda_lenta = math.sin(2 * math.pi * nota * tempo) * 0.12
        harmonico = math.sin(2 * math.pi * nota * 2 * tempo) * 0.035
        brilho = math.sin(2 * math.pi * (nota * 1.5) * tempo) * 0.025
        oceano = math.sin(2 * math.pi * 0.12 * tempo) * 0.025
        amostras.append((onda_lenta + harmonico + brilho) * (0.82 + oceano))

    suavizacao = int(TAXA * 0.4)
    for indice in range(suavizacao):
        fator = indice / suavizacao
        amostras[indice] *= fator
        amostras[-indice - 1] *= fator

    salvar("trilha.wav", amostras)


def gerar_tom(nome, frequencias, duracao, volume=0.35, ruido=0.0):
    total = int(TAXA * duracao)
    amostras = []
    bloco = duracao / len(frequencias)

    for indice in range(total):
        tempo = indice / TAXA
        frequencia = frequencias[min(len(frequencias) - 1, int(tempo / bloco))]
        forma = math.sin(2 * math.pi * frequencia * tempo)
        forma += 0.25 * math.sin(2 * math.pi * frequencia * 2 * tempo)
        forma += random.uniform(-ruido, ruido)
        amostras.append(forma * volume * envelope(tempo, duracao))

    salvar(nome, amostras)


gerar_trilha()
gerar_tom("colisao.wav", [150, 95], 0.32, volume=0.42, ruido=0.18)
gerar_tom("fase.wav", [330, 440, 660], 0.85, volume=0.30)
gerar_tom("vitoria.wav", [392, 523.25, 659.25, 783.99], 1.25, volume=0.32)
gerar_tom("derrota.wav", [220, 174.61, 130.81, 98], 1.15, volume=0.34, ruido=0.03)

print(f"Áudios criados em: {PASTA}")
