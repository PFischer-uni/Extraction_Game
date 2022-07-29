from otree.api import *

doc = """
comprehension question 1
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1 = models.IntegerField(label='Imagine that you play the game with two fishers at the lake. After both fisherhave decided how many fish to catch, there are 40 fish left in the lake. How many fish will be in the lake in the next round?',
                                choices=[44, 40, 48],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz1_solution = models.BooleanField()
    quiz2 = models.IntegerField(label='Imagine that you play the game with two fishers at the lake. After both fishers have decided how many fish to catch, there are 58 fish left in the lake. How many fish will be in the lake in the next round?',
                                choices=[54, 60, 64],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz2_solution = models.BooleanField()
    quiz3 = models.IntegerField(label='Imagine that you play the game with two fishers at the lake. After the 10th round and the regrowth of 10 percent, there are 30 fish left in the lake. How many of these fish does each of the two fishers receive?',
                                choices=[10, 30, 15],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz3_solution = models.BooleanField()
    quiz4 = models.IntegerField(label='Imagine that you play the game with two fishers at the lake. What determines your payoff in the game?',
                                choices=[[1,'The fish you catch in all rounds.'], [2,'Half of the fish that are left in the lake after the final round.'], [3,'The fish you catch in all rounds plus half of the fish that are left in the lake after the final round.']],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz4_solution = models.BooleanField()
    quiz5 = models.IntegerField(label='Imagine that you play the game with only one fisher at the lake. There are 12 fish in the lake. You catch 2 fish. How many fish are in the lake in the next round?',
                                choices=[11, 20, 10],
                                widget=widgets.RadioSelect,
                                blank=False
                                )
    quiz5_solution = models.BooleanField()

# PAGES
class quiz1(Page):
    form_model = 'player'
    form_fields = ['quiz1']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz1 == 44:
            player.quiz1_solution = True
        else:
            player.quiz1_solution = False

class quiz1_solution(Page):
    form_model = 'player'


class quiz2(Page):
    form_model = 'player'
    form_fields = ['quiz2']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz2 == 64:
            player.quiz2_solution = True
        else:
            player.quiz2_solution = False

class quiz2_solution(Page):
    form_model = 'player'

class quiz3(Page):
    form_model = 'player'
    form_fields = ['quiz3']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz3 == 15:
            player.quiz3_solution = True
        else:
            player.quiz3_solution = False


class quiz3_solution(Page):
    form_model = 'player'


class quiz4(Page):
    form_model = 'player'
    form_fields = ['quiz4']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz4 == 3:
            player.quiz4_solution = True
        else:
            player.quiz4_solution = False


class quiz4_solution(Page):
    form_model = 'player'


class quiz5(Page):
    form_model = 'player'
    form_fields = ['quiz5']

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.quiz5 == 11:
            player.quiz5_solution = True
        else:
            player.quiz5_solution = False

class quiz5_solution(Page):
    form_model = 'player'


class ResultsWaitPage(WaitPage):
    pass




page_sequence = [quiz1, quiz1_solution, quiz2, quiz2_solution, quiz3, quiz3_solution,
                 quiz4, quiz4_solution, quiz5, quiz5_solution]

