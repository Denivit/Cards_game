import sys

import pygame

from cards_game import (deck, deck_cards, played_cards, player_1, player_2,
                        trump_card)

# Инициализация Pygame
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дурак")

# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Шрифт
font = pygame.font.Font(None, 12)

# Пример списка карт игроков
player_cards_1 = player_1.hands
player_cards_2 = player_2.hands

# Загрузка изображения рубашки карты
card_back = pygame.image.load("images/back-red.png").convert_alpha()
card_back = pygame.transform.scale(card_back, (70, 100))  # Масштабируем рубашку


def draw_text(text, x, y, color=BLACK, font_size=24, font_name=None, bold=False, italic=False):
    """
    Отрисовывает текст на экране.
    :param text: Текст для отрисовки
    :param x: Координата X
    :param y: Координата Y
    :param color: Цвет текста
    :param font_size: Размер шрифта
    :param font_name: Название шрифта (если используется системный шрифт)
    :param bold: Жирный текст
    :param italic: Курсивный текст
    """
    # Создаём шрифт с указанными параметрами
    font = pygame.font.Font(font_name, font_size)
    font.set_bold(bold)  # Жирный текст
    font.set_italic(italic)  # Курсивный текст

    # Отрисовываем текст
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_card(x, y, card, is_face_up=True):
    """
    Отрисовывает карту как изображение.
    :param x: Координата X для отрисовки карты
    :param y: Координата Y для отрисовки карты
    :param card: Объект карты, у которого есть атрибут image
    :param is_face_up: Если False, отрисовывает рубашку карты
    """
    if is_face_up:
        # Загружаем изображение карты, если оно ещё не загружено
        card.image = pygame.image.load(card.image_path).convert_alpha()
        card.image = pygame.transform.scale(card.image, (70, 100))  # Масштабируем
        screen.blit(card.image, (x, y))
    else:
        # Отрисовываем рубашку карты
        screen.blit(card_back, (x, y))


def draw_game_field():
    """Отрисовывает игровое поле."""
    screen.fill(GREEN)  # Зеленый фон для игрового поля
    #Отрисовываем имена
    draw_text(player_1.name, 350, 520, RED, font_size=36, bold=True)
    draw_text(player_2.name, 350, 10, RED, font_size=36, bold=True)
    
    # Отрисовка зоны для колоды
    if deck_cards:  # Если в колоде есть карты
        screen.blit(card_back, (10, 250))  # Отрисовываем рубашку
    else:  # Если колода пуста
        pygame.draw.rect(screen, WHITE, (10, 250, 70, 100))  # Пустой прямоугольник
        draw_text("Пусто", 20, 270) 

    # Козырь
    if trump_card:  # Если козырь есть
        trump = trump_card[0]  # Берём первый элемент из списка
        draw_card(100, 250, trump, is_face_up=True)  # Отрисовываем козырь
    else:  # Если козыря нет
        pygame.draw.rect(screen, WHITE, (100, 250, 70, 100))  # Пустой прямоугольник
        draw_text("Нет козыря", 110, 270)  # Текст "Нет козыря"

    # Отрисовка зоны для сброса (отбоя)
    if True:  # Если в отбое есть карты
        screen.blit(card_back, (690, 250))  # Отрисовываем рубашку
    else:  # Если отбой пуст
        pygame.draw.rect(screen, WHITE, (690, 250, 70, 100))  # Пустой прямоугольник
        draw_text("Пусто", 700, 270)  # Текст "Пусто"

    # Отрисовка зоны для хода (сыгранные карты)
    if played_cards:  # Если в зоне хода есть карты
        for i, card in enumerate(played_cards):
            draw_card(200 + i * 80, 250, card, is_face_up=True)  # Отрисовываем карты

    # Отрисовка карт игрока
    for i, card in enumerate(player_cards_1):
        draw_card(200 + i * 80, 400, card, is_face_up=True)  # Карты игрока внизу экрана

    # Отрисовка карт противника
    for i, card in enumerate(player_cards_2):
        draw_card(200 + i * 80, 50, card, is_face_up=False)  # Карты противника вверху экрана (рубашкой вверх)


def handle_mouse_click(event, click_processed):
    """
    Обрабатывает клик мыши.
    :param event: Событие мыши
    :param click_processed: Флаг, указывающий, был ли клик уже обработан
    :return: Обновлённое значение флага click_processed
    """
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not click_processed:
        mouse_x, mouse_y = event.pos  # Координаты клика

        # Проверка, попал ли клик в зону карт игрока
        for i, card in enumerate(player_cards_1):
            card_x = 200 + i * 80  # Координата X карты
            card_y = 400  # Координата Y карты

            # Проверка, находится ли курсор в зоне карты
            if (card_x <= mouse_x <= card_x + 70 and
                card_y <= mouse_y <= card_y + 100):
                print(f"Игрок выбрал карту: {card}")
                # Добавляем карту в зону хода
                played_cards.append(card)
                # Удаляем карту из руки игрока
                player_cards_1.pop(i)  # Удаляем только выбранную карту
                click_processed = True  # Помечаем клик как обработанный
                break  # Прерываем цикл после выбора карты

    # Сбрасываем флаг при отпускании кнопки мыши
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        click_processed = False

    return click_processed


def maps_mouse_click(event, click_processed):
    """Переносит карты из зоны игры в руки игрока"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not click_processed:
        mouse_x, mouse_y = event.pos
        for i, card in enumerate(player_cards_1):
            card_x = 200 + i * 80  # Координата X карты
            card_y = 250  # Координата Y карты

            # Проверка, находится ли курсор в зоне карты
            if (card_x <= mouse_x <= card_x + 70 and
                card_y <= mouse_y <= card_y + 100):
                print(f"Игрок выбрал карту: {card}")
                # Добавляем карту в зону хода
                player_cards_1.extend(played_cards)
                # Удаляем карту из руки игрока
                played_cards.clear()
                click_processed = True  # Помечаем клик как обработанный
                break  # Прерываем цикл после выбора карты

    # Сбрасываем флаг при отпускании кнопки мыши
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        click_processed = False

    return click_processed


def stand_down_mouse_click(event, click_processed):
    """Переносит карты из зоны игры в отбой"""
    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not click_processed:
        mouse_x, mouse_y = event.pos
        for i, card in enumerate(player_cards_1):
            card_x = 690  # Координата X карты
            card_y = 250  # Координата Y карты

            # Проверка, находится ли курсор в зоне карты
            if (card_x <= mouse_x <= card_x + 70 and
                card_y <= mouse_y <= card_y + 100):
                print(f"Игрок выбрал карту: {card}")
                # Добавляем карту в зону хода
                stand_down = deck.stand_down
                stand_down.extend(played_cards)
                # Удаляем карту из руки игрока
                played_cards.clear()
                # Добавляем карты если менее 6
                player_1.add_cards()
                player_2.add_cards()
                click_processed = True  # Помечаем клик как обработанный
                break  # Прерываем цикл после выбора карты

    # Сбрасываем флаг при отпускании кнопки мыши
    if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
        click_processed = False

    return click_processed


def main():
    """Основной игровой цикл."""
    clock = pygame.time.Clock()
    click_processed = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # Обработка клика мыши
            click_processed = handle_mouse_click(event, click_processed)
            maps_mouse_click(event, click_processed)
        # Отрисовка игрового поля
        draw_game_field()
        stand_down_mouse_click(event, click_processed)
        # Обновление экрана
        pygame.display.flip()

        # Ограничение FPS
        clock.tick(30)


if __name__ == "__main__":
    main()