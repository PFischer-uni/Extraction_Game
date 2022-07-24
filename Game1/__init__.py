from otree.api import *
import math


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'Game1'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 10
    INITIAL_STOCK_A = 101
    MAX_EXTRACTION = [0,0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10]
    INITIAL_STOCK_B = 21
    REGROWTH_RATE = 1.1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    current_stock_A = models.IntegerField(
        initial=C.INITIAL_STOCK_A,
        min=0,
        max=C.INITIAL_STOCK_A,
        doc="""Current Stock""",
        label="Fishes left"
    )
    current_stock_B = models.IntegerField(
        initial=C.INITIAL_STOCK_B,
        min=0,
        max=C.INITIAL_STOCK_B,
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
    if player.id_in_group != 3:
        return range(
            0,
            C.MAX_EXTRACTION[group.current_stock_A]+1,
            1
        )
    else:
        return range(
            0,
            C.MAX_EXTRACTION[group.current_stock_B] + 1,
            1
        )

def calculate_remaining_stock_A(group):
    current_round = group.round_number
    if current_round > 1:
        previous_stock = group.in_round(current_round - 1).current_stock_A
        if previous_stock > 3:
            p1 = group.get_player_by_id(1)
            p1_fished = p1.in_round(current_round - 1).fished_amount
            p2 = group.get_player_by_id(2)
            p2_fished = p2.in_round(current_round - 1).fished_amount
            new_stock = round((previous_stock - p1_fished - p2_fished) * C.REGROWTH_RATE)
            group.current_stock_A = C.INITIAL_STOCK_A if new_stock > C.INITIAL_STOCK_A else new_stock

def calculate_remaining_stock_B(group):
    current_round = group.round_number
    if current_round > 1:
        previous_stock = group.in_round(current_round - 1).current_stock_B
        if previous_stock > 3:
            p3 = group.get_player_by_id(3)
            p3_fished = p3.in_round(current_round - 1).fished_amount
            new_stock = round((previous_stock - p3_fished) * C.REGROWTH_RATE)
            group.current_stock_B = C.INITIAL_STOCK_B if new_stock > C.INITIAL_STOCK_B else new_stock

# PAGES
class CalculateRemainingStock(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        calculate_remaining_stock_A(group)
        calculate_remaining_stock_B(group)


class Fishing(Page):
    form_model = 'player'
    form_fields = ['fished_amount']

    @staticmethod
    def is_displayed(player: Player):
        if player.id_in_group == 3:
            return player.group.current_stock_B > 3
        else:
            return player.group.current_stock_A > 3



    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        if current_round > 1:
            if player.id_in_group == 1:
                return dict(other_player_fished_amount=player.group.get_player_by_id(2).in_round(current_round - 1).fished_amount)
            elif player.id_in_group == 2:
                return dict(other_player_fished_amount=player.group.get_player_by_id(1).in_round(current_round - 1).fished_amount)

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
            new_stock_A = round((group.current_stock_A - p1.fished_amount - p2.fished_amount) * C.REGROWTH_RATE)
            new_stock_B = round(
                (group.current_stock_B - p3.fished_amount) * C.REGROWTH_RATE)
            group.current_stock_A = C.INITIAL_STOCK_A if new_stock_A > C.INITIAL_STOCK_A else new_stock_A
            group.current_stock_B = C.INITIAL_STOCK_B if new_stock_B > C.INITIAL_STOCK_B else new_stock_B
            leftover_A = math.floor(group.current_stock_A / 2)
            p1.participant.payoff += leftover_A
            p2.participant.payoff += leftover_A
            p3.participant.payoff += group.current_stock_B


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10


page_sequence = [CalculateRemainingStock, Fishing, WaitEndOfRound, Results]
