import pygame
import sys
import random
import math

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
RECT_HEIGHT = 400

# Posição do retângulo central
rect_x = (SCREEN_WIDTH - RECT_WIDTH) // 2
rect_y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2

# Inicializando a tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batalha Naval Simplificada")

# Fonte para desenhar as letras e coordenadas
font = pygame.font.Font(None, 36)

# Arrays para armazenar as posições e letras
left_points = []
right_points = []
all_points = []
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Definindo a quantidade de pontos a serem gerados em cada lado do retângulo
num_points = 10  # Você pode alterar este valor conforme necessário

# Função para gerar pontos aleatórios dentro de um retângulo
def generate_random_points(num_points, x_start, x_end, y_start, y_end):
    points = []
    for i in range(num_points):
        x = random.randint(x_start, x_end)
        y = random.randint(y_start, y_end)
        letter = alphabet[i % len(alphabet)]  # Gira o alfabeto se necessário
        points.append({'position': (x, y), 'letter': letter})
    return points

# Função para calcular a distância entre dois pontos
def calculate_distance(point1, point2):
    x1, y1 = point1['position']
    x2, y2 = point2['position']
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# Função para encontrar o par de pontos mais próximo
def find_closest_pairs(points):
    closest_pairs = []
    available_points = points.copy()
    
    while available_points:
        point = available_points.pop(0)
        closest = None
        min_distance = float('inf')
        
        for other_point in available_points:
            distance = calculate_distance(point, other_point)
            if distance < min_distance:
                min_distance = distance
                closest = other_point
        
        if closest:
            available_points.remove(closest)
            closest_pairs.append((point, closest))
    
    return closest_pairs

# Gerando pontos para o lado esquerdo do retângulo
left_points = generate_random_points(num_points, rect_x, SCREEN_WIDTH // 2, rect_y, rect_y + RECT_HEIGHT)

# Gerando pontos para o lado direito do retângulo
right_points = generate_random_points(num_points, SCREEN_WIDTH // 2, rect_x + RECT_WIDTH, rect_y, rect_y + RECT_HEIGHT)

# Unindo todos os pontos e embaralhando a ordem
all_points = left_points + right_points
random.shuffle(all_points)

# Encontrando pares mais próximos
closest_pairs = find_closest_pairs(all_points)

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
    points = left_points if side == 'left' else right_points

    for point in points:
        if point['letter'] == letter.upper():
            coords = f"({point['position'][0]}, {point['position'][1]})"
            if side == 'left':
                screen.blit(font.render(coords, True, BLACK), (100, SCREEN_HEIGHT - 100))
            elif side == 'right':
                screen.blit(font.render(coords, True, BLACK), (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 100))

# Loop principal
def main():
    global text_left, text_right, active_left, active_right, input_color_left, input_color_right

    while True:
        screen.fill(WHITE)

        # Desenha o retângulo central
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)

        # Desenha a linha vertical dentro do retângulo
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, rect_y), (SCREEN_WIDTH // 2, rect_y + RECT_HEIGHT), 2)

        # Desenha os pontos e letras para os pares mais próximos
        for pair in closest_pairs:
            for point in pair:
                pygame.draw.circle(screen, RED if point in left_points else BLUE, point['position'], 5)
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
