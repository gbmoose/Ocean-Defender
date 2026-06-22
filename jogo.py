import random
import sys
from pathlib import Path

import pygame


LARGURA = 800
ALTURA = 500
ALTURA_HUD = 110
FPS = 60
PONTOS_POR_FASE = 10
TEMPO_AVISO_FASE = 2000


def caminho_asset(*partes):
    if getattr(sys, "frozen", False):
        pasta_base = Path(sys.executable).resolve().parent
    else:
        pasta_base = Path(__file__).resolve().parent
    return str(pasta_base.joinpath("assets", *partes))


pygame.mixer.pre_init(22050, -16, 1, 512)
pygame.init()

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ocean Defender")
relogio = pygame.time.Clock()

fonte_titulo = pygame.font.Font(None, 72)
fonte_subtitulo = pygame.font.Font(None, 40)
fonte_menu = pygame.font.Font(None, 32)
fonte_hud = pygame.font.Font(None, 29)

imagem_fundo = pygame.image.load(caminho_asset("fundo.png")).convert()
imagem_fundo_fase2 = pygame.image.load(caminho_asset("fundo_fase2.png")).convert()

jogador = pygame.Rect(100, 220, 80, 60)
imagem_jogador = pygame.image.load(caminho_asset("jogador.png")).convert_alpha()
imagem_jogador = pygame.transform.smoothscale(imagem_jogador, jogador.size)

inimigo = pygame.Rect(750, 200, 60, 60)
inimigo2 = pygame.Rect(1050, 150, 60, 60)
inimigo3 = pygame.Rect(1350, 350, 60, 60)
inimigo_fase2 = pygame.Rect(1000, 220, 90, 64)

imagem_inimigo = pygame.image.load(caminho_asset("inimigo.png")).convert_alpha()
imagem_inimigo = pygame.transform.smoothscale(imagem_inimigo, inimigo.size)
imagem_inimigo_fase2 = pygame.image.load(
    caminho_asset("inimigo_fase2.png")
).convert_alpha()
imagem_inimigo_fase2 = pygame.transform.smoothscale(
    imagem_inimigo_fase2,
    inimigo_fase2.size,
)

sons = {}
audio_disponivel = pygame.mixer.get_init() is not None
som_ativo = True

if audio_disponivel:
    try:
        pygame.mixer.music.load(caminho_asset("audio", "trilha.wav"))
        pygame.mixer.music.set_volume(0.28)
        sons = {
            "colisao": pygame.mixer.Sound(caminho_asset("audio", "colisao.wav")),
            "fase": pygame.mixer.Sound(caminho_asset("audio", "fase.wav")),
            "vitoria": pygame.mixer.Sound(caminho_asset("audio", "vitoria.wav")),
            "derrota": pygame.mixer.Sound(caminho_asset("audio", "derrota.wav")),
        }
        for som in sons.values():
            som.set_volume(0.45)
        pygame.mixer.music.play(-1)
    except (pygame.error, FileNotFoundError):
        audio_disponivel = False
        sons = {}

velocidade_jogador = 5
velocidade_inimigo = 4
estado = "menu"
rodando = True
vidas = 3
pontos = 0
fase = 1
fim_aviso_fase = 0


def escrever(texto, fonte, cor, y, x=LARGURA // 2):
    imagem = fonte.render(texto, True, cor)
    posicao = imagem.get_rect(center=(x, y))
    tela.blit(imagem, posicao)


def desenhar_painel(retangulo, cor=(3, 18, 35, 205), borda=(70, 180, 230, 180)):
    painel = pygame.Surface(retangulo.size, pygame.SRCALPHA)
    pygame.draw.rect(painel, cor, painel.get_rect(), border_radius=18)
    pygame.draw.rect(painel, borda, painel.get_rect(), 2, border_radius=18)
    tela.blit(painel, retangulo.topleft)


def tocar_som(nome):
    if audio_disponivel and som_ativo and nome in sons:
        sons[nome].play()


def alternar_som():
    global som_ativo
    som_ativo = not som_ativo
    if not audio_disponivel:
        return
    if som_ativo:
        pygame.mixer.music.unpause()
    else:
        pygame.mixer.music.pause()
        for som in sons.values():
            som.stop()


def reposicionar_inimigo(retangulo, distancia=0):
    retangulo.left = LARGURA + distancia
    retangulo.y = random.randint(ALTURA_HUD, ALTURA - retangulo.height)


def reiniciar_inimigos():
    reposicionar_inimigo(inimigo)
    reposicionar_inimigo(inimigo2, 300)
    reposicionar_inimigo(inimigo3, 600)
    reposicionar_inimigo(inimigo_fase2, 400)


def iniciar_jogo():
    global vidas, pontos, fase, estado, fim_aviso_fase
    jogador.center = (140, ALTURA // 2)
    vidas = 3
    pontos = 0
    fase = 1
    reiniciar_inimigos()
    estado = "transicao"
    fim_aviso_fase = pygame.time.get_ticks() + TEMPO_AVISO_FASE
    tocar_som("fase")


def registrar_ponto():
    global pontos, fase, estado, fim_aviso_fase
    pontos += 1

    if pontos < PONTOS_POR_FASE:
        return

    if fase == 1:
        fase = 2
        pontos = 0
        reiniciar_inimigos()
        estado = "transicao"
        fim_aviso_fase = pygame.time.get_ticks() + TEMPO_AVISO_FASE
        tocar_som("fase")
    else:
        estado = "vitoria"
        tocar_som("vitoria")


def atualizar_inimigo(retangulo, velocidade, distancia_retorno=0):
    global vidas, estado
    retangulo.x -= velocidade

    if retangulo.right < 0:
        reposicionar_inimigo(retangulo, distancia_retorno)
        registrar_ponto()

    if estado == "jogo" and jogador.colliderect(retangulo):
        vidas = max(0, vidas - 1)
        reposicionar_inimigo(retangulo, distancia_retorno)
        if vidas == 0:
            estado = "derrota"
            tocar_som("derrota")
        else:
            tocar_som("colisao")


def desenhar_fundo():
    if fase == 2 and estado != "menu":
        tela.blit(imagem_fundo_fase2, (0, 0))
    else:
        tela.blit(imagem_fundo, (0, 0))


def desenhar_menu():
    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 15, 35, 80))
    tela.blit(sombra, (0, 0))

    escrever("OCEAN DEFENDER", fonte_titulo, (255, 220, 40), 82)
    escrever("Proteja o oceano e sobreviva às profundezas", fonte_menu, (220, 245, 255), 130)

    desenhar_painel(pygame.Rect(120, 160, 560, 285))
    escrever("ENTER  -  Iniciar missão", fonte_subtitulo, (255, 230, 80), 205)
    escrever("WASD ou Setas  -  Movimentar", fonte_menu, (255, 255, 255), 255)
    escrever("ESC  -  Voltar ao menu / Sair", fonte_menu, (255, 255, 255), 300)
    escrever("M  -  Ligar ou desligar o som", fonte_menu, (255, 255, 255), 345)
    escrever("Objetivo: complete as 2 fases", fonte_menu, (120, 255, 190), 402)


def desenhar_hud():
    desenhar_painel(
        pygame.Rect(14, 12, 190, 94),
        cor=(2, 16, 32, 220),
        borda=(80, 200, 235, 190),
    )
    cor = (255, 255, 255)
    textos = [f"Vidas: {vidas}", f"Pontos: {pontos}", f"Fase: {fase}"]
    for indice, texto in enumerate(textos):
        imagem = fonte_hud.render(texto, True, cor)
        tela.blit(imagem, (30, 21 + indice * 27))

    status_som = "SOM: ON" if som_ativo and audio_disponivel else "SOM: OFF"
    imagem_som = fonte_hud.render(status_som, True, (210, 240, 255))
    tela.blit(imagem_som, (LARGURA - imagem_som.get_width() - 18, 18))


def desenhar_transicao():
    sombra = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    sombra.fill((0, 10, 28, 145))
    tela.blit(sombra, (0, 0))
    desenhar_painel(pygame.Rect(135, 165, 530, 165))

    if fase == 1:
        titulo = "FASE 1 - ÁGUAS RASAS"
        descricao = "Desvie das minas e alcance 10 pontos"
    else:
        titulo = "FASE 2 - ZONA ABISSAL"
        descricao = "Cuidado com as criaturas das profundezas"

    escrever(titulo, fonte_subtitulo, (255, 225, 70), 215)
    escrever(descricao, fonte_menu, (240, 250, 255), 275)


while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_m:
                alternar_som()
            elif estado == "menu" and evento.key == pygame.K_RETURN:
                iniciar_jogo()
            elif estado == "menu" and evento.key == pygame.K_ESCAPE:
                rodando = False
            elif estado in ("jogo", "transicao") and evento.key == pygame.K_ESCAPE:
                estado = "menu"
            elif estado in ("derrota", "vitoria") and evento.key == pygame.K_RETURN:
                estado = "menu"

    if estado == "transicao" and pygame.time.get_ticks() >= fim_aviso_fase:
        estado = "jogo"

    desenhar_fundo()

    if estado == "menu":
        desenhar_menu()

    elif estado == "transicao":
        tela.blit(imagem_jogador, jogador)
        desenhar_transicao()

    elif estado == "jogo":
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.y -= velocidade_jogador
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.y += velocidade_jogador
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.x -= velocidade_jogador
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.x += velocidade_jogador

        jogador.clamp_ip(tela.get_rect())

        if fase == 1:
            velocidade_inimigo = min(7, 4 + pontos // 3)
        else:
            velocidade_inimigo = 7

        atualizar_inimigo(inimigo, velocidade_inimigo)

        if estado == "jogo" and fase == 1 and pontos >= 3:
            atualizar_inimigo(inimigo2, velocidade_inimigo, 200)
        if estado == "jogo" and fase == 1 and pontos >= 6:
            atualizar_inimigo(inimigo3, velocidade_inimigo, 300)
        if estado == "jogo" and fase == 2:
            atualizar_inimigo(inimigo_fase2, velocidade_inimigo + 2, 300)

        if estado == "jogo":
            tela.blit(imagem_jogador, jogador)
            tela.blit(imagem_inimigo, inimigo)

            if fase == 1 and pontos >= 3:
                tela.blit(imagem_inimigo, inimigo2)
            if fase == 1 and pontos >= 6:
                tela.blit(imagem_inimigo, inimigo3)
            if fase == 2:
                tela.blit(imagem_inimigo_fase2, inimigo_fase2)

            desenhar_hud()

    elif estado == "derrota":
        desenhar_painel(pygame.Rect(145, 155, 510, 190))
        escrever("VOCÊ PERDEU", fonte_titulo, (255, 70, 70), 210)
        escrever("ENTER - Voltar ao menu", fonte_menu, (255, 255, 255), 285)

    elif estado == "vitoria":
        desenhar_painel(pygame.Rect(145, 155, 510, 190))
        escrever("VOCÊ VENCEU!", fonte_titulo, (70, 255, 140), 210)
        escrever("ENTER - Voltar ao menu", fonte_menu, (255, 255, 255), 285)

    pygame.display.update()
    relogio.tick(FPS)

pygame.quit()
