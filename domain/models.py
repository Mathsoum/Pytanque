from enum import IntEnum
from random import shuffle

from PySide.QtCore import QAbstractItemModel, QModelIndex, Qt

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

        self.team_count = team_count
        self.team_data = {}

        for i in range(0, self.team_count):
            self.team_data[i] = None

    def columnCount(self, parent=QModelIndex):
        return 2

    def rowCount(self, parent=QModelIndex):
        return self.team_count // 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.DisplayRole:
            return self.team_data[(index.column() * ((self.team_count // 2) - 1)) + index.row()]
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.BackgroundRole:
            return None
        else:
            return None

    def index(self, row, column, parent=QModelIndex):
        return self.createIndex(row, column)

    def parent(self, child):
        return QModelIndex()

    def headerData(self, section, orientation, role):
        return None

    def get_match(self, index):
        return self.match_list[index]

    def find_match_with_player(self, player):
        return [it for it in self.match_list if it.first_team == player or it.second_team == player][0]

    def set_winner(self, winner):
        match = self.find_match_with_player(winner)
        idx = self.match_list.index(match)
        match.set_finished(winner)
        self.dataChanged.emit(self.index(0, idx), self.index(1, idx))

    def get_match_finished_count(self):
        return len([it for it in self.match_list if it.is_finished()])


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

    def init_first_match_model(self):
        # Generate first match list
        team_model_copy = team_model.team_list
        shuffle(team_model_copy)
        for i in range(0, len(team_model_copy), 2):
            if i == len(team_model_copy) - 1:
                self.first_match_model.add_match(Match(team_model_copy[i]))
            else:
                self.first_match_model.add_match(Match(team_model_copy[i], team_model_copy[i + 1]))
