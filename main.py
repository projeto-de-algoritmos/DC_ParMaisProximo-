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

# Função de dividir e conquistar para encontrar o par de pontos mais próximo
def closest_pair_divide_and_conquer(points):
    def closest_pair_rec(sorted_x, sorted_y):
        if len(sorted_x) <= 3:
            return brute_force_closest_pair(sorted_x)
        
        mid = len(sorted_x) // 2
        midpoint = sorted_x[mid]['position'][0]
        
        left_x = sorted_x[:mid]
        right_x = sorted_x[mid:]
        
        midpoint_x = sorted_x[mid]['position'][0]
        
        left_y = list(filter(lambda p: p['position'][0] <= midpoint_x, sorted_y))
        right_y = list(filter(lambda p: p['position'][0] > midpoint_x, sorted_y))
        
        (p1_left, p2_left, dist_left) = closest_pair_rec(left_x, left_y)
        (p1_right, p2_right, dist_right) = closest_pair_rec(right_x, right_y)
        
        min_pair = (p1_left, p2_left) if dist_left < dist_right else (p1_right, p2_right)
        min_dist = min(dist_left, dist_right)
        
        in_strip = [p for p in sorted_y if abs(p['position'][0] - midpoint) < min_dist]
        
        for i in range(len(in_strip)):
            for j in range(i + 1, min(i + 7, len(in_strip))):
                p1, p2 = in_strip[i], in_strip[j]
                dist = calculate_distance(p1, p2)
                if dist < min_dist:
                    min_dist = dist
                    min_pair = (p1, p2)
        
        return min_pair[0], min_pair[1], min_dist
    
    sorted_x = sorted(points, key=lambda p: p['position'][0])
    sorted_y = sorted(points, key=lambda p: p['position'][1])
    
    return closest_pair_rec(sorted_x, sorted_y)

# Função de força bruta para encontrar o par de pontos mais próximo
def brute_force_closest_pair(points):
    min_dist = float('inf')
    p1 = None
    p2 = None
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            dist = calculate_distance(points[i], points[j])
            if dist < min_dist:
                min_dist = dist
                p1, p2 = points[i], points[j]
    return p1, p2, min_dist

# Gerando pontos para o lado esquerdo do retângulo
left_points = generate_random_points(num_points, rect_x, SCREEN_WIDTH // 2, rect_y, rect_y + RECT_HEIGHT)

# Gerando pontos para o lado direito do retângulo
right_points = generate_random_points(num_points, SCREEN_WIDTH // 2, rect_x + RECT_WIDTH, rect_y, rect_y + RECT_HEIGHT)

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
message = ""

# Controle de bloqueio
left_locked = False
right_locked = False

# Função para atualizar a mensagem de resultado ao digitar
def update_message():
    global text_left, text_right, left_points, right_points, message, left_locked, right_locked

    if text_left.isdigit():
        input_distance = float(text_left)
        
        closest_pair_right = closest_pair_divide_and_conquer(right_points)
        _, _, min_distance_right = closest_pair_right
        
        if input_distance >= 0.9 * min_distance_right:
            message = f"Acertou! Distância: {min_distance_right:.2f}"
            right_points.remove(closest_pair_right[0])
        else:
            message = f"Errou! A menor distância é {min_distance_right:.2f}"
        
        left_locked = True
        right_locked = False

    if text_right.isdigit():
        input_distance = float(text_right)
        
        closest_pair_left = closest_pair_divide_and_conquer(left_points)
        _, _, min_distance_left = closest_pair_left
        
        if input_distance >= 0.9 * min_distance_left:
            message = f"Acertou! Distância: {min_distance_left:.2f}"
            left_points.remove(closest_pair_left[0])
        else:
            message = f"Errou! A menor distância é {min_distance_left:.2f}"
        
        right_locked = True
        left_locked = False

# Loop principal
def main():
    global text_left, text_right, active_left, active_right, input_color_left, input_color_right, left_points, right_points, message, left_locked, right_locked

    while True:
        screen.fill(WHITE)

        # Desenha o retângulo central
        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)

        # Desenha a linha vertical dentro do retângulo
        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, rect_y), (SCREEN_WIDTH // 2, rect_y + RECT_HEIGHT), 2)

        # Desenha os pontos gerados aleatoriamente
        for point in left_points:
            pygame.draw.circle(screen, RED, point['position'], 5)
            screen.blit(font.render(point['letter'], True, BLACK), (point['position'][0] + 10, point['position'][1] - 10))
        
        for point in right_points:
            pygame.draw.circle(screen, BLUE, point['position'], 5)
            screen.blit(font.render(point['letter'], True, BLACK), (point['position'][0] + 10, point['position'][1] - 10))

        # Desenha os campos de entrada
        pygame.draw.rect(screen, input_color_left, input_box_left, 2)
        pygame.draw.rect(screen, input_color_right, input_box_right, 2)
        screen.blit(font.render(text_left, True, BLACK), (input_box_left.x + 5, input_box_left.y + 5))
        screen.blit(font.render(text_right, True, BLACK), (input_box_right.x + 5, input_box_right.y + 5))

        # Desenha a mensagem de resultado
        if message:
            result_text = font.render(message, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH - 240, SCREEN_HEIGHT - 100))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Verifica se clicou nos campos de entrada
                if input_box_left.collidepoint(event.pos) and not left_locked:
                    active_left = True
                    active_right = False
                elif input_box_right.collidepoint(event.pos) and not right_locked:
                    active_right = True
                    active_left = False
                else:
                    active_left = False
                    active_right = False

                input_color_left = input_color_active if active_left else input_color_inactive
                input_color_right = input_color_active if active_right else input_color_inactive

            if event.type == pygame.KEYDOWN:
                if active_left and not left_locked:
                    if event.key == pygame.K_BACKSPACE:
                        text_left = text_left[:-1]
                    else:
                        text_left += event.unicode
                    update_message()

                elif active_right and not right_locked:
                    if event.key == pygame.K_BACKSPACE:
                        text_right = text_right[:-1]
                    else:
                        text_right += event.unicode
                    update_message()

        pygame.display.flip()

if __name__ == "__main__":
    main()
