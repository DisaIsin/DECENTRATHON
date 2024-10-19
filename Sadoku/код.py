import pygame
import random
import os
import time

# Инициализация Pygame
pygame.init()

# Настройки окна
screen_width = 1280
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Управление")

# Загрузка фона
background = pygame.image.load("фон.jpg")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Размеры Андрея (настраиваемые ширина и высота)
andrey_width = 40  # Ширина Андрея
andrey_height = 80  # Высота Андрея

# Загрузка изображения Андрея
andrey_image = pygame.image.load("андрей.png")
andrey_image = pygame.transform.scale(andrey_image, (andrey_width, andrey_height))

# Размеры фермера (настраиваемые ширина и высота)
farmer_width = 70  # Ширина фермера
farmer_height = 100  # Высота фермера

# Загрузка изображения фермера
farmer_image = pygame.image.load("фермер.png")
farmer_image = pygame.transform.scale(farmer_image, (farmer_width, farmer_height))

# Загрузка изображения сердца (жизнь)
heart_image = pygame.image.load("heart.png")
heart_image = pygame.transform.scale(heart_image, (60, 40))  # Шире сердечки, высота остается

# Настройки квадрата (игрока - Андрей)
square_x = screen_width // 2 - andrey_width // 2
square_y = screen_height // 2 - andrey_height // 2
speed = 2

# Позиция фермера
farmer_x = 180
farmer_y = 350

# Размеры врага (уменьшаем по высоте и ширине пропорционально)
horse_width = 300
horse_height = 200

# Загрузка изображений врага (торговца)
horse_folder = "лошадь без фона"
horse_images_original = [pygame.image.load(os.path.join(horse_folder, f"horse{i}.png")) for i in range(1, 8)]
horse_images = [pygame.transform.scale(img, (horse_width, horse_height)) for img in horse_images_original]

# Задержка для смены кадров анимации врага
frame_delay = 100  # Время в миллисекундах между сменой кадров анимации

# Цвета для диалогов и текста
dialogue_background_color = (128, 128, 128)  # Серый цвет фона диалога
text_color = (255, 255, 255)  # Белый цвет текста

# Параметры для диалогов
font = pygame.font.SysFont(None, 36)
show_prompt = False  # Показать подсказку "Нажмите F"
dialogue = [
    "Фермер: Привет, Андрей! Как идут дела?",
    "Андрей: Привет! Неплохо, работаем. А у тебя как с полями?",
    "Фермер: Нормально. Скоро будет дождь, это хорошо для урожая!",
    "Андрей: Да, именно! Надеюсь, он поможет вырасти всем растениям.",
    "Фермер: Согласен! Главное — чтобы не было сильных ветров."
]
dialogue_index = 0  # Индекс текущей фразы
dialogue_start_time = 0  # Время начала показа сообщения
show_dialogue = False  # Показать текущее сообщение
interaction_stage = 0  # Этап взаимодействия
dialogue_completed = False  # Диалог окончен

# Функция для отрисовки закругленного фона диалога
def draw_rounded_box(surface, rect, color, alpha, radius):
    s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)  # Создаем поверхность с поддержкой прозрачности
    pygame.draw.rect(s, (*color, alpha), s.get_rect(), border_radius=radius)  # Рисуем закругленный прямоугольник
    surface.blit(s, rect.topleft)

# Функция для отрисовки имени персонажа на сером фоне
def draw_name(surface, name, x, y, width):
    text_surface = font.render(name, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y - 20))  # Расположим текст выше персонажа
    draw_rounded_box(surface, text_rect, (128, 128, 128), 180, 5)  # Серый фон с закругленными краями
    surface.blit(text_surface, text_rect)

# Инициализация жизней
lives = 3

# Функция для спавна нового врага с корректными диапазонами спавна
def spawn_horse():
    horse_x = 0 - horse_images[0].get_width()  # Начальная позиция врага за пределами экрана
    horse_y = random.randint(400, 440)  # Враг спавнится в диапазоне 400-440 пикселей по оси Y
    return horse_x, horse_y

# Проверка столкновения масок
def check_collision(player_rect, enemy_rect, player_mask, enemy_mask):
    offset = (enemy_rect.x - player_rect.x, enemy_rect.y - player_rect.y)
    return player_mask.overlap(enemy_mask, offset) is not None

# Функция для проверки расстояния между игроком и фермером
def distance_between(rect1, rect2):
    dx = rect1.centerx - rect2.centerx
    dy = rect1.centery - rect2.centery
    return (dx**2 + dy**2) ** 0.5

# Настройки врага (торговца)
horse_speed = 3.5
horse_x, horse_y = spawn_horse()

# Основной цикл
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение нажатых клавиш
    keys = pygame.key.get_pressed()

    # Управление Андреем
    if keys[pygame.K_w] and square_y - speed >= 0:
        square_y -= speed
    if keys[pygame.K_s] and square_y + andrey_height + speed <= screen_height:
        square_y += speed
    if keys[pygame.K_a] and square_x - speed >= 0:
        square_x -= speed
    if keys[pygame.K_d] and square_x + andrey_width + speed <= screen_width:
        square_x += speed

    # Движение торговца (врага) слева направо
    horse_x += horse_speed
    if horse_x > screen_width:  # Если враг вышел за правую границу экрана, удаляем его и спавним нового
        horse_x, horse_y = spawn_horse()  # Спавним врага на новой позиции

    # Проверка на взаимодействие с фермером
    player_rect = pygame.Rect(square_x, square_y, andrey_width, andrey_height)
    farmer_rect = pygame.Rect(farmer_x, farmer_y, farmer_width, farmer_height)
    enemy_rect = pygame.Rect(horse_x, horse_y, horse_width, horse_height)

    # Проверка на расстояние между игроком и фермером
    distance = distance_between(player_rect, farmer_rect)

    if distance <= 50 and not dialogue_completed:
        show_prompt = True
        if keys[pygame.K_f] and interaction_stage == 0:  # Подсказка и начало диалога
            interaction_stage = 1
            show_prompt = False
            show_dialogue = True
            dialogue_start_time = time.time()
        elif keys[pygame.K_f] and not show_dialogue:  # Следующая фраза после нажатия F
            interaction_stage += 1
            if interaction_stage > len(dialogue):
                interaction_stage = len(dialogue)  # Останавливаемся на последней фразе
                dialogue_completed = True  # Диалог окончен
            show_dialogue = True
            dialogue_start_time = time.time()
    else:
        # Если игрок уходит дальше 50 пикселей, прервать диалог
        show_prompt = False
        show_dialogue = False
        interaction_stage = 0  # Сбросить диалог
        dialogue_completed = False  # Сбросить флаг окончания диалога

    # Скрыть сообщение через 3 секунды
    if show_dialogue and time.time() - dialogue_start_time > 3:
        show_dialogue = False

    # Проверка на столкновение игрока с врагом
    player_mask = pygame.mask.Mask((andrey_width, andrey_height), fill=True)
    enemy_mask = pygame.mask.from_surface(horse_images[0])

    if check_collision(player_rect, enemy_rect, player_mask, enemy_mask):
        lives -= 1
        horse_x, horse_y = spawn_horse()  # Спавним нового врага, если произошло столкновение

    # Очистка экрана и отрисовка фона
    screen.blit(background, (0, 0))

    # Отрисовка Андрея
    screen.blit(andrey_image, (square_x, square_y))
    draw_name(screen, "Андрей", square_x, square_y, andrey_width)  # Имя над Андреем

    # Отрисовка фермера
    screen.blit(farmer_image, (farmer_x, farmer_y))
    draw_name(screen, "Фермер", farmer_x, farmer_y, farmer_width)  # Имя над фермером

    # Отрисовка торговца (врага) с анимацией
    current_horse_frame = (pygame.time.get_ticks() // frame_delay) % len(horse_images)
    screen.blit(horse_images[current_horse_frame], (horse_x, horse_y))

    # Отрисовка жизней в правом верхнем углу
    for i in range(lives):
        screen.blit(heart_image, (screen_width - (i + 1) * 50, 10))  # Уменьшено расстояние между сердечками

    # Отрисовка подсказки "Нажмите F" при подходе к фермеру
    if show_prompt:
        text_surface = font.render("Нажмите F", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(farmer_x + farmer_width // 2, farmer_y - 30))
        draw_rounded_box(screen, text_rect, (0, 0, 0), 128, 10)  # Полупрозрачный черный фон с закругленными краями
        screen.blit(text_surface, text_rect)

    # Отрисовка диалога
    if show_dialogue and interaction_stage > 0 and interaction_stage <= len(dialogue):
        text_surface = font.render(dialogue[interaction_stage - 1], True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2 - 50))
        draw_rounded_box(screen, text_rect, dialogue_background_color, 180, 10)  # Серый фон с закругленными краями
        screen.blit(text_surface, text_rect)

    # Обновление экрана
    pygame.display.flip()

    # Ограничение FPS
    clock.tick(60)

    # Проверка на проигрыш (если жизней не осталось)
    if lives <= 0:
        running = False  # Завершаем основной цикл

# Завершение Pygame
pygame.quit()
