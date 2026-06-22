import pygame

import random

inimigo = pygame.Rect(750, 200, 60, 60)
inimigo2 = pygame.Rect(1050, 100, 60, 60)
inimigo3 = pygame.Rect(1350, 350, 60, 60)
inimigo_fase2 = pygame.Rect(1000, 220, 90, 64)
velocidade_inimigo = 4

pygame.init()

LARGURA = 800
ALTURA = 500

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Ocean Defender")

imagem_fundo = pygame.image.load(
    "assets/fundo.png"
).convert()

imagem_fundo_fase2 = pygame.image.load(
    "assets/fundo_fase2.png"
).convert()

relogio = pygame.time.Clock()
fonte_titulo = pygame.font.Font(None, 72)
fonte_menu = pygame.font.Font(None, 32)

jogador = pygame.Rect(100, 220, 80, 60)
imagem_jogador = pygame.image.load(
    "assets/jogador.png"
).convert_alpha()

imagem_jogador = pygame.transform.smoothscale(
    imagem_jogador,
    jogador.size
)
imagem_inimigo = pygame.image.load(
    "assets/inimigo.png"
).convert_alpha()

imagem_inimigo = pygame.transform.smoothscale(
    imagem_inimigo,
    inimigo.size
)
imagem_inimigo_fase2 = pygame.image.load(
    "assets/inimigo_fase2.png"
).convert_alpha()

imagem_inimigo_fase2 = pygame.transform.smoothscale(
    imagem_inimigo_fase2,
    inimigo_fase2.size
)
velocidade = 5
estado = "menu"
rodando = True
vidas = 3
pontos = 0
fase = 1

def escrever(texto, fonte, cor, y, x=LARGURA // 2):
    imagem = fonte.render(texto, True, cor)
    posicao = imagem.get_rect(center=(x, y))
    tela.blit(imagem, posicao)




while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if estado == "menu" and evento.key == pygame.K_RETURN:
                jogador.center = (140, ALTURA // 2)
                vidas = 3
                pontos = 0
                fase = 1
                inimigo.left = LARGURA
                inimigo.y = random.randint(
                    0,
                    ALTURA - inimigo.height
                )
                inimigo2.left = LARGURA + 300
                inimigo2.y = random.randint(
                    0,
                    ALTURA - inimigo2.height
                )

                inimigo3.left = LARGURA + 600
                inimigo3.y = random.randint(
                    0,
                    ALTURA - inimigo3.height
                )
                inimigo_fase2.left = LARGURA + 400
                inimigo_fase2.y = random.randint(
                0,
                ALTURA - inimigo_fase2.height
                )

                estado = "jogo"

            elif estado == "jogo" and evento.key == pygame.K_ESCAPE:
                estado = "menu"
            elif estado == "derrota" and evento.key == pygame.K_RETURN:
                estado = "menu"
            elif estado == "vitoria" and evento.key == pygame.K_RETURN:
                estado = "menu"

    if estado == "jogo" and fase == 2:
        tela.blit(imagem_fundo_fase2, (0, 0))
    else:
        tela.blit(imagem_fundo, (0, 0))

    if estado == "menu":
        escrever(
            "OCEAN DEFENDER",
            fonte_titulo,
            (255, 220, 40),
            120
        )
        escrever(
            "ENTER - Iniciar",
            fonte_menu,
            (255, 255, 255),
            230
        )
        escrever(
            "WASD ou Setas - Movimentar",
            fonte_menu,
            (255, 255, 255),
            280
        )
        escrever(
            "ESC - Voltar ao menu",
            fonte_menu,
            (255, 255, 255),
            330
        )
        escrever(
            "Objetivo: alcance 10 pontos",
            fonte_menu,
            (255, 255, 255),
            380
        )

    elif estado == "jogo":
        teclas = pygame.key.get_pressed()
    
        if teclas[pygame.K_UP] or teclas[pygame.K_w]:
            jogador.y -= velocidade
        if teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
            jogador.y += velocidade
        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            jogador.x -= velocidade
        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            jogador.x += velocidade

        jogador.clamp_ip(tela.get_rect())

        if fase == 1:
            velocidade_inimigo = min(
                7,
                4 + pontos // 3
            )
        else:
            velocidade_inimigo = 7

        inimigo.x -= velocidade_inimigo

        if inimigo.right < 0:
            inimigo.left = LARGURA
            pontos += 1
            if pontos >= 10:
                if fase == 1:
                    fase = 2
                    pontos = 0
                else:
                    estado = "vitoria"
            inimigo.y = random.randint(
                0,
                ALTURA - inimigo.height
            )

        if jogador.colliderect(inimigo):
            vidas = max(0, vidas - 1)

            if vidas == 0:
                estado = "derrota"
            inimigo.left = LARGURA
            inimigo.y = random.randint(
                0,
                ALTURA - inimigo.height
            )
        escrever(
            f"Vidas: {vidas}",
            fonte_menu,
            (255, 255, 255),
            30,
            80
        )
        escrever(
            f"Pontos: {pontos}",
            fonte_menu,
            (255, 255, 255),
            60,
            80
        )
        escrever(
            f"Fase: {fase}",
            fonte_menu,
            (255, 255, 255),
            90,
            80
        )

        tela.blit(
            imagem_jogador,
            jogador
        )

        tela.blit(
            imagem_inimigo,
            inimigo
        )
        if fase == 1 and pontos >= 3:
            inimigo2.x -= velocidade_inimigo

            if inimigo2.right < 0:
                inimigo2.left = LARGURA + 200
                inimigo2.y = random.randint(
                    0,
                    ALTURA - inimigo2.height
                )
                pontos += 1

            if jogador.colliderect(inimigo2):
                vidas = max(0, vidas - 1)
                inimigo2.left = LARGURA + 200
                inimigo2.y = random.randint(
                    0,
                    ALTURA - inimigo2.height
                )

                if vidas == 0:
                    estado = "derrota"

            tela.blit(
                imagem_inimigo,
                inimigo2
            )
        if fase == 1 and pontos >= 6:
            inimigo3.x -= velocidade_inimigo

            if inimigo3.right < 0:
                inimigo3.left = LARGURA + 300
                inimigo3.y = random.randint(
                    0,
                    ALTURA - inimigo3.height
                )
                pontos += 1

            if jogador.colliderect(inimigo3):
                vidas = max(0, vidas - 1)
                inimigo3.left = LARGURA + 300
                inimigo3.y = random.randint(
                    0,
                    ALTURA - inimigo3.height
                )

                if vidas == 0:
                    estado = "derrota"

            tela.blit(
                imagem_inimigo,
                inimigo3
            )
            if fase == 2:
                inimigo_fase2.x -= velocidade_inimigo + 2

            if inimigo_fase2.right < 0:
                inimigo_fase2.left = LARGURA + 300
                inimigo_fase2.y = random.randint(
                    0,
                    ALTURA - inimigo_fase2.height
                )
                pontos += 1

                if pontos >= 10:
                    estado = "vitoria"

            if jogador.colliderect(inimigo_fase2):
                vidas = max(0, vidas - 1)
                inimigo_fase2.left = LARGURA + 300
                inimigo_fase2.y = random.randint(
                    0,
                    ALTURA - inimigo_fase2.height
                )

                if vidas == 0:
                    estado = "derrota"

            tela.blit(
                imagem_inimigo_fase2,
                inimigo_fase2
            )
    elif estado == "derrota":
        escrever(
            "VOCE PERDEU",
            fonte_titulo,
            (255, 60, 60),
            200
        )

        escrever(
            "ENTER - Voltar ao menu",
            fonte_menu,
            (255, 255, 255),
            280
        )

    elif estado == "vitoria":
        escrever(
            "VOCE VENCEU!",
            fonte_titulo,
            (60, 255, 120),
            200
        )

        escrever(
            "ENTER - Voltar ao menu",
            fonte_menu,
            (255, 255, 255),
            280
        )    
    pygame.display.update()
    relogio.tick(60)

pygame.quit()