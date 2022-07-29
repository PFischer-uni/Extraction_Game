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
    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)
    quiz1 = models.IntegerField(label='Imagine that you play in a team of two. After all members of the team have fished, there are 48 fish left in the lake. How much fish will be in the lake in the next round considering the re-growth rate of 10 percent? ')
    quiz2 = models.IntegerField(label='Imagine that you play in a team of two. After the 10th round and the regrowth of 10 percent, there are 30 fish left. How many of these fish does each of the two team members receive?')
    quiz3 = models.IntegerField(label='Imagine that you play in a team of two. In each round you fished 1 fish. At the end of the game there is no fish left. How many Uganda Schilling did you earn in this game?')
    quiz4 = models.IntegerField(label='Imagine that you play the game alone. There are 20 fish in the lake. You fish 5 fish. How much fish is in the pool in the next round?')

# PAGES
class comprehension1(Page):
    form_model = 'player'
    form_fields = ['quiz1']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(quiz1=51)

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {f: 'Wrong' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 3:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors

class comprehension2(Page):
    form_model = 'player'
    form_fields = ['quiz2']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(quiz2=15)

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {f: 'Wrong' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 3:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors


class comprehension3(Page):
    form_model = 'player'
    form_fields = ['quiz3']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(quiz3=10)

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {f: 'Wrong' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 3:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors

class comprehension4(Page):
    form_model = 'player'
    form_fields = ['quiz4']

    @staticmethod
    def error_message(player: Player, values):
        # alternatively, you could make quiz1_error_message, quiz2_error_message, etc.
        # but if you have many similar fields, this is more efficient.
        solutions = dict(quiz4=17)

        # error_message can return a dict whose keys are field names and whose
        # values are error messages
        errors = {f: 'Wrong' for f in solutions if values[f] != solutions[f]}
        # print('errors is', errors)
        if errors:
            player.num_failed_attempts += 1
            if player.num_failed_attempts >= 3:
                player.failed_too_many = True
                # we don't return any error here; just let the user proceed to the
                # next page, but the next page is the 'failed' page that boots them
                # from the experiment.
            else:
                return errors

class Failed1(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many

class Failed2(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many

class Failed3(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many

class Failed4(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.failed_too_many

class ResultsWaitPage(WaitPage):
    pass


class Results1(Page):
    pass

class Results2(Page):
    pass

class Results3(Page):
    pass

class Results4(Page):
    pass

page_sequence = [comprehension1, Results1, comprehension2, Results2, comprehension3, Results3,
                 comprehension4, Results4]

