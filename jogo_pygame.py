import pygame
import sys
import time
from mundo import Mundo
from agente import Agente
from sensores import sensores
from testes import obter_percepcoes

pygame.init()

TAMANHO_CELULA = 100
TAMANHO = 4
WIDTH = HEIGHT = TAMANHO * TAMANHO_CELULA
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mundo de Wumpus")

# Recursos visuais e sonoros
img_agente = pygame.image.load("imagens/agente.png")
img_ouro = pygame.image.load("imagens/ouro.png")
img_poco = pygame.image.load("imagens/poco.png")
img_wumpus = pygame.image.load("imagens/wumpus.png")

som_ouro = pygame.mixer.Sound("sons/ouro.wav")
som_poco = pygame.mixer.Sound("sons/poco.wav")
som_wumpus = pygame.mixer.Sound("sons/wumpus.wav")

fonte = pygame.font.SysFont(None, 48)

def desenhar_texto(texto, x, y, cor=(0,0,0)):
    texto_render = fonte.render(texto, True, cor)
    screen.blit(texto_render, (x, y))

def menu_inicial():
    while True:
        screen.fill((255, 255, 255))
        desenhar_texto("Mundo de Wumpus", 80, 100)
        desenhar_texto("Clique para Jogar", 100, 200)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return

def animacao_entrada(agente):
    for i in range(3):
        screen.fill((255, 255, 255))
        pygame.display.flip()
        time.sleep(0.3)
        desenhar_mapa(matriz, agente)
        time.sleep(0.3)

def desenhar_mapa(mundo, agente):
    screen.fill((255, 255, 255))
    for i in range(len(mundo)):
        for j in range(len(mundo[i])):
            x = j * TAMANHO_CELULA
            y = i * TAMANHO_CELULA
            pygame.draw.rect(screen, (200, 200, 200), (x, y, TAMANHO_CELULA, TAMANHO_CELULA), 1)

    # Mostrar apenas o agente
    ax, ay = agente.pos
    screen.blit(pygame.transform.scale(img_agente, (100, 100)), (ay*TAMANHO_CELULA, ax*TAMANHO_CELULA))
    pygame.display.flip()


def main():
    menu_inicial()

    global matriz
    TAMANHO_MUNDO = 4
    mundo = Mundo(TAMANHO_MUNDO)
    agente = Agente()
    matriz = mundo.matriz

    clock = pygame.time.Clock()
    animacao_entrada(agente)
    running = True

    while running and agente.vivo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        desenhar_mapa(matriz, agente)
        time.sleep(0.4)

        percepcoes = obter_percepcoes(matriz, agente.pos)
        acao = agente.decidir_acao(percepcoes)
        print(f"Ação: {acao}, Posição: {agente.pos}, Percepções: {percepcoes}")
        terminou = agente.executar_acao(acao, matriz)

        x, y = agente.pos
        if matriz[x][y] == "W":
            som_wumpus.play()
            print("O agente encontrou o Wumpus! Game Over!")
            break
        elif matriz[x][y] == "P":
            som_poco.play()
            print("O agente caiu em um poço! Game Over!")
            break
        elif terminou:
            som_ouro.play()
            break

        clock.tick(2)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
