from otree.api import *
import math


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Game2'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
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
        widget=widgets.RadioSelect,
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
    current_round = group.round_number
    if current_round > 1:
        previous_stock = group.in_round(current_round - 1).current_stock
        if previous_stock > 3:
            p1 = group.get_player_by_id(1)
            p1_fished = p1.in_round(current_round - 1).fished_amount
            p2 = group.get_player_by_id(2)
            p2_fished = p2.in_round(current_round - 1).fished_amount
            p3 = group.get_player_by_id(3)
            p3_fished = p3.in_round(current_round - 1).fished_amount
            new_stock = round((previous_stock - p1_fished - p2_fished - p3_fished) * C.REGROWTH_RATE)
            group.current_stock = C.INITIAL_STOCK if new_stock > C.INITIAL_STOCK else new_stock


# PAGES
class CalculateRemainingStock(WaitPage):
    after_all_players_arrive = calculate_remaining_stock

    titel_text = "Please Wait"
    body_text = " The game will continue shortly."


class Fishing(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        if player.round_number < 6:
            return player.group.current_stock > 3 and player.id_in_group != 3
        else:
            return player.group.current_stock > 3

    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        others_total_fished_amount = 0
        if current_round > 1:
            others = player.get_others_in_group()
            for other in others:
                others_total_fished_amount += other.in_round(current_round - 1).fished_amount
        return dict(others_total_fished_amount=others_total_fished_amount)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff += player.fished_amount
        return


class WaitEndOfRound(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        current_round = group.round_number
        if current_round == 10:
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p3 = group.get_player_by_id(3)
            new_stock = round((group.current_stock - p1.fished_amount - p2.fished_amount - p3.fished_amount) * C.REGROWTH_RATE)
            group.current_stock = C.INITIAL_STOCK if new_stock > C.INITIAL_STOCK else new_stock
            leftover_per_player = math.floor(group.current_stock / 3)
            players = group.get_players()
            for player in players:
                player.participant.payoff += leftover_per_player

    titel_text = "Please Wait"
    body_text = " The game will continue shortly."


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10


page_sequence = [CalculateRemainingStock, Fishing, WaitEndOfRound, Results]
