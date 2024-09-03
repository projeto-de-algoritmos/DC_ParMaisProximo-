import pygame
import sys
import random
import math

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

RECT_WIDTH = 700
RECT_HEIGHT = 400

rect_x = (SCREEN_WIDTH - RECT_WIDTH) // 2
rect_y = (SCREEN_HEIGHT - RECT_HEIGHT) // 2

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Batalha Pontual")

font = pygame.font.Font(None, 36)

left_points = []
right_points = []
alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

num_points = 10 

def generate_random_points(num_points, x_start, x_end, y_start, y_end):
    points = []
    for i in range(num_points):
        x = random.randint(x_start, x_end)
        y = random.randint(y_start, y_end)
        letter = alphabet[i % len(alphabet)] 
        points.append({'position': (x, y), 'letter': letter})
    return points

def calculate_distance(point1, point2):
    x1, y1 = point1['position']
    x2, y2 = point2['position']
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

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

left_points = generate_random_points(num_points, rect_x, SCREEN_WIDTH // 2, rect_y, rect_y + RECT_HEIGHT)
right_points = generate_random_points(num_points, SCREEN_WIDTH // 2, rect_x + RECT_WIDTH, rect_y, rect_y + RECT_HEIGHT)

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

left_locked = False
right_locked = False

button_box_left = pygame.Rect(input_box_left.x + input_box_left.width + 10, input_box_left.y, 90, 32)
button_box_right = pygame.Rect(input_box_right.x + input_box_right.width + 10, input_box_right.y, 90, 32)
left_eliminated_letters = []
right_eliminated_letters = []

def update_message():
    global text_left, text_right, left_points, right_points, message, left_locked, right_locked

    if text_left.isdigit():
        input_distance = float(text_left)
        
        closest_pair_right = closest_pair_divide_and_conquer(right_points)
        _, _, min_distance_right = closest_pair_right
        
        if 0.90 * min_distance_right <= input_distance <= 1.05 * min_distance_right:
            message = f"Acertou! Distância: {min_distance_right:.2f}"
            right_eliminated_letters.append(closest_pair_right[0]['letter'])
            right_points.remove(closest_pair_right[0])
        else:
            message = f"Errou! A menor distância é {min_distance_right:.2f}"
        
        left_locked = False
        right_locked = False

    if text_right.isdigit():
        input_distance = float(text_right)
        
        closest_pair_left = closest_pair_divide_and_conquer(left_points)
        _, _, min_distance_left = closest_pair_left
        
        if 0.90 * min_distance_left <= input_distance <= 1.05 * min_distance_left:
            message = f"Acertou! Distância: {min_distance_left:.2f}"
            left_eliminated_letters.append(closest_pair_left[0]['letter'])
            left_points.remove(closest_pair_left[0])
        else:
            message = f"Errou!"
        
        right_locked = False
        left_locked = False

turn = 'left' 

def main():
    global text_left, text_right, active_left, active_right, input_color_left, input_color_right, left_points, right_points, message, left_locked, right_locked, turn

    while True:
        screen.fill(WHITE)


        pygame.draw.rect(screen, BLACK, (rect_x, rect_y, RECT_WIDTH, RECT_HEIGHT), 2)


        pygame.draw.line(screen, BLACK, (SCREEN_WIDTH // 2, rect_y), (SCREEN_WIDTH // 2, rect_y + RECT_HEIGHT), 2)


        for point in left_points:
            pygame.draw.circle(screen, RED, point['position'], 5)
            screen.blit(font.render(point['letter'], True, BLACK), (point['position'][0] + 10, point['position'][1] - 10))


        for point in right_points:
            pygame.draw.circle(screen, BLUE, point['position'], 5)
            screen.blit(font.render(point['letter'], True, BLACK), (point['position'][0] + 10, point['position'][1] - 10))


        pygame.draw.rect(screen, input_color_left, input_box_left, 2)
        pygame.draw.rect(screen, input_color_right, input_box_right, 2)
        screen.blit(font.render(text_left, True, BLACK), (input_box_left.x + 5, input_box_left.y + 5))
        screen.blit(font.render(text_right, True, BLACK), (input_box_right.x + 5, input_box_right.y + 5))


        pygame.draw.rect(screen, input_color_active if turn == 'left' else input_color_inactive, button_box_left)
        pygame.draw.rect(screen, input_color_active if turn == 'right' else input_color_inactive, button_box_right)

        button_text_left = font.render('atacar', True, WHITE)
        button_text_right = font.render('atacar', True, WHITE)
        screen.blit(button_text_left, (button_box_left.x + 10, button_box_left.y + 5))
        screen.blit(button_text_right, (button_box_right.x + 10, button_box_right.y + 5))


        if message:
            result_text = font.render(message, True, BLACK)
            screen.blit(result_text, (SCREEN_WIDTH - 600, SCREEN_HEIGHT - 550))


        eliminated_text_left = font.render('Pontos Eliminados: ' + ', '.join(left_eliminated_letters), True, RED)
        screen.blit(eliminated_text_left, (10, 10))


        eliminated_text_right = font.render('Pontos Eliminados: ' + ', '.join(right_eliminated_letters), True, BLUE)
        screen.blit(eliminated_text_right, (SCREEN_WIDTH - 320, 10))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_box_left.collidepoint(event.pos) and turn == 'left' and not left_locked:
                    left_locked = True
                    right_locked = False
                    update_message()
                    text_left = ''
                    turn = 'right'

                if button_box_right.collidepoint(event.pos) and turn == 'right' and not right_locked:
                    right_locked = True
                    left_locked = False
                    update_message()
                    text_right = ''
                    turn = 'left'

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
                    if event.key == pygame.K_RETURN:
                        update_message()
                        text_left = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_left = text_left[:-1]
                    else:
                        text_left += event.unicode

                if active_right:
                    if event.key == pygame.K_RETURN:
                        update_message()
                        text_right = ''
                    elif event.key == pygame.K_BACKSPACE:
                        text_right = text_right[:-1]
                    else:
                        text_right += event.unicode

if __name__ == "__main__":
    main()
