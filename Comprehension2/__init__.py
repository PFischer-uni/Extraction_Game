from otree.api import *

doc = """
comprehension question 2
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension2'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz6 = models.IntegerField(label='How many fishers can catch fish in the first 5 rounds?',
                                choices=[1, 2, 3],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz6_solution = models.BooleanField()
    quiz7 = models.IntegerField(label='Among how many fishers will the fish left in the lake after the last round be split for the final payoff?',
                                choices=[1, 2, 3],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz7_solution = models.BooleanField()


# PAGES
class quiz6(Page):
    form_model = 'player'
    form_fields = ['quiz6']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz6 == 2:
            player.quiz6_solution = True
        else:
            player.quiz6_solution = False

class quiz6_solution(Page):
    form_model = 'player'


class quiz7(Page):
    form_model = 'player'
    form_fields = ['quiz7']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz7 == 3:
            player.quiz7_solution = True
        else:
            player.quiz7_solution = False

class quiz7_solution(Page):
    form_model = 'player'



class ResultsWaitPage(WaitPage):
    pass




page_sequence = [quiz6, quiz6_solution, quiz7, quiz7_solution]