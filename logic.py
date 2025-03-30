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


def step_logic(card):
    """"""
    range = card.rank
    only_deck = deck.attack + deck.defense
    for cart in only_deck:
        range_cart = cart.rank
        if range == range_cart:
            return True


player_hand = player_2.hands
trump_suit = trump_card[0].suit
a = select_card_to_play(player_hand, trump_suit)
print(f'Мой ход {a}')
