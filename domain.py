__author__ = 'Mathieu'


class Team():
    def __init__(self, name, club):
        self.name = name
        self.club = club

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.club)


class Match():
    def __init__(self, first_team, second_team):
        self.first_team = first_team
        self.second_team = second_team

    def __str__(self):
        return '{0} vs {1}'.format(self.first_team, self.second_team)
