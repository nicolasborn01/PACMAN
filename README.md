# Pac-Man Arcade (Pygame)

Jogo estilo Pac-Man feito em Python com Pygame, contando com movimentação suave, fases progressivas, fantasmas com comportamento dinâmico, menu inicial animado e tela de seleção de fases com cursor retrô.

## Funcionalidades

* **Movimentação e controles:** Controle do Pac-Man pelas setas do teclado com buffer de direção para curvas no centro dos blocos e animação de abrir e fechar a boca.
* **Fases progressivas:** Mapas em matrizes que aumentam de tamanho e quantidade de fantasmas conforme o nível, com espaços vazios tratando-se como limites de colisão.
* **Fantasmas e superpontos:** Fantasmas com até 8 cores diferentes que perseguem o Pac-Man quando estão longe e fogem para os cantos quando chegam perto (a até 4 blocos) ou ficam vulneráveis ao comer superpontos (`O`). Ao serem comidos, retornam temporariamente inativos antes de voltarem ao normal.
* **Menu, seleção de fases e estados:** Tela inicial com fundo animado, grade clicável para escolher fases desbloqueadas, cursor pixel art que muda para mãozinha ao passar sobre botões ativos e telas de vitória e game over.

## Como executar

1. Instale o Pygame:
   ```bash
   pip install pygame
