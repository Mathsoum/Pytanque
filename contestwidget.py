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
        first_team_button.toggled.connect(self.winner_selected_slot)
        second_team_button = QRadioButton("Team #2")
        second_team_button.toggled.connect(self.winner_selected_slot)

        # Selectors in button group for better management
        self.button_group = QButtonGroup()
        self.button_group.addButton(first_team_button)
        self.button_group.addButton(second_team_button)

        # Winner selector layout
        winner_selector_layout = QHBoxLayout()
        winner_selector_layout.addStretch(1)
        winner_selector_layout.addWidget(first_team_button)
        winner_selector_layout.addWidget(second_team_button)
        winner_selector_layout.addStretch(1)

        # Validate button
        self.validate_button = QPushButton("Validate")
        self.validate_button.setEnabled(False)
        self.validate_button.clicked.connect(self.clear_selected_winner)  # FIXME For test purposes only

        # Validate button layout
        validate_button_layout = QHBoxLayout()
        validate_button_layout.addStretch(1)
        validate_button_layout.addWidget(self.validate_button)
        validate_button_layout.addStretch(1)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(match_layout)
        main_layout.addLayout(winner_selector_layout)
        main_layout.addLayout(validate_button_layout)

        self.setLayout(main_layout)

    def winner_selected_slot(self):
        # Enable/Disable validate button
        self.validate_button.setEnabled(self.button_group.checkedButton() is not None)

    def clear_selected_winner(self):
        self.button_group.setExclusive(False)
        for button in self.button_group.buttons():
            button.setChecked(False)

        self.button_group.setExclusive(True)
