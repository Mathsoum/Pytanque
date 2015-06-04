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

        # Generate first match list
        team_model_copy = team_model.team_list
        shuffle(team_model_copy)
        self.match_list = []
        for i in range(0, len(team_model_copy), 2):
            if i == len(team_model_copy) - 1:
                self.match_list.append(Match(team_model_copy[i], Team('NO_NAME', 'NO_CLUB')))
            else:
                self.match_list.append(Match(team_model_copy[i], team_model_copy[i + 1]))

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
        print("Match : <%s> vs <%s>" % (match.first_team, match.second_team))
        print("Match : %s wins" % winner)
        match.set_finished(winner)
        print(self.match_list[idx].is_finished())
        print("Match : Index %d updated" % idx)
        self.dataChanged.emit(self.index(0, idx), self.index(1, idx))
