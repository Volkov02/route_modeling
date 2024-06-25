import pygame
import math

# Инициализация Pygame
pygame.init()

# Задание параметров окна
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Моделирование маршрута")

# Цвет
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
grey = (200, 200, 200)

# Переменные для рисования
drawing = False
key_points = []

def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

def draw_axes(screen, width, height):
    font = pygame.font.Font(None, 24)
    
    # Ось X
    pygame.draw.line(screen, black, (50, height - 50), (width, height - 50), 2)
    # Ось Y
    pygame.draw.line(screen, black, (50, height - 50), (50, 0), 2)

    # Метки на оси X
    for x in range(50, width, 50):
        pygame.draw.line(screen, black, (x, height - 45), (x, height - 55), 2)
        label = font.render(str(x - 50), True, black)
        screen.blit(label, (x - 10, height - 40))

    # Метки на оси Y
    for y in range(height - 50, 0, -50):
        pygame.draw.line(screen, black, (45, y), (55, y), 2)
        label = font.render(str(height - 50 - y), True, black)
        screen.blit(label, (10, y - 10))

def transform_to_coords(point):
    return (point[0] - 50, height - 50 - point[1])

def draw_button(screen, x, y, w, h, text, color):
    pygame.draw.rect(screen, color, (x, y, w, h))
    font = pygame.font.Font(None, 24)
    label = font.render(text, True, black)
    screen.blit(label, (x + 5, y + 5))

# Главный цикл программы
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Левая кнопка мыши
                mouse_pos = event.pos
                if 10 <= mouse_pos[0] <= 90 and 10 <= mouse_pos[1] <= 40:
                    # Кнопка "Очистить"
                    key_points = []
                elif 100 <= mouse_pos[0] <= 180 and 10 <= mouse_pos[1] <= 40:
                    # Кнопка "Сохранить"
                    with open('key_points.txt', 'w') as f:
                        for key_point in key_points:
                            coords = transform_to_coords(key_point)
                            f.write(f"{coords[0]}, {coords[1]}\n")
                    print("Ключевые точки сохранены в файл key_points.txt")
                else:
                    drawing = True
                    if not key_points or distance(event.pos, key_points[-1]) >= 40:
                        key_points.append(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Левая кнопка мыши
                drawing = False
        elif event.type == pygame.MOUSEMOTION:
            if drawing:
                if not key_points or distance(event.pos, key_points[-1]) >= 40:
                    key_points.append(event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # Очистка экрана
    screen.fill(white)

    # Рисование системы координат
    draw_axes(screen, width, height)

    # Рисование ключевых точек
    if len(key_points) > 1:
        pygame.draw.lines(screen, red, False, key_points, 2)
    for key_point in key_points:
        pygame.draw.circle(screen, blue, key_point, 5)

    # Рисование кнопок
    draw_button(screen, 10, 10, 80, 30, "Очистить", grey)
    draw_button(screen, 100, 10, 100, 30, "Сохранить", grey)

    # Обновление экрана
    pygame.display.flip()

# Завершение Pygame
pygame.quit()
