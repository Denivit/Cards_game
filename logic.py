from cards_game import player_2, trump_card, deck


def select_card_to_play(player_hand, trump_suit, is_all_trump_cards=False):
    """Выбирает карту для бота."""

    all_trump = all(card.suit == trump_suit for card in player_hand)

    # Если все козырные, то выбираем самую младшую
    if all_trump:
        return min(player_hand, key=lambda x: x.value)

    if not player_hand:
        return None

    # Если не все карты козырные, исключаем козыри
    if not is_all_trump_cards:
        non_trump_cards = [
            card for card in player_hand if card.suit != trump_suit
        ]
        if non_trump_cards:
            player_hand = non_trump_cards

    # Считаем количество карт каждой масти
    suit_counts = {}
    for card in player_hand:
        suit_counts[card.suit] = suit_counts.get(card.suit, 0) + 1

    # Находим масти с максимальным количеством карт
    max_count = max(suit_counts.values()) if suit_counts else 0
    candidate_suits = [
        suit for suit, count in suit_counts.items() if count == max_count
    ]

    # Фильтруем карты по выбранным мастям
    candidate_cards = [
        card for card in player_hand if card.suit in candidate_suits
    ]

    # Сортируем карты: сначала по масти, затем по значению
    candidate_cards.sort(key=lambda x: (x.suit, x.value))

    # Возвращаем самую младшую карту
    return candidate_cards[0] if candidate_cards else None


def bot_atack_step_logic():
    """Выбирает карту чтобы подкинуть  у бота."""
    only_deck = deck.attack + deck.defense
    for cart in player_2.hands:
        for cart_table in only_deck:
            if cart.rank == cart_table.rank:
                return cart


def defanse_bot():
    """Выбирает карту для защиты."""
    if not deck.attack:
        return None  # Нет карт для отбития
    last_card = deck.attack[-1]
    candidate_cards = [
        card for card in player_2.hands 
        if (card.suit == last_card.suit and card.value > last_card.value) 
        or (card.suit == trump_card[0].suit and last_card.suit != trump_card[0].suit)
    ]
    if candidate_cards:
        # Возвращаем самую младшую подходящую карту
        return min(candidate_cards, key=lambda x: x.value)
    return None


def atack_step_logic(card) -> bool:
    """Разрешает  при атаке ходить только тем рангом который уже есть на
    столе.
    """
    range = card.rank
    only_deck = deck.attack + deck.defense
    for cart in only_deck:
        range_cart = cart.rank
        if range == range_cart:
            return True


def defense_step(card) -> bool:
    """Предусмотрена игра картами выше по рангу если одной масти, в так же
    предусматривает защиту козырями.
    """
    value_defense_cart = card.value
    suit_defense_cart = card.suit
    atack_cart = deck.attack[-1]
    value_atack_cart = atack_cart.value
    suit_atack_cart = atack_cart.suit

    if (suit_atack_cart == suit_defense_cart
            and value_defense_cart > value_atack_cart):
        return True
    if (suit_atack_cart != trump_card[0].suit
            and suit_defense_cart == trump_card[0].suit):
        return True


player_hand = player_2.hands
trump_suit = trump_card[0].suit
a = select_card_to_play(player_hand, trump_suit)
print(f'Мой ход {a}')
