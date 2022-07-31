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
    empirical_belief_A = models.IntegerField(
        min=0,
        max=C.MAX_EXTRACTION[-1],
        doc="""Belief about what the teammate with lowest id has fished""",
    )
    empirical_belief_B = models.IntegerField(
        min=0,
        max=C.MAX_EXTRACTION[-1],
        doc="""Belief about what the teammate with highest id has fished""",
    )
    normative_belief_A = models.IntegerField(
        min=0,
        max=C.MAX_EXTRACTION[-1],
        doc="""Belief about what Player 1 should have fished""",
    )
    normative_belief_B = models.IntegerField(
        min=0,
        max=C.MAX_EXTRACTION[-1],
        doc="""Belief about what Player 2 should have fished""",
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
        else:
            group.current_stock = previous_stock


# PAGES
class CalculateRemainingStock(WaitPage):
    after_all_players_arrive = calculate_remaining_stock

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
        fished_amount_A = 0
        fished_amount_B = 0
        if current_round > 1:
            teammates = player.get_others_in_group()
            fished_amount_A = teammates[0].in_round(current_round - 1).fished_amount
            fished_amount_B = teammates[1].in_round(current_round - 1).fished_amount
        return dict(fished_amount_A=fished_amount_A, fished_amount_B=fished_amount_B)

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.payoff += player.fished_amount
        return


class Belief(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        if player.round_number > 5:
            if player.id_in_group != 3:
                return ['empirical_belief_A', 'empirical_belief_B']
            else:
                return ['empirical_belief_A', 'empirical_belief_B', 'normative_belief_A', 'normative_belief_B']
        else:
            return ['empirical_belief_A']

    @staticmethod
    def is_displayed(player: Player):
        skipped_round = False
        current_round = player.round_number
        if current_round > 1:
            skipped_round = player.group.in_round(current_round - 1).current_stock < 3
        return (player.id_in_group != 3 or player.round_number > 5) and not skipped_round

    @staticmethod
    def vars_for_template(player: Player):
        label_belief_A_local = 'How many fish do you believe your <b>teammate</b> has caught in the previous round?'
        label_belief_B_local = 'How many fish do you believe the <b>new fisher</b> has caught in the previous round?'
        label_belief_A_migrant = 'How many fish do you believe <b>Fisher 1</b> has caught in the previous round?'
        label_belief_B_migrant = 'How many fish do you believe <b>Fisher 2</b> has caught in the previous round?'
        label_normative_belief_A = 'How much do you think <b>Fisher 1</b> <u>should</u> have caught in the previous round?'
        label_normative_belief_B = 'How much do you think <b>Fisher 2</b> <u>should</u> have caught in the previous round?'
        return dict(label_belief_A_local=label_belief_A_local, label_belief_B_local=label_belief_B_local,
                    label_belief_A_migrant=label_belief_A_migrant, label_belief_B_migrant=label_belief_B_migrant,
                    label_normative_belief_A=label_normative_belief_A, label_normative_belief_B=label_normative_belief_B)


class WaitEndOfRound(WaitPage):
    template_name = 'MyWaitPage.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        current_round = group.round_number
        if current_round == 10:
            # Calculate remaining stock in the lake, divide by 3 and distribute payoff ####
            p1 = group.get_player_by_id(1)
            p2 = group.get_player_by_id(2)
            p3 = group.get_player_by_id(3)
            new_stock = round((group.current_stock - p1.fished_amount - p2.fished_amount - p3.fished_amount) * C.REGROWTH_RATE)
            group.current_stock = C.INITIAL_STOCK if new_stock > C.INITIAL_STOCK else new_stock
            leftover_per_player = math.floor(group.current_stock / 3)
            players = group.get_players()
            for player in players:
                player.participant.payoff += leftover_per_player

            # Calculate payoffs related to correct 'beliefs' predictions ####
            players_history = [player.in_all_rounds() for player in players]
            belief_payoffs = [0, 0, 0]

            for player in [0, 1, 2]:
                i = 0
                for player_round in players_history[player]:
                    if player_round.field_maybe_none('empirical_belief_A') == players_history[0][i].fished_amount:
                        belief_payoffs[player] += 100
                    if player_round.field_maybe_none('empirical_belief_B') == players_history[1][i].fished_amount:
                        belief_payoffs[player] += 100
                    i += 1
            p1.participant.payoff += belief_payoffs[0]
            p2.participant.payoff += belief_payoffs[1]
            p3.participant.payoff += belief_payoffs[2]

    @staticmethod
    def vars_for_template(player: Player):
        current_round = player.round_number
        fished_amount_A = 0
        fished_amount_B = 0
        if current_round > 1:
            teammates = player.get_others_in_group()
            fished_amount_A = teammates[0].in_round(current_round - 1).fished_amount
            fished_amount_B = teammates[1].in_round(current_round - 1).fished_amount
        return dict(fished_amount_A=fished_amount_A, fished_amount_B=fished_amount_B)


class Results(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 10


page_sequence = [CalculateRemainingStock, Fishing, Belief, WaitEndOfRound, Results]
