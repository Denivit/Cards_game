import sys

import pygame

from cards_game import deck, deck_cards, player_1, player_2, trump_card
from logic import (atack_step_logic, bot_atack_step_logic, defense_step,
                   select_card_to_play, defanse_bot)

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Дурак")
WHITE = (255, 255, 255)
GREEN = (0, 128, 0)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
PLAYER_HAND_ZONE = {
        'x_start': 200,
        'y': 400,
        'card_width': 70,
        'card_height': 100,
        'spacing': 70,
    }

PLAY_ZONE = {
        'x_start': 200,
        'y': 250,
        'card_width': 70,
        'card_height': 100,
        'spacing': 80
    }

DISCARD_ZONE = {
        'x': 690,
        'y': 250,
        'width': 70,
        'height': 100
    }

font = pygame.font.Font(None, 12)

player_cards_1 = player_1.hands
player_cards_2 = player_2.hands

# Загрузка изображения рубашки карты
card_back = pygame.image.load("images/back-red.png").convert_alpha()
card_back = pygame.transform.scale(card_back, (70, 100))


def draw_text(text: str,
              x: int,
              y: int,
              color: str = BLACK,
              font_size: int = 24,
              font_name: str = None,
              bold=False,
              italic=False
              ) -> None:
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
    font.set_bold(bold)
    font.set_italic(italic)

    # Отрисовываем текст
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))


def draw_card(x: int,
              y: int,
              card,
              is_face_up=True):
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
        card.image = pygame.transform.scale(card.image, (70, 100))
        screen.blit(card.image, (x, y))
    else:
        # Отрисовываем рубашку карты
        screen.blit(card_back, (x, y))


def draw_game_field() -> None:
    """Отрисовывает игровое поле."""
    screen.fill(GREEN)  # Зеленый фон для игрового поля
    # Отрисовываем имена
    draw_text(player_1.name, 350, 520, RED, font_size=36, bold=True)
    draw_text(player_2.name, 350, 10, RED, font_size=36, bold=True)

    # Отрисовка зоны для колоды
    if deck_cards:  # Если в колоде есть карты
        screen.blit(card_back, (10, 250))

    # Козырь
    if trump_card:  # Если козырь есть
        trump = trump_card[0]  # Берём первый элемент из списка
        draw_card(100, 250, trump, is_face_up=True)

    # Отрисовка зоны для сброса (отбоя)
    if True:  # Если в отбое есть карты
        screen.blit(card_back, (690, 250))

    # Отрисовка атаки
    if deck.attack:  # Если в зоне хода есть карты
        for i, card in enumerate(deck.attack):
            draw_card(205 + i * 80, 220, card, is_face_up=True)
    # Отрисовка защиты
    if deck.defense:  # Если в зоне хода есть карты
        for i, card in enumerate(deck.defense):
            draw_card(200 + i * 80, 250, card, is_face_up=True)

    # Отрисовка карт игрока
    for i, card in enumerate(player_cards_1):
        if len(player_cards_1) == 7:
            PLAYER_HAND_ZONE['spacing'] = 60
            draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                      400,
                      card,
                      is_face_up=True)
        if len(player_cards_1) == 8:
            PLAYER_HAND_ZONE['spacing'] = 50
            draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                      400,
                      card,
                      is_face_up=True)
        if len(player_cards_1) == 8:
            PLAYER_HAND_ZONE['spacing'] = 50
            draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                      400,
                      card,
                      is_face_up=True)
        if len(player_cards_1) == 9:
            PLAYER_HAND_ZONE['spacing'] = 40
            draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                      400,
                      card,
                      is_face_up=True)
        else:
            draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                      400,
                      card,
                      is_face_up=True)

    # Отрисовка карт противника
    for i, card in enumerate(player_cards_2):
        draw_card(200 + i * PLAYER_HAND_ZONE['spacing'],
                  50,
                  card,
                  is_face_up=False)


def handle_mouse_click(event, click_processed):
    """
    Универсальный обработчик кликов мыши для всех игровых зон
    :param event: Событие мыши
    :param click_processed: Флаг обработки клика
    :param game_state: Состояние игры
    :return: Обновлённый флаг click_processed
    """
    # Обработка нажатия кнопки мыши
    if (event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and not click_processed):
        mouse_x, mouse_y = event.pos

        # 1. Проверка клика по картам в руке игрока
        for i, card in enumerate(player_cards_1):
            card_x = PLAYER_HAND_ZONE['x_start'] + i * PLAYER_HAND_ZONE['spacing']
            card_y = PLAYER_HAND_ZONE['y']
            if i < len(player_cards_1) - 1:
                clickable_width = PLAYER_HAND_ZONE['spacing']  # Видимая часть
            else:
                clickable_width = PLAYER_HAND_ZONE['card_width']  # Полная ширина
                # Проверяем попадание курсора в область
            if (card_x <= mouse_x <= card_x + clickable_width and 
                card_y <= mouse_y <= card_y + PLAYER_HAND_ZONE['card_height']):
                print(f"Игрок выбрал карту: {card}")
                # Если атакующий ходит
                if player_1.status is True:
                    if atack_step_logic(card) is True or not deck.attack:
                        deck.attack.append(card)
                        player_cards_1.pop(i)
                        click_processed = True
                        break
                    else:
                        print('Нет такой карты в колоде')
                else:
                    # Если защищающий ходит
                    if not deck.attack:
                        print('Ждём хода противника')
                    else:
                        if defense_step(card) is True:
                            deck.defense.append(card)
                            player_cards_1.pop(i)
                            click_processed = True
                            break
                        else:
                            print('Нельзя этой картой отбивать атаку')

        # 2. Проверка клика по игровой зоне (взять карты)
        if not click_processed and (deck.attack or deck.defense):
            mouse_x, mouse_y = event.pos
            for i in range(max(len(deck.attack), len(deck.defense))):
                card_x = PLAY_ZONE['x_start'] + i * PLAY_ZONE['spacing']
                card_y = PLAY_ZONE['y']

                if (card_x <= mouse_x <= card_x + PLAY_ZONE['card_width']
                        and card_y <= mouse_y <= card_y
                        + PLAY_ZONE['card_height']):
                    if player_1.status is False:
                        print("Игрок берёт карты")
                        player_cards_1.extend(deck.attack + deck.defense)
                        deck.attack.clear()
                        deck.defense.clear()
                        player_1.add_cards()
                        player_2.add_cards()
                        click_processed = True
                        break
                    else:
                        print('Атакующий не может снимать каты с поля атаки')

        # 3. Проверка клика по зоне отбоя (сброс карт)
        if not click_processed:
            if (DISCARD_ZONE['x'] <= mouse_x <= DISCARD_ZONE['x']
                    + DISCARD_ZONE['width']
                    and
                    DISCARD_ZONE['y'] <= mouse_y <= DISCARD_ZONE['y']
                    + DISCARD_ZONE['height']):
                if deck.attack == []:
                    print('Нет карт для отбоя')
                else:
                    if player_1.status is True:
                        print("Карты отправлены в отбой")
                        discard_pile = deck.stand_down
                        discard_pile.extend(deck.attack + deck.defense)
                        deck.attack.clear()
                        deck.defense.clear()
                        player_1.add_cards()
                        player_2.add_cards()
                        player_1.status = False
                        player_2.status = True
                        click_processed = True
                    else:
                        print('Закончить ход может только атакующий')

    # Сброс флага при отпускании кнопки
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
        # Ход бота если защищается
        if player_2.status is False and len(deck.attack) != len(deck.defense):
            defence_cart = defanse_bot()
            print(f'До {defence_cart}')
            if defence_cart is None:
                print('Забираю, нечем бить!')
                player_cards_2.extend(deck.defense + deck.attack)
                deck.attack.clear()
                deck.defense.clear()
                player_1.add_cards()
            else:
                deck.defense.append(defence_cart)
                player_cards_2.remove(defence_cart)

        # Ход бота если атакует
        if (player_2.status is True
                and len(deck.attack) == len(deck.defense)
                and len(deck.attack) < 1):
            trump_suit = trump_card[0].suit
            step_bot = select_card_to_play(player_cards_2, trump_suit)
            print(f'Бот пойдёт картой {step_bot}')
            deck.attack.append(step_bot)
            player_cards_2.remove(step_bot)
        elif (player_2.status is True
                and len(deck.attack) == len(deck.defense)
                and len(deck.attack) > 0):
            step_bot = bot_atack_step_logic()
            if step_bot != None:
                print(f'Бот подкидывает карту {step_bot}')
                deck.attack.append(step_bot)
                player_cards_2.remove(step_bot)
            else:
                print("Карты отправлены в отбой")
                discard_pile = deck.stand_down
                discard_pile.extend(deck.attack + deck.defense)
                deck.attack.clear()
                deck.defense.clear()
                player_1.add_cards()
                player_2.add_cards()
                player_2.status = False
                player_1.status = True
        # Отрисовка игрового поля
        draw_game_field()
        # Обновление экрана
        pygame.display.flip()
        # Ограничение FPS
        clock.tick(30)


if __name__ == "__main__":
    main()
