from enum import Enum
from random import shuffle
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
    def __init__(self):
        super(MatchModel, self).__init__()
        self.match_list = []
        self.team_list = []

    def add_match(self, match):
        if match not in self.match_list:
            self.match_list.append(match)

    def add_team(self, team):
        if team not in self.team_list:
            self.team_list.append(team)

    def columnCount(self, parent=QModelIndex):
        return 2

    def rowCount(self, parent=QModelIndex):
        return len(self.match_list)

    def data(self, index, role=Qt.DisplayRole):
        selected_match = self.match_list[index.row()]
        if role == Qt.DisplayRole:
            if index.column() == 0:
                return selected_match.first_team.name
            if index.column() == 1:
                return selected_match.second_team.name
        elif role == Qt.TextAlignmentRole:
            return Qt.AlignCenter
        elif role == Qt.BackgroundRole:
            if selected_match.is_finished():
                if selected_match.is_winner(selected_match.first_team):
                    if index.column() == 0:
                        return QBrush(Qt.green, Qt.Dense5Pattern)
                    else:
                        return QBrush(Qt.red, Qt.Dense5Pattern)
                elif selected_match.is_winner(selected_match.second_team):
                    if index.column() == 0:
                        return QBrush(Qt.red, Qt.Dense5Pattern)
                    else:
                        return QBrush(Qt.green, Qt.Dense5Pattern)
            else:
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


class ContestPhase(Enum):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4


class ContestModel:
    def __init__(self):
        self.first_match_model = MatchModel()
        self.second_match_models = [MatchModel(), MatchModel()]
        self.third_match_models = [MatchModel(), MatchModel(), MatchModel()]
        self.fourth_match_models = [MatchModel(), MatchModel(), MatchModel(), MatchModel()]

        self.init_first_match_model()

    def init_first_match_model(self):
        # Generate first match list
        team_model_copy = team_model.team_list
        shuffle(team_model_copy)
        for i in range(0, len(team_model_copy), 2):
            if i == len(team_model_copy) - 1:
                self.first_match_model.add_match(Match(team_model_copy[i]))
            else:
                self.first_match_model.add_match(Match(team_model_copy[i], team_model_copy[i + 1]))
