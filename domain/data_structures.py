from enum import Enum

__author__ = 'Mathieu'


class Team:
    def __init__(self, name='NO_NAME', club='NO_CLUB', number=0):
        self.number = number
        self.name = name
        self.club = club
        self.played_against = {}

    def add_match(self, other_team, has_win):
        self.played_against[other_team] = has_win

    def __str__(self):
        return '{0} ({1})'.format(self.name, self.club)

    def __unicode__(self):
        return '{0} ({1})'.format(self.name, self.club)

    def __eq__(self, other):
        return other.name == self.name and other.club == self.club

    def __hash__(self, *args, **kwargs):
        return hash((self.name, self.club))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return repr((self.name, self.club, self.number))


class MatchStatus(Enum):
    PLAYING = 0
    DONE = 1


class Match:
    def __init__(self, first_team, second_team=Team()):
        self.first_team = first_team
        self.second_team = second_team
        if second_team == Team():
            self.set_finished(first_team)
        else:
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

    def __eq__(self, other):
        return self.first_team == other.first_team and self.second_team == other.second_team

    def __ne__(self, other):
        return not self.__eq__(other)
