from enum import IntEnum
import random

from PySide.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide.QtGui import QBrush

from domain.data_structures import Team, Match

__author__ = 'msoum'


class TeamModel(QAbstractItemModel):
    def __init__(self):
        super(TeamModel, self).__init__()

        self.team_list = [
            Team('A', 'A'),
            Team('B', 'B'),
            Team('C', 'C'),
            Team('D', 'D'),
            Team('E', 'E'),
            Team('F', 'F'),
            Team('G', 'G'),
            Team('H', 'H'),
            Team('I', 'I'),
            Team('J', 'J'),
        ]

    def columnCount(self, parent=QModelIndex):
        return 2

    def rowCount(self, parent=QModelIndex):
        return len(self.team_list)

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return self.team_list[index.row()].name
            if index.column() == 1:
                return self.team_list[index.row()].club
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        else:
            return None

    def index(self, row, column, parent=QModelIndex):
        return self.createIndex(row, column)

    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        if orientation == Qt.Vertical:
            return super(TeamModel, self).headerData(section, orientation, role)
        elif orientation == Qt.Horizontal and role == Qt.DisplayRole:
            if section == 0:
                return 'Team name'
            else:
                return 'Club name'
        else:
            return None

    def add_team(self, name, club):
        self.beginInsertRows(QModelIndex(), len(self.team_list), len(self.team_list))
        self.team_list.append(Team(name, club))
        self.endInsertRows()

    def get_team(self, row):
        return self.team_list[row]

    def update_team(self, team, new_name, new_club):
        self.beginResetModel()
        team_idx = self.team_list.index(team)
        self.team_list[team_idx] = Team(new_name, new_club)
        self.endResetModel()

    def delete_team(self, team):
        team_idx = self.team_list.index(team)
        self.beginRemoveRows(QModelIndex(), team_idx, team_idx)
        self.team_list.pop(team_idx)
        self.endRemoveRows()


team_model = TeamModel()


class MatchModel(QAbstractItemModel):
    def __init__(self, team_count):
        super(MatchModel, self).__init__()
        self.match_list = []
        self.team_list = []

        self.team_data = []

        for i in range(0, team_count):
            self.team_data.append(None)

    def columnCount(self, parent=QModelIndex):
        return 2

    def rowCount(self, parent=QModelIndex):
        return len(self.team_data) // 2

    def data(self, index, role=Qt.DisplayRole):
        team = self.team_data[(index.column() * ((len(self.team_data) // 2) - 1)) + index.row()]
        other_team = self.team_data[(((index.column() + 1) % 2) * ((len(self.team_data) // 2) - 1)) + index.row()]
        if role == Qt.DisplayRole:
            if team is None:
                return "None"
            else:
                return team.name
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.BackgroundRole:
            if team is not None and other_team in team.played_against:
                if team.played_against[other_team]:
                    return QBrush(Qt.green, Qt.Dense5Pattern)
                else:
                    return QBrush(Qt.red, Qt.Dense5Pattern)
            else:
                return None
        else:
            return None

    def get_match(self, row):
        first_team_idx = row
        second_team_idx = (len(self.team_data) // 2) - 1 + row
        return Match(self.team_data[first_team_idx], self.team_data[second_team_idx])

    def get_raw_team(self, index):
        return self.team_data[(index.column() * ((len(self.team_data) // 2) - 1)) + index.row()]

    def index(self, row, column, parent=QModelIndex):
        return self.createIndex(row, column)

    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        return None

    def find_match_with_player(self, player):
        return [it for it in self.match_list if it.first_team == player or it.second_team == player][0]

    def set_winner(self, row, first_column):
        if first_column:
            column = 0
        else:
            column = 1

        winner_team = self.get_raw_team(self.index(row, column))
        loser_team = self.get_raw_team(self.index(row, (column + 1) % 2))
        winner_team.add_match(loser_team, True)
        loser_team.add_match(winner_team, False)

    def get_match_finished_count(self):
        return len([it for it in self.match_list if it.is_finished()])

    def add_team(self, team):
        rand_idx = self.__compute_random_index()
        self.team_data[rand_idx] = team
        index = self.create_index_from_data_index(rand_idx)
        self.dataChanged.emit(index, index)

    def create_index_from_data_index(self, idx):
        team_count = len(self.team_data)
        col = 1
        if idx < team_count // 2:
            col = 0
        row = idx - (col * (team_count // 2))
        return self.index(row, col)

    def __compute_random_index(self):
        rand_idx = random.choice([i for i in range(0, len(self.team_data)) if self.team_data[i] is None])
        return rand_idx

class ContestPhase(IntEnum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class ContestModel:
    def __init__(self):

        self.team_count = 0

        # Compute match model size according to team count and current phase
        # ContestPhase.FIRST:
        first = len(team_model.team_list)
        # ContestPhase.SECOND:
        half = (first // 2)
        second_one_win = half + (half % 2)
        second_no_win = half - (half % 2)
        # ContestPhase.THIRD:
        half_one = second_one_win // 2
        half_no = second_one_win // 2
        third_two_win = half_one + (half_one % 2)
        third_one_win = half_one - (half_one % 2) + half_no + (half_no % 2)
        third_no_win = half_no - (half_no % 2)
        # ContestPhase.FOURTH:
        half_two = third_two_win // 2
        half_one = third_one_win // 2
        half_no = third_no_win // 2
        fourth_three_win = half_two + (half_two % 2)
        fourth_two_win = half_two - (half_two % 2) + half_one + (half_one % 2)
        fourth_one_win = half_one - (half_one % 2) + half_no + (half_no % 2)
        fourth_no_win = half_no - (half_no % 2)

        self.first_match_model = MatchModel(first)
        self.second_match_models = [
            MatchModel(second_no_win),
            MatchModel(second_one_win)
        ]
        self.third_match_models = [
            MatchModel(third_no_win),
            MatchModel(third_one_win),
            MatchModel(third_two_win)
        ]
        self.fourth_match_models = [
            MatchModel(fourth_no_win),
            MatchModel(fourth_one_win),
            MatchModel(fourth_two_win),
            MatchModel(fourth_three_win)
        ]

        self.init_first_match_model()

    def init_first_match_model(self):
        # Generate first match list
        team_list = list(team_model.team_list)
        random.shuffle(team_list)
        for team in team_list:
            self.first_match_model.add_team(team)
