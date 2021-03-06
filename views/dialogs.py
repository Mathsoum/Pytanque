from PySide import QtCore

from PySide.QtCore import Qt
from PySide.QtGui import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QLabel, QRadioButton
from domain.data_structures import Team

__author__ = 'msoum'


class TeamDialog(QDialog):
    def __init__(self, parent=None, name='', club=''):
        super(TeamDialog, self).__init__(parent)

        # Line edits
        self.name_edit = QLineEdit(name)
        self.club_edit = QLineEdit(club)

        # Form layout
        form_layout = QFormLayout()
        form_layout.addRow('Name', self.name_edit)
        form_layout.addRow('Club', self.club_edit)

        # Button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        button_box_layout = QHBoxLayout()
        button_box_layout.addStretch(1)
        button_box_layout.addWidget(button_box)

        # Dialog layout
        dialog_layout = QVBoxLayout()
        dialog_layout.addLayout(form_layout)
        dialog_layout.addStretch()
        dialog_layout.addLayout(button_box_layout)

        self.setLayout(dialog_layout)


class ContestStatusDialog(QDialog):
    def __init__(self, team_list, parent=None):
        super(ContestStatusDialog, self).__init__(parent)

        self.setWindowTitle('Contest status')

        team_list_copy = sorted(team_list, key=lambda it: it.number)
        if Team('###', '###') in team_list_copy:
            team_list_copy.remove(Team('###', '###'))

        layout = QGridLayout()
        self.create_header_line(layout)
        for team in team_list_copy:
            row = team_list_copy.index(team) + 1
            num = QLabel(str(team.number))
            num.setAlignment(Qt.AlignCenter)
            layout.addWidget(num, row, 0)
            name = QLabel(team.name)
            name.setAlignment(Qt.AlignCenter)
            layout.addWidget(name, row, 1)
            club = QLabel(team.club)
            club.setAlignment(Qt.AlignCenter)
            layout.addWidget(club, row, 2)
            col = 3
            win_count = 0
            lose_count = 0
            for k, v in team.played_against.items():
                if v:
                    label = QLabel('W')
                    label.setStyleSheet("QLabel { color: green }")
                    label.setAlignment(Qt.AlignCenter)
                    win_count += 1
                else:
                    label = QLabel('L')
                    label.setStyleSheet("QLabel { color: red }")
                    label.setAlignment(Qt.AlignCenter)
                    lose_count += 1

                layout.addWidget(label, row, col)
                col += 1

            for i in range(col, 7):
                layout.addWidget(QLabel(), row, i)

            layout.addWidget(QLabel('(%d,%d)' % (win_count, lose_count)))

        self.setLayout(layout)

    @staticmethod
    def create_header_line(layout):
        num = QLabel('N°')
        num.setAlignment(Qt.AlignCenter)
        layout.addWidget(num, 0, 0)
        name = QLabel('Name')
        name.setAlignment(Qt.AlignCenter)
        layout.addWidget(name, 0, 1)
        club = QLabel('Club')
        club.setAlignment(Qt.AlignCenter)
        layout.addWidget(club, 0, 2)
        match1 = QLabel('#1')
        match1.setAlignment(Qt.AlignCenter)
        layout.addWidget(match1, 0, 3)
        match2 = QLabel('#2')
        match2.setAlignment(Qt.AlignCenter)
        layout.addWidget(match2, 0, 4)
        match3 = QLabel('#3')
        match3.setAlignment(Qt.AlignCenter)
        layout.addWidget(match3, 0, 5)
        match4 = QLabel('#4')
        match4.setAlignment(Qt.AlignCenter)
        layout.addWidget(match4, 0, 6)
        total = QLabel('Total')
        total.setAlignment(Qt.AlignCenter)
        layout.addWidget(total, 0, 7)


class ChampionshipMatchDialog(QDialog):
    def __init__(self, node):
        super().__init__(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        self.selection = None

        first = node.left
        second = node.right

        layout = QGridLayout()
        self.first_button = QRadioButton(first.data.name)
        self.first_button.toggled.connect(self.selection_changed)
        layout.addWidget(self.first_button, 0, 0)
        self.second_button = QRadioButton(second.data.name)
        self.second_button.toggled.connect(self.selection_changed)
        layout.addWidget(self.second_button, 1, 0)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        button_box_layout = QHBoxLayout()
        button_box_layout.addStretch(1)
        button_box_layout.addWidget(self.button_box)
        self.button_box.button(QDialogButtonBox.Ok).setEnabled(False)

        layout.addLayout(button_box_layout, 2, 0)

        self.setLayout(layout)

    def selection_changed(self):
        if self.first_button.isChecked():
            self.selection = self.first_button.text()
        else:
            self.selection = self.second_button.text()

        self.button_box.button(QDialogButtonBox.Ok).setEnabled(True)

