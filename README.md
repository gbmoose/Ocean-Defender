# Ocean Defender

Jogo 2D desenvolvido em Python com Pygame para a atividade prática de Linguagem de Programação Aplicada.

## Objetivo

Controle o submarino, desvie dos inimigos e complete duas fases:

- Fase 1 — Águas Rasas: minas aparecem em quantidade e velocidade progressivas.
- Fase 2 — Zona Abissal: minas e criaturas marinhas tornam o desafio mais rápido.

Alcance 10 pontos em cada fase. O jogador começa com 3 vidas.

## Controles

- `ENTER`: iniciar ou voltar ao menu após vitória/derrota.
- `WASD` ou setas: movimentar o submarino.
- `ESC`: voltar ao menu; no menu, fechar o jogo.
- `M`: ligar ou desligar música e efeitos.

## Executar pelo Python

1. Instale Python 3 e Pygame.
2. Mantenha a pasta `assets` ao lado de `jogo.py`.
3. Execute:

```powershell
python jogo.py
```

## Estrutura necessária para o executável

```text
OceanDefender.exe
assets/
  fundo.png
  fundo_fase2.png
  jogador.png
  inimigo.png
  inimigo_fase2.png
  audio/
```

Projeto autoral criado para fins acadêmicos.
