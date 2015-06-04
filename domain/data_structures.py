from enum import Enum

__author__ = 'Mathieu'


class Team():
    def __init__(self, name, club):
        self.name = name
        self.club = club

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.club)

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.club)


class MatchStatus(Enum):
    PLAYING = 0
    DONE = 1


class Match():
    def __init__(self, first_team, second_team):
        self.first_team = first_team
        self.second_team = second_team
        self.match_status = MatchStatus.PLAYING
        self.winner = None

    def is_finished(self):
        return self.match_status == MatchStatus.DONE

    def set_finished(self, winner):
        self.match_status = MatchStatus.DONE
        self.winner = winner

    def is_winner(self, player):
        return self.match_status == MatchStatus.DONE and self.winner == player

    def __str__(self):
        return '{0} vs {1}'.format(str(self.first_team), str(self.second_team))

    def __unicode__(self):
        return '{0} vs {1}'.format(str(self.first_team), str(self.second_team))
