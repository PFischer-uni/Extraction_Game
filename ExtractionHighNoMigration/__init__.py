from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ExtractionHighMigration'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    INITIAL_STOCK = 101
    MAX_EXTRACTION = [0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
    REGROWTH_RATE = 1.1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_stock = models.IntegerField(
        initial=C.INITIAL_STOCK,
        min=0,
        max=C.INITIAL_STOCK,
        doc="""Current Stock""",
        label="Fishes left"
    )


class Player(BasePlayer):
    fished_amount = models.IntegerField(
        initial=0,
        min=0,
        max=C.MAX_EXTRACTION[-1],
        doc="""Amount fished at round""",
        label="How much do you want to fish?"
    )


# FUNCTIONS
def fished_amount_choices(player):
    group = player.group
    return range(
        0,
        C.MAX_EXTRACTION[group.current_stock]+1,
        1
    )


def calculate_remaining_stock(group):
    p1 = group.get_player_by_id(1)
    p2 = group.get_player_by_id(2)
    p3 = group.get_player_by_id(3)
    if group.current_stock > 0:
        new_stock = round((group.current_stock - p1.fished_amount - p2.fished_amount - p3.fished_amount) * C.REGROWTH_RATE)
        group.current_stock = 101 if new_stock > 101 else new_stock




# PAGES
class Round1(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound1(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round2(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound2(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round3(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
       return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound3(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round4(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
       return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound4(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round5(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
       return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound5(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round6(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound6(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round7(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound7(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round8(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound8(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round9(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound9(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Round10(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        return player.group.current_stock > 0 and player.id_in_group != 3


class CalculateRound10(WaitPage):
    after_all_players_arrive = calculate_remaining_stock


class Results(Page):
    pass


page_sequence = [Round1, CalculateRound1, Round2, CalculateRound2, Round3, CalculateRound3, Round4, CalculateRound4, Round5, CalculateRound5, Round6, CalculateRound6, Round7, CalculateRound7, Round8, CalculateRound8, Round9, CalculateRound9, Round10, CalculateRound10, Results]
