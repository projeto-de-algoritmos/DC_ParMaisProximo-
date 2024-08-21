import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Dimensões do retângulo central
RECT_WIDTH = 700
RECT_HEIGHT = 200

# Posição do retângulo central
rect_x = (SCREEN_WIDTH - RECT_WIDTH) // 2
rect_y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2

# Inicializando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batalha Naval Simplificada")

# Fonte para desenhar as letras e coordenadas
font = pygame.font.Font(None, 36)

# Array para armazenar as posições e letras
points = []
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letter_index = 0

# Campos de entrada de texto
input_box_left = pygame.Rect(100, SCREEN_HEIGHT - 50, 140, 32)
input_box_right = pygame.Rect(SCREEN_WIDTH - 240, SCREEN_HEIGHT - 50, 140, 32)
input_color_active = pygame.Color('dodgerblue2')
input_color_inactive = pygame.Color('lightskyblue3')
input_color_left = input_color_inactive
input_color_right = input_color_inactive
text_left = ''
text_right = ''
active_left = False
active_right = False

# Função para desenhar as coordenadas
def draw_coordinates(letter, side):
    for point in points:
        if point['letter'] == letter.upper():
            coords = f"({point['position'][0]}, {point['position'][1]})"
            if side == 'left':
                screen.blit(font.render(coords, True, BLACK), (100, SCREEN_HEIGHT - 100))
            elif side == 'right':
                screen.blit(font.render(coords, True, BLACK), (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 100))

# Loop principal
def main():
    global letter_index, text_left, text_right, active_left, active_right, input_color_left, input_color_right

    while True:
        screen.fill(WHITE)

        # Desenha o retângulo central
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)

        # Desenha a linha vertical dentro do retângulo
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, rect_y), (SCREEN_WIDTH // 2, rect_y + RECT_HEIGHT), 2)

        # Desenha os pontos e letras
        for point in points:
            pygame.draw.circle(screen, RED, point['position'], 5)
            letter_surface = font.render(point['letter'], True, BLACK)
            screen.blit(letter_surface, (point['position'][0] + 10, point['position'][1] - 10))

        # Desenha os campos de entrada
        pygame.draw.rect(screen, input_color_left, input_box_left, 2)
        pygame.draw.rect(screen, input_color_right, input_box_right, 2)
        screen.blit(font.render(text_left, True, BLACK), (input_box_left.x + 5, input_box_left.y + 5))
        screen.blit(font.render(text_right, True, BLACK), (input_box_right.x + 5, input_box_right.y + 5))

        # Desenha as coordenadas dos pontos associados às letras digitadas
        if text_left:
            draw_coordinates(text_left, 'left')
        if text_right:
            draw_coordinates(text_right, 'right')

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verifica se clicou nos campos de entrada
                if input_box_left.collidepoint(event.pos):
                    active_left = True
                    active_right = False
                elif input_box_right.collidepoint(event.pos):
                    active_right = True
                    active_left = False
                else:
                    active_left = False
                    active_right = False

                input_color_left = input_color_active if active_left else input_color_inactive
                input_color_right = input_color_active if active_right else input_color_inactive

                # Adiciona o ponto e a letra ao array se o clique estiver dentro do retângulo
                if rect_x <= mouse_pos[0] <= rect_x + RECT_WIDTH and rect_y <= mouse_pos[1] <= rect_y + RECT_HEIGHT:
                    if letter_index < len(alphabet):
                        points.append({
                            'position': mouse_pos,
                            'letter': alphabet[letter_index]
                        })
                        letter_index += 1

            if event.type == pygame.KEYDOWN:
                if active_left:
                    if event.key == pygame.K_BACKSPACE:
                        text_left = text_left[:-1]
                    else:
                        text_left += event.unicode
                elif active_right:
                    if event.key == pygame.K_BACKSPACE:
                        text_right = text_right[:-1]
                    else:
                        text_right += event.unicode

        pygame.display.flip()

if __name__ == "__main__":
    main()
