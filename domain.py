__author__ = 'Mathieu'


class Team():
    def __init__(self, name, club):
        self.name = name
        self.club = club

    def __str__(self):
        return '%s (%s)' % (self.name, self.club)
