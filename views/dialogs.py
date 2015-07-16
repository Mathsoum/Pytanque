from PySide.QtGui import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QHBoxLayout, QVBoxLayout, QGridLayout, \
    QLabel

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

        layout = QGridLayout()
        self.create_header_line(layout)
        for team in team_list:
            layout.addWidget(QLabel(team.name), team_list.index(team) + 1, 0)
            layout.addWidget(QLabel(team.club), team_list.index(team) + 1, 1)

        self.setLayout(layout)

    @staticmethod
    def create_header_line(layout):
        layout.addWidget(QLabel('Name'), 0, 0)
        layout.addWidget(QLabel('Club'), 0, 1)
        layout.addWidget(QLabel('#1'), 0, 2)
        layout.addWidget(QLabel('#2'), 0, 3)
        layout.addWidget(QLabel('#3'), 0, 4)
        layout.addWidget(QLabel('#4'), 0, 5)
        layout.addWidget(QLabel('Total'), 0, 5)

