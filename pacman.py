import pygame
import sys
import random

# --- Configurações Iniciais ---
pygame.init()

TILE_SIZE = 40
COLS, ROWS = 19, 11
WIDTH = COLS * TILE_SIZE
HEIGHT = ROWS * TILE_SIZE
FPS = 60

# Cores
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (135, 206, 250)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Lista com 8 cores para os fantasmas
CORES_FANTASMAS = [
    (255, 0, 0),       # Vermelho
    (255, 184, 255),   # Rosa
    (0, 255, 255),     # Ciano
    (255, 184, 82),    # Laranja
    (0, 255, 0),       # Verde
    (160, 32, 240),    # Roxo
    (255, 255, 255),   # Branco
    (139, 69, 19)      # Marrom
]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Arcade")
clock = pygame.time.Clock()

pygame.mouse.set_visible(False) # Esconde o mouse padrão do sistema

fonte_normal = pygame.font.SysFont(None, 36)
fonte_grande = pygame.font.SysFont(None, 55)

# --- Matrizes dos cursores Retro (Seta e Mão) ---
CURSOR_SETA = [
    "X         ",
    "XX        ",
    "X.X       ",
    "X..X      ",
    "X...X     ",
    "X....X    ",
    "X.....X   ",
    "X......X  ",
    "X.......X ",
    "X....XXXXX",
    "X..X.X    ",
    "X.X X.X   ",
    "XX  X.X   ",
    "     XX   "
]

CURSOR_MAO = [
    "   XX     ",
    "  X..X    ",
    "  X..X    ",
    "  X..X XX ",
    "  X..XX..X",
    " XX..X...X",
    "X........X",
    "X........X",
    " X.......X",
    "  X......X",
    "   XXXXXX "
]

# --- Definição das Fases ---

# Fase 1: Pequena (2 Fantasmas)
FASE_1 = [
    "                   ",
    "                   ",
    "  ###############  ",
    "  #O.....P.....O#  ",
    "  #.####.#.####.#  ",
    "  #...G.....G...#  ",
    "  #.####.#.####.#  ",
    "  #O...........O#  ",
    "  ###############  ",
    "                   ",
    "                   "
]

# Fase 2: Média (4 Fantasmas)
FASE_2 = [
    "                   ",
    " ################# ",
    " #O......P......O# ",
    " #.#####.#.#####.# ",
    " #G#...........#G# ",
    " #.#.###...###.#.# ",
    " #...G.......G...# ",
    " #.#############.# ",
    " #O.............O# ",
    " ################# ",
    "                   "
]

# Fase 3: Grande (6 Fantasmas)
FASE_3 = [
    "###################",
    "#O.......P.......O#",
    "#.###.#######.###.#",
    "#G#.............#G#",
    "#.#.###.###.###.#.#",
    "#G......#.#......G#",
    "#####.#.###.#.#####",
    "#O....#G...G#....O#",
    "#.###############.#",
    "#O...............O#",
    "###################"
]

# Fase 4: O Caos Total (8 Fantasmas espalhados)
FASE_4 = [
    "###################",
    "#O...G...P...G...O#",
    "#.###.#######.###.#",
    "#G#.............#G#",
    "#.#.###.###.###.#.#",
    "#.......#.#.......#",
    "#####.#.###.#.#####",
    "#O..G.#G...G#.G..O#",
    "#.###############.#",
    "#O...............O#",
    "###################"
]

# A grade de fases no menu (repetindo as últimas para fechar 6 botões)
FASES = [FASE_1, FASE_2, FASE_3, FASE_4, FASE_3, FASE_4]

# --- Funções Visuais (Fundo e Mouse) ---
def desenhar_cursor_retro(hover=False):
    mx, my = pygame.mouse.get_pos()
    pixels = CURSOR_MAO if hover else CURSOR_SETA
    escala = 3
    
    offset_x = -5 if hover else 0 
    offset_y = -5 if hover else 0
    
    for y, linha in enumerate(pixels):
        for x, char in enumerate(linha):
            px, py = mx + offset_x + x * escala, my + offset_y + y * escala
            if char == 'X':
                pygame.draw.rect(screen, BLACK, (px, py, escala, escala))
            elif char == '.':
                pygame.draw.rect(screen, WHITE, (px, py, escala, escala))

def desenhar_fundo_animado(tempo_atual):
    # Grade de fundo em movimento (Neon Retrô)
    deslocamento = (tempo_atual // 30) % TILE_SIZE
    for y in range(0, HEIGHT + TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (20, 20, 35), (0, y + deslocamento), (WIDTH, y + deslocamento))
    for x in range(0, WIDTH + TILE_SIZE, TILE_SIZE):
        pygame.draw.line(screen, (20, 20, 35), (x + deslocamento, 0), (x + deslocamento, HEIGHT))

    # Animação no rodapé: Pac-Man escuro sendo perseguido
    pos_x = (tempo_atual // 5) % (WIDTH + 400) - 200
    cy = HEIGHT - 40
    
    # Pac-Man (Cores mais escuras pra não atrapalhar o texto do menu)
    pygame.draw.circle(screen, (100, 100, 0), (pos_x, cy), 60)
    if (tempo_atual // 250) % 2 == 0: 
        pygame.draw.polygon(screen, BLACK, [(pos_x, cy), (pos_x+70, cy-40), (pos_x+70, cy+40)])
    
    # Fantasma
    gx = pos_x - 150
    pygame.draw.circle(screen, (0, 0, 100), (gx, cy - 20), 50)
    pygame.draw.rect(screen, (0, 0, 100), (gx - 50, cy - 20, 100, 70))
    pygame.draw.circle(screen, (180, 180, 180), (gx - 20, cy - 20), 10)
    pygame.draw.circle(screen, (180, 180, 180), (gx + 20, cy - 20), 10)
    pygame.draw.circle(screen, (100, 100, 0), (gx - 20, cy - 20), 4)
    pygame.draw.circle(screen, (100, 100, 0), (gx + 20, cy - 20), 4)
    pygame.draw.polygon(screen, (180, 180, 180), [(gx-20, cy+20), (gx-10, cy+10), (gx, cy+20), (gx+10, cy+10), (gx+20, cy+20)], 3)


# --- Classes ---
class Pacman:
    def __init__(self, col, row):
        self.col, self.row = col, row
        self.px, self.py = col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2
        self.dir_x, self.dir_y, self.prox_dir_x, self.prox_dir_y = 0, 0, 0, 0
        self.vel = 2  

    def mover(self, limites_colisao):
        centro_x, centro_y = self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2
        if self.px == centro_x and self.py == centro_y:
            if (self.col + self.prox_dir_x, self.row + self.prox_dir_y) not in limites_colisao:
                self.dir_x, self.dir_y = self.prox_dir_x, self.prox_dir_y
            if (self.col + self.dir_x, self.row + self.dir_y) in limites_colisao:
                self.dir_x, self.dir_y = 0, 0

        self.px += self.dir_x * self.vel
        self.py += self.dir_y * self.vel
        self.col, self.row = self.px // TILE_SIZE, self.py // TILE_SIZE

    def desenhar(self, surface, tempo_atual):
        raio = TILE_SIZE // 2 - 4
        pygame.draw.circle(surface, YELLOW, (self.px, self.py), raio)
        if (tempo_atual // 150) % 2 == 0 and (self.dir_x != 0 or self.dir_y != 0):
            if self.dir_x == 1: pontos = [(self.px, self.py), (self.px+raio, self.py-raio), (self.px+raio, self.py+raio)]
            elif self.dir_x == -1: pontos = [(self.px, self.py), (self.px-raio, self.py-raio), (self.px-raio, self.py+raio)]
            elif self.dir_y == -1: pontos = [(self.px, self.py), (self.px-raio, self.py-raio), (self.px+raio, self.py-raio)]
            elif self.dir_y == 1: pontos = [(self.px, self.py), (self.px-raio, self.py+raio), (self.px+raio, self.py+raio)]
            pygame.draw.polygon(surface, BLACK, pontos)


class Fantasma:
    def __init__(self, col, row, canto_x, canto_y, cor):
        self.start_col, self.start_row = col, row
        self.col, self.row = col, row
        self.px, self.py = col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2
        self.dir_x, self.dir_y = 1, 0
        self.vel = 2
        self.canto_x, self.canto_y = canto_x, canto_y
        self.cor = cor
        self.vulneravel_ate = 0
        self.morto_ate = 0

    def renascer(self, tempo_atual):
        self.col, self.row = self.start_col, self.start_row
        self.px, self.py = self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2
        self.vulneravel_ate = 0
        self.morto_ate = tempo_atual + 3000

    def mover(self, pacman, limites_colisao, tempo_atual):
        centro_x, centro_y = self.col * TILE_SIZE + TILE_SIZE // 2, self.row * TILE_SIZE + TILE_SIZE // 2
        if self.px == centro_x and self.py == centro_y:
            opcoes = []
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                if (self.col + dx, self.row + dy) not in limites_colisao:
                    if not (dx == -self.dir_x and dy == -self.dir_y and (self.dir_x != 0 or self.dir_y != 0)):
                        opcoes.append((dx, dy))
            if not opcoes: opcoes = [(-self.dir_x, -self.dir_y)]
                
            if self.vulneravel_ate > tempo_atual:
                alvo_c, alvo_r = self.canto_x, self.canto_y 
            else:
                dist = abs(self.col - pacman.col) + abs(self.row - pacman.row)
                alvo_c, alvo_r = (self.canto_x, self.canto_y) if dist <= 4 else (pacman.col, pacman.row)

            melhor_opcao, menor_dist = random.choice(opcoes), 9999
            for dx, dy in opcoes:
                dist = abs((self.col + dx) - alvo_c) + abs((self.row + dy) - alvo_r)
                if dist < menor_dist:
                    menor_dist, melhor_opcao = dist, (dx, dy)
                    
            self.dir_x, self.dir_y = melhor_opcao

        self.px += self.dir_x * self.vel
        self.py += self.dir_y * self.vel
        self.col, self.row = self.px // TILE_SIZE, self.py // TILE_SIZE

    def desenhar(self, surface, tempo_atual):
        if self.morto_ate > tempo_atual:
            pygame.draw.circle(surface, WHITE, (self.px - 5, self.py - 6), 4)
            pygame.draw.circle(surface, WHITE, (self.px + 5, self.py - 6), 4)
            pygame.draw.circle(surface, BLUE, (self.px - 5, self.py - 6), 2)
            pygame.draw.circle(surface, BLUE, (self.px + 5, self.py - 6), 2)
            return

        vulneravel = self.vulneravel_ate > tempo_atual
        c = BLUE if vulneravel else self.cor
        raio = TILE_SIZE // 2 - 4
        
        pygame.draw.circle(surface, c, (self.px, self.py - 4), raio)
        pygame.draw.rect(surface, c, (self.px - raio, self.py - 4, raio * 2, raio + 4))
        base_y = self.py + raio
        pygame.draw.polygon(surface, c, [
            (self.px - raio, base_y), (self.px - raio//2, base_y + 5), (self.px, base_y), 
            (self.px + raio//2, base_y + 5), (self.px + raio, base_y)
        ])
        
        if vulneravel:
            pygame.draw.circle(surface, WHITE, (self.px - 4, self.py - 5), 3)
            pygame.draw.circle(surface, WHITE, (self.px + 4, self.py - 5), 3)
        else:
            pygame.draw.circle(surface, WHITE, (self.px - 5, self.py - 6), 4)
            pygame.draw.circle(surface, WHITE, (self.px + 5, self.py - 6), 4)
            pygame.draw.circle(surface, BLUE, (self.px - 5, self.py - 6), 2)
            pygame.draw.circle(surface, BLUE, (self.px + 5, self.py - 6), 2)


class Jogo:
    def __init__(self):
        self.estado = "MENU"
        self.fase_atual = 0
        self.pontuacao = 0
        self.fases_desbloqueadas = 1 
        self.botoes_fases = [] 

    def iniciar_jogo(self, fase_index):
        self.fase_atual = fase_index
        self.pontuacao = 0 
        self.carregar_fase()
        self.estado = "JOGANDO"

    def carregar_fase(self):
        mapa = FASES[self.fase_atual]
        self.paredes_visiveis = set()
        self.limites_colisao = set()
        self.pontos, self.super_pontos, self.fantasmas = set(), set(), []
        cantos_fuga = [(0, 0), (COLS-1, ROWS-1), (COLS-1, 0), (0, ROWS-1)]
        idx_fantasma = 0
        
        for r, linha in enumerate(mapa):
            for c, char in enumerate(linha):
                if char == '#': 
                    self.paredes_visiveis.add((c, r)); self.limites_colisao.add((c, r))
                elif char == ' ': self.limites_colisao.add((c, r))
                elif char == '.': self.pontos.add((c, r))
                elif char == 'O': self.super_pontos.add((c, r))
                elif char == 'P': self.pacman = Pacman(c, r)
                elif char == 'G':
                    cor = CORES_FANTASMAS[idx_fantasma % len(CORES_FANTASMAS)]
                    canto_x = cantos_fuga[idx_fantasma % 4][0]
                    canto_y = cantos_fuga[idx_fantasma % 4][1]
                    self.fantasmas.append(Fantasma(c, r, canto_x, canto_y, cor))
                    idx_fantasma += 1

    def desenhar_tela_selecao(self, pos_mouse):
        self.botoes_fases.clear()
        self.desenhar_texto_centralizado("SELECIONE A FASE", YELLOW, -150)
        
        tamanho_botao = 80
        margem = 20
        colunas = 3 
        offset_x = (WIDTH - (colunas * tamanho_botao + (colunas - 1) * margem)) // 2
        offset_y = 100
        
        mouse_hover_em_algum = False

        for i in range(len(FASES)):
            col = i % colunas
            row = i // colunas
            x = offset_x + col * (tamanho_botao + margem)
            y = offset_y + row * (tamanho_botao + margem)
            
            rect = pygame.Rect(x, y, tamanho_botao, tamanho_botao)
            desbloqueada = i < self.fases_desbloqueadas
            
            hover = rect.collidepoint(pos_mouse) and desbloqueada
            
            if hover:
                mouse_hover_em_algum = True
                rect.inflate_ip(10, 10)
            
            cor_fundo = LIGHT_BLUE if desbloqueada else GRAY
            cor_borda = YELLOW if hover else WHITE 
            espessura_borda = 6 if hover else 3

            pygame.draw.rect(screen, cor_fundo, rect, border_radius=15)
            pygame.draw.rect(screen, cor_borda, rect, espessura_borda, border_radius=15)
            
            texto = fonte_grande.render(str(i + 1), True, BLACK)
            screen.blit(texto, texto.get_rect(center=rect.center))
            
            self.botoes_fases.append((rect, i))

        self.desenhar_texto_centralizado("Pressione [ESC] para Menu", WHITE, 200, fonte_normal)
        return mouse_hover_em_algum

    def desenhar_mapa(self, tempo_atual):
        for c, r in self.paredes_visiveis: pygame.draw.rect(screen, BLUE, (c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
        for c, r in self.pontos: pygame.draw.circle(screen, WHITE, (c * TILE_SIZE + 20, r * TILE_SIZE + 20), 4)
        for c, r in self.super_pontos:
            if (tempo_atual // 250) % 2 == 0: pygame.draw.circle(screen, WHITE, (c * TILE_SIZE + 20, r * TILE_SIZE + 20), 8)

    def desenhar_texto_centralizado(self, texto, cor, offset_y=0, fonte=fonte_grande):
        screen.blit(fonte.render(texto, True, cor), fonte.render(texto, True, cor).get_rect(center=(WIDTH // 2, HEIGHT // 2 + offset_y)))

    def atualizar(self, tempo_atual):
        self.pacman.mover(self.limites_colisao)
        for fantasma in self.fantasmas:
            if fantasma.morto_ate > tempo_atual: continue
            fantasma.mover(self.pacman, self.limites_colisao, tempo_atual)
            if abs(self.pacman.px - fantasma.px) < 15 and abs(self.pacman.py - fantasma.py) < 15:
                if fantasma.vulneravel_ate > tempo_atual:
                    self.pontuacao += 200 
                    fantasma.renascer(tempo_atual)
                else: self.estado = "GAME_OVER"

        if self.estado == "GAME_OVER": return
        
        pos_celula = (self.pacman.col, self.pacman.row)
        if pos_celula in self.pontos: self.pontos.remove(pos_celula); self.pontuacao += 10
        if pos_celula in self.super_pontos:
            self.super_pontos.remove(pos_celula); self.pontuacao += 50
            for f in self.fantasmas:
                if f.morto_ate <= tempo_atual: f.vulneravel_ate = tempo_atual + 6000 
                
        if len(self.pontos) == 0 and len(self.super_pontos) == 0:
            if self.fase_atual + 1 >= self.fases_desbloqueadas:
                self.fases_desbloqueadas = self.fase_atual + 2
            self.estado = "VITORIA"

# --- Loop Principal ---
jogo = Jogo()

while True:
    tempo_atual = pygame.time.get_ticks()
    pos_mouse = pygame.mouse.get_pos()
    is_hovering = False 
    
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and jogo.estado == "SELECAO_FASE":
                for rect, fase_index in jogo.botoes_fases:
                    if rect.collidepoint(pos_mouse) and fase_index < jogo.fases_desbloqueadas:
                        jogo.iniciar_jogo(fase_index)

        elif event.type == pygame.KEYDOWN:
            if jogo.estado == "MENU":
                if event.key == pygame.K_RETURN: jogo.estado = "SELECAO_FASE"
            elif jogo.estado == "SELECAO_FASE":
                if event.key == pygame.K_ESCAPE: jogo.estado = "MENU"
            elif jogo.estado == "JOGANDO":
                if event.key == pygame.K_UP: jogo.pacman.prox_dir_x, jogo.pacman.prox_dir_y = 0, -1
                elif event.key == pygame.K_DOWN: jogo.pacman.prox_dir_x, jogo.pacman.prox_dir_y = 0, 1
                elif event.key == pygame.K_LEFT: jogo.pacman.prox_dir_x, jogo.pacman.prox_dir_y = -1, 0
                elif event.key == pygame.K_RIGHT: jogo.pacman.prox_dir_x, jogo.pacman.prox_dir_y = 1, 0
            elif jogo.estado in ["VITORIA", "GAME_OVER", "FIM_DE_JOGO"]:
                if event.key == pygame.K_SPACE: jogo.estado = "SELECAO_FASE"

    # --- Renderização ---
    if jogo.estado == "MENU":
        desenhar_fundo_animado(tempo_atual)
        jogo.desenhar_texto_centralizado("PAC-MAN ARCADE", YELLOW, -30)
        jogo.desenhar_texto_centralizado("Pressione [ENTER] para Jogar", WHITE, 30, fonte_normal)
        desenhar_cursor_retro(False)

    elif jogo.estado == "SELECAO_FASE":
        desenhar_fundo_animado(tempo_atual)
        is_hovering = jogo.desenhar_tela_selecao(pos_mouse) 
        desenhar_cursor_retro(is_hovering)

    elif jogo.estado == "JOGANDO":
        jogo.atualizar(tempo_atual)
        jogo.desenhar_mapa(tempo_atual)
        for fantasma in jogo.fantasmas: fantasma.desenhar(screen, tempo_atual)
        jogo.pacman.desenhar(screen, tempo_atual)
        screen.blit(fonte_normal.render(f"Pontos: {jogo.pontuacao}  Fase: {jogo.fase_atual + 1}", True, WHITE), (10, 10))

    elif jogo.estado == "VITORIA":
        jogo.desenhar_texto_centralizado("FASE CONCLUÍDA!", GREEN, -30)
        jogo.desenhar_texto_centralizado("Pressione [ESPAÇO] para Fases", WHITE, 30, fonte_normal)
        desenhar_cursor_retro(False)

    elif jogo.estado == "GAME_OVER":
        jogo.desenhar_texto_centralizado("GAME OVER", RED, -30)
        jogo.desenhar_texto_centralizado("Pressione [ESPAÇO] para Fases", WHITE, 30, fonte_normal)
        desenhar_cursor_retro(False)

    pygame.display.flip()
    clock.tick(FPS)