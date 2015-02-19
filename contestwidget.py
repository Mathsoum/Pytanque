from PySide.QtGui import QWidget, QButtonGroup, QTableView, QRadioButton, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from PySide.QtCore import Qt

__author__ = 'Mathieu'


class ContestWidget(QWidget):
    def __init__(self):
        super(ContestWidget, self).__init__()

        # Table views & labels
        self.first_match_label = QLabel("Match #1")
        self.first_match_label.setAlignment(Qt.AlignCenter)
        self.first_match_table_view = QTableView()
        first_match_layout = QVBoxLayout()
        first_match_layout.addWidget(self.first_match_label)
        first_match_layout.addWidget(self.first_match_table_view)

        self.second_match_label = QLabel("Match #2")
        self.second_match_label.setAlignment(Qt.AlignCenter)
        self.second_match_table_view = QTableView()
        second_match_layout = QVBoxLayout()
        second_match_layout.addWidget(self.second_match_label)
        second_match_layout.addWidget(self.second_match_table_view)

        self.third_match_label = QLabel("Match #3")
        self.third_match_label.setAlignment(Qt.AlignCenter)
        self.third_match_table_view = QTableView()
        third_match_layout = QVBoxLayout()
        third_match_layout.addWidget(self.third_match_label)
        third_match_layout.addWidget(self.third_match_table_view)

        self.fourth_match_label = QLabel("Match #4")
        self.fourth_match_label.setAlignment(Qt.AlignCenter)
        self.fourth_match_table_view = QTableView()
        fourth_match_layout = QVBoxLayout()
        fourth_match_layout.addWidget(self.fourth_match_label)
        fourth_match_layout.addWidget(self.fourth_match_table_view)

        match_layout = QHBoxLayout()
        match_layout.addLayout(first_match_layout)
        match_layout.addLayout(second_match_layout)
        match_layout.addLayout(third_match_layout)
        match_layout.addLayout(fourth_match_layout)

        # Winning team selector
        first_team_button = QRadioButton("Team #1")
        second_team_button = QRadioButton("Team #2")
        self.button_group = QButtonGroup()
        self.button_group.addButton(first_team_button)
        self.button_group.addButton(second_team_button)
        team_button_layout = QHBoxLayout()
        team_button_layout.addStretch(1)
        team_button_layout.addWidget(first_team_button)
        team_button_layout.addWidget(second_team_button)
        team_button_layout.addStretch(1)
        validate_button = QPushButton("Validate")
        validate_button_layout = QHBoxLayout()
        validate_button_layout.addStretch(1)
        validate_button_layout.addWidget(validate_button)
        validate_button_layout.addStretch(1)

        main_layout = QVBoxLayout()
        main_layout.addLayout(match_layout)
        main_layout.addLayout(team_button_layout)
        main_layout.addLayout(validate_button_layout)

        self.setLayout(main_layout)

