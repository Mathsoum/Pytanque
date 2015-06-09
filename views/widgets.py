from PySide.QtCore import Qt
from PySide.QtGui import QWidget, QLabel, QTableView, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, \
    QIcon, QAbstractItemView, QDialog, QMessageBox
from domain.models import ContestModel
from views.dialogs import TeamDialog

__author__ = 'msoum'


class ContestWidget(QWidget):
    @staticmethod
    def setup_view(model, view):
        view.setModel(model)
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.setSelectionMode(QAbstractItemView.SingleSelection)
        view.setColumnWidth(0, 100)
        view.setColumnWidth(1, 100)

    def __init__(self):
        super(ContestWidget, self).__init__()

        # Currently selected match (for later use)
        self.selected_table_view = None
        self.selected_index = None

        # ContestModel creation
        self.contest_model = ContestModel()

        # Table views & labels
        self.first_match_view = QTableView()
        self.second_match_views = [QTableView(), QTableView()]
        self.third_match_views = [QTableView(), QTableView(), QTableView()]
        self.fourth_match_views = [QTableView(), QTableView(), QTableView(), QTableView()]

        # First round
        first_match_layout = self.setup_first_match_view()
        # Second round
        second_match_layout = self.setup_second_match_view()
        # Third round
        third_match_layout = self.setup_third_match_view()
        # Fourth round
        fourth_match_layout = self.setup_forth_match_view()

        match_layout = QHBoxLayout()
        match_layout.addLayout(first_match_layout)
        match_layout.addLayout(second_match_layout)
        match_layout.addLayout(third_match_layout)
        match_layout.addLayout(fourth_match_layout)

        # Winning team selector
        self.first_team_button = QRadioButton("Team #1")
        self.first_team_button.toggled.connect(self.winner_selected_slot)
        self.first_team_button.setEnabled(False)
        self.second_team_button = QRadioButton("Team #2")
        self.second_team_button.toggled.connect(self.winner_selected_slot)
        self.second_team_button.setEnabled(False)

        # Selectors in button group for better management
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.first_team_button)
        self.button_group.addButton(self.second_team_button)

        # Winner selector layout
        winner_selector_layout = QHBoxLayout()
        winner_selector_layout.addStretch(1)
        winner_selector_layout.addWidget(self.first_team_button)
        winner_selector_layout.addWidget(self.second_team_button)
        winner_selector_layout.addStretch(1)

        # Validate button
        self.validate_button = QPushButton("Validate")
        self.validate_button.setEnabled(False)
        self.validate_button.clicked.connect(self.set_winner_validate_button_slot)

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

    def setup_first_match_view(self):
        label = QLabel("Match #1")
        label.setAlignment(Qt.AlignCenter)
        self.setup_view(self.contest_model.first_match_model, self.first_match_view)
        selection_model = self.first_match_view.selectionModel()
        selection_model.currentChanged.connect(self.selection_changed_first_view)
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.first_match_view)
        return layout

    def setup_second_match_view(self):
        label = QLabel("Match #2")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        phase = 1
        for i in range(0, phase + 1):
            label = QLabel("({0}/{1})".format(phase - i, i))
            label.setAlignment(Qt.AlignCenter)
            self.setup_view(self.contest_model.second_match_models[i], self.second_match_views[i])
            layout.addWidget(label)
            layout.addWidget(self.second_match_views[i])

        return layout

    def setup_third_match_view(self):
        label = QLabel("Match #3")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        phase = 2
        for i in range(0, phase + 1):
            label = QLabel("({0}/{1})".format(phase - i, i))
            label.setAlignment(Qt.AlignCenter)
            self.setup_view(self.contest_model.third_match_models[i], self.third_match_views[i])
            layout.addWidget(label)
            layout.addWidget(self.third_match_views[i])

        return layout

    def setup_forth_match_view(self):
        label = QLabel("Match #4")
        label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(label)
        phase = 3
        for i in range(0, phase + 1):
            label = QLabel("({0}/{1})".format(phase - i, i))
            label.setAlignment(Qt.AlignCenter)
            self.setup_view(self.contest_model.fourth_match_models[i], self.fourth_match_views[i])
            layout.addWidget(label)
            layout.addWidget(self.fourth_match_views[i])

        return layout

    def selection_changed_first_view(self):
        self.selected_table_view = self.first_match_view
        self.selection_changed()

    def selection_changed_second_one_win_view(self):
        self.selected_table_view = self.second_match_views[0]
        self.selection_changed()

    def selection_changed_second_no_win_view(self):
        self.selected_table_view = self.second_match_views[1]
        self.selection_changed()

    def selection_changed_third_no_win_view(self):
        self.selected_table_view = self.third_match_views[0]
        self.selection_changed()

    def selection_changed_third_one_win_view(self):
        self.selected_table_view = self.third_match_views[1]
        self.selection_changed()

    def selection_changed_third_two_win_view(self):
        self.selected_table_view = self.third_match_views[2]
        self.selection_changed()

    def selection_changed_fourth_no_win_view(self):
        self.selected_table_view = self.fourth_match_views[0]
        self.selection_changed()

    def selection_changed_fourth_one_win_view(self):
        self.selected_table_view = self.fourth_match_views[1]
        self.selection_changed()

    def selection_changed_fourth_two_win_view(self):
        self.selected_table_view = self.fourth_match_views[2]
        self.selection_changed()

    def selection_changed_fourth_three_win_view(self):
        self.selected_table_view = self.fourth_match_views[3]
        self.selection_changed()

    def selection_changed(self):
        self.selected_index = self.selected_table_view.currentIndex().row()
        selected_match = self.selected_table_view.model().get_match(self.selected_index)
        self.button_group.buttons()[0].setText(str(selected_match.first_team))
        self.button_group.buttons()[1].setText(str(selected_match.second_team))
        self.button_group.buttons()[0].setEnabled(True)
        self.button_group.buttons()[1].setEnabled(True)
        if selected_match.is_finished():
            if str(selected_match.winner) == self.button_group.buttons()[0].text():
                self.button_group.buttons()[0].setChecked(True)
            else:
                self.button_group.buttons()[1].setChecked(True)
        else:
            self.clear_selected_winner()

    def winner_selected_slot(self):
        # Enable/Disable validate button
        self.validate_button.setEnabled(self.button_group.checkedButton() is not None)

    def set_winner_validate_button_slot(self):
        match = self.selected_table_view.model().get_match(self.selected_index)
        if self.first_team_button.isChecked():
            self.selected_table_view.model().set_winner(match.first_team)
        else:
            self.selected_table_view.model().set_winner(match.second_team)

    def clear_selected_winner(self):
        self.button_group.setExclusive(False)
        for button in self.button_group.buttons():
            button.setChecked(False)

        self.button_group.setExclusive(True)


class RegistrationWidget(QWidget):
    def __init__(self):
        super(RegistrationWidget, self).__init__()

        # Model initialisation
        self.model = None

        # Table view
        self.table_view = QTableView()

        # Buttons
        self.add_button = QPushButton(QIcon('icons/add.png'), '&Add', self)
        self.add_button.clicked.connect(self.add_new_team_slot)
        self.edt_button = QPushButton(QIcon('icons/edit.png'), '&Edit', self)
        self.edt_button.clicked.connect(self.edt_team_slot)
        self.del_button = QPushButton(QIcon('icons/delete.png'), '&Delete', self)
        self.del_button.clicked.connect(self.del_team_slot)
        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edt_button)
        button_layout.addWidget(self.del_button)
        button_layout.addStretch(1)

        # HBox
        main_layout = QHBoxLayout()
        main_layout.addWidget(self.table_view)
        main_layout.addLayout(button_layout)

        # Set layout
        self.setLayout(main_layout)

    def set_model(self, new_model):
        self.model = new_model
        self.table_view.setModel(new_model)
        self.table_view.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table_view.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_view.setColumnWidth(0, 150)
        self.table_view.setColumnWidth(1, 150)

    def add_new_team_slot(self):
        dialog = TeamDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            print('OK dialog')
            print(dialog.name_edit.text(), dialog.club_edit.text())
            self.model.add_team(dialog.name_edit.text(), dialog.club_edit.text())

    def edt_team_slot(self):
        selected_team = self.selected_team()
        dialog = TeamDialog(self, selected_team.name, selected_team.club)
        if dialog.exec_() == QDialog.Accepted:
            self.model.update_team(selected_team, dialog.name_edit.text(), dialog.club_edit.text())

    def del_team_slot(self):
        dialog = QMessageBox(self)
        dialog.setText('Du you really wish to delete this team ?')
        selected_team = self.selected_team()
        dialog.setInformativeText('{0} ({1})'.format(selected_team.name, selected_team.club))
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Cancel)
        if dialog.exec_() == QMessageBox.Ok:
            self.model.delete_team(selected_team)

    def selected_team(self):
        selected_index = self.table_view.selectionModel().currentIndex().row()
        return self.model.get_team(selected_index)
