import random


NUMBER_OF_CARDS_DEALT = 6
NAME_PLAYER_1 = "Валерий"
NAME_PLAYER_2 = "Ботяра"
COUNT_CARD = 36
MIN_COUNT_CARD = 6


class Card():
    """Класс карты."""
    def __init__(
            self, suit: str, rank: str, value: int, image_path: str) -> None:
        self.suit = suit
        self.rank = rank
        self.value = value
        self.image_path = image_path
        self.image = None

    def __str__(self):
        return f'{self.rank}_{self.suit}'


class Deck_Cards():
    """Класс колоды и действия с ней."""
    def __init__(self) -> None:
        self.colour = ["бубна", "черви", "крести", "пики"]
        self.deck = []
        self.defense = []
        self.attack = []
        self.trump_card = []
        self.stand_down = []
        self.count = COUNT_CARD
        self.card_ranks = {
            '2': 2,
            '3': 3,
            '4': 4,
            '5': 5,
            '6': 6,
            '7': 7,
            '8': 8,
            '9': 9,
            '10': 10,
            'валет': 11,
            'дама': 12,
            'кароль': 13,
            'туз': 14
        }

    def create_deck(self) -> None:
        """Создаёт колоду и перетосовывает колоду."""
        for suit in self.colour:
            for rank, value in self.card_ranks.items():
                image_name = f'{suit}_{rank}.png'
                image_path = f'images/{image_name}'
                card = Card(
                    suit=suit,
                    rank=rank,
                    value=value,
                    image_path=image_path
                )
                deck_cards.append(card)
        random.shuffle(self.deck)


class Player():
    """Класс игрока и бота."""
    instances = []

    def __init__(self) -> None:
        Player.instances.append(self)
        self.name = "Name"
        self.status = None
        self.hands = []

    @classmethod
    def get_all_instances(cls) -> list:
        """Получаем список игроков."""
        return cls.instances

    @classmethod
    def get_instance_count(cls) -> int:
        """Считаем игроков."""
        return len(cls.instances)

    def len_hands(self) -> int:
        """Считает карты на руках"""
        return len(self.hands)

    def add_cards(self) -> None:
        """Добавляет карты в руки если они есть в колоде"""
        if self.len_hands() < NUMBER_OF_CARDS_DEALT and len(deck_cards) > 0:
            count = NUMBER_OF_CARDS_DEALT - self.len_hands()
            for index in range(count):
                hands = self.hands
                if len(deck_cards) > 0:
                    hands.append(deck_cards.pop())
                else:
                    if len(trump_card) > 0:
                        hands.append(trump_card.pop())
                    else:
                        print("Всё кончено")


class Leader(Deck_Cards):
    """Класс который описывает поведение ведущего."""
    def __init__(self):
        self.step = ''

    def hands_out_the_сards(self, deck: list, *args, **kwargs) -> None:
        """Раздаёт карты, указывает козырь."""
        if count_player <= NUMBER_OF_CARDS_DEALT:
            for player in list_player:
                for index in range(NUMBER_OF_CARDS_DEALT):
                    hands = player.hands
                    hands.append(deck_cards.pop())
        trump_card.append(deck_cards.pop())

    def one_step(
            self,
            player_1_hands: list,
            player_2_hands: list,
            trump_card: list
            ) -> None:
        """Определяет, кто первый ходит."""
        trump_suit = trump_card[0].suit
        player1_trumps = []
        player2_trumps = []

    # Собираем козырные карты первого игрока
        for card in player_1_hands:
            if card.suit == trump_suit:
                player1_trumps.append(card)

    # Собираем козырные карты второго игрока
        for card in player_2_hands:
            if card.suit == trump_suit:
                player2_trumps.append(card)

        # Случай, когда у обоих нет козырей
        if len(player1_trumps) == 0 and len(player2_trumps) == 0:
            if random.randint(0, 1) == 0:
                player_1.status = True
                player_2.status = False
            else:
                player_1.status = False
                player_2.status = True
            return

        # Если у первого игрока нет козырей
        if len(player1_trumps) == 0:
            player_1.status = False
            player_2.status = True
            return

        # Если у второго игрока нет козырей
        if len(player2_trumps) == 0:
            player_1.status = True
            player_2.status = False
            return

        # Находим младший козырь у первого игрока
        min_trump_p1 = player1_trumps[0]
        for card in player1_trumps:
            if card.value < min_trump_p1.value:
                min_trump_p1 = card

        # Находим младший козырь у второго игрока
        min_trump_p2 = player2_trumps[0]
        for card in player2_trumps:
            if card.value < min_trump_p2.value:
                min_trump_p2 = card

        # Сравниваем младшие козыри
        if min_trump_p1.value < min_trump_p2.value:
            player_1.status = True
            player_2.status = False
        else:
            player_1.status = False
            player_2.status = True


player_1 = Player()   # Игрок 1
player_1.name = NAME_PLAYER_1
deck_player_1 = player_1.hands
# Игрок 2
player_2 = Player()
player_2.name = NAME_PLAYER_2
deck_player_2 = player_2.hands
# Создаём калоду
deck = Deck_Cards()
deck_cards = deck.deck
deck_finall = deck.create_deck()
# print(deck_cards[1].image_path)
# Создаём ведущего
leader = Leader()
# Считаем игроков
count_player = Player.get_instance_count()
list_player = Player.get_all_instances()
# Раздаем карты
trump_card = deck.trump_card
leader.hands_out_the_сards(deck_cards, count_player, list_player, trump_card)
# print(f'Карты {player_1.name}: {player_1.hands}'
#       f'и карты {player_2.name}: {player_2.hands}')
player_1_hands = player_1.hands
player_2_hands = player_2.hands
one_step = leader.one_step(player_1_hands, player_2_hands, trump_card)
print(f'Первый ходит: {player_2.status}')
