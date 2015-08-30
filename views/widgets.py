import pprint
from PySide.QtCore import Qt, QLine
from PySide.QtGui import QWidget, QLabel, QTableView, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, \
    QIcon, QAbstractItemView, QDialog, QMessageBox, QGridLayout, QPainter, QColor
from domain.championship.models import ChampionshipModel

from domain.four_matches.models import ContestModel, team_model
from views.dialogs import TeamDialog, ContestStatusDialog

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

        # ContestModel creation
        self.contest_model = ContestModel()

        # Currently selected match (for later use)
        self.selected_table_view = None
        self.selected_index = None

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

        # Table views & labels
        self.match_views = (
            QTableView(),
            [QTableView(), QTableView()],
            [QTableView(), QTableView(), QTableView()],
            [QTableView(), QTableView(), QTableView(), QTableView()]
        )
        match_layout = self.create_match_layout()

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

    def create_match_layout(self):
        match_layout = QHBoxLayout()
        for phase in range(0, 4):
            label = QLabel("Match #%d" % (phase + 1))
            label.setAlignment(Qt.AlignCenter)
            layout = QVBoxLayout()
            layout.addWidget(label)
            if phase == 0:
                self.setup_view(self.contest_model.match_models[phase], self.match_views[0])
                layout.addWidget(self.match_views[0])
                selection_model = self.match_views[0].selectionModel()
                selection_model.currentChanged.connect(self.selection_slot)
            else:
                for i in range(0, phase + 1):
                    label = QLabel("({0}/{1})".format(phase - i, i))
                    label.setAlignment(Qt.AlignCenter)
                    self.setup_view(self.contest_model.match_models[phase][phase - i],
                                    self.match_views[phase][phase - i])
                    selection_model = self.match_views[phase][phase - i].selectionModel()
                    selection_model.currentChanged.connect(self.selection_slot)
                    layout.addWidget(label)
                    layout.addWidget(self.match_views[phase][phase - i])

            match_layout.addLayout(layout)

        return match_layout

    def selection_slot(self, selected):
        if selected.column() == 0:
            team_left_name = selected.data()
            team_right_name = selected.sibling(selected.row(), 1).data()
        else:
            team_left_name = selected.sibling(selected.row(), 0).data()
            team_right_name = selected.data()

        team_left = team_model.get_team_from_name(team_left_name)
        team_right = team_model.get_team_from_name(team_right_name)

        self.first_team_button.setText(str(team_left))
        self.second_team_button.setText(str(team_right))
        self.first_team_button.setEnabled(True)
        self.second_team_button.setEnabled(True)
        if team_right is not None and team_left is not None and team_right in team_left.played_against:
            if team_left.played_against[team_right]:
                self.first_team_button.setChecked(True)
            else:
                self.second_team_button.setChecked(True)
        else:
            self.clear_selected_winner()

        self.clear_table_selection(selected)

    def clear_table_selection(self, selected_index):
        model = selected_index.model()
        view = self.match_views[0]
        if view.model() is not model:
            view.clearSelection()
        for phase in self.match_views[1:]:
            for view in phase:
                if view.model() is not model:
                    view.clearSelection()

    def winner_selected_slot(self):
        # Enable/Disable validate button
        self.validate_button.setEnabled(self.button_group.checkedButton() is not None)

    def set_winner_validate_button_slot(self):
        if self.first_team_button.isChecked():
            winner = team_model.get_team_from_name(self.first_team_button.text().split(' (')[0])
        else:
            winner = team_model.get_team_from_name(self.second_team_button.text().split(' (')[0])

        # print("Winner button clicked ! Winner is %s" % winner)
        self.contest_model.set_winner(winner)

    def clear_selected_winner(self):
        self.button_group.setExclusive(False)
        for button in self.button_group.buttons():
            button.setChecked(False)

        self.button_group.setExclusive(True)

    def show_status_view(self):
        dialog = ContestStatusDialog(self.contest_model.team_list)
        dialog.exec_()


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


def get_parent_list(local_list):
    return set([it[0].parent for it in local_list])


class ChampionshipWidget(QWidget):
    def __init__(self, parent=None):
        super(ChampionshipWidget, self).__init__(parent)

        self.data = {}
        self.leave_list = []
        self.__grid = QGridLayout()
        self.model = ChampionshipModel(team_model.team_list)
        self.make_leave_list()
        self.init_ui()

    def init_ui(self):
        leave_count = len(self.model.graph.leaves)
        self.setup_first_column(leave_count)
        self.setLayout(self.__grid)

    def setup_first_column(self, leave_count):
        for i in range(0, (leave_count * 2) - 1):
            if i % 2 == 0:
                label = self.create_team_label(str(self.model.graph.leaves[i // 2]))
                self.__grid.addWidget(label, i, 0)

    def make_leave_list(self):
        graph = self.model.graph
        for i in range(0, graph.level_count()):
            self.data[i] = []

        top = 0
        left = 0
        self.data[0] = []
        for leave in graph.leaves:
            self.data[0].append((leave, top, left))
            top += 2

        for level in range(0, graph.level_count()):
            print('Building level', level)
            for item in self.data[level]:
                sibling = graph.get_sibling(item[0])
                print('Item :', item[0], str((item[1], item[2])), '( sibling', sibling, ')')
                if sibling is not None and sibling in [it[0] for it in self.data[level]]:  # Classic
                    sibling_tuple = [it for it in self.data[level] if it[0] == sibling][0]
                    parent = item[0].parent
                    if item[0].parent not in [it[0] for it in self.data[level + 1]]:
                        if sibling_tuple[1] < item[1]:
                            new_tuple = (parent, item[1] - (2 ** level), item[2] + 2)
                            self.data[level + 1].append(new_tuple)
                            self.add_bracket(sibling_tuple[1], item[1], new_tuple[1], item[2] + 1)
                            self.__grid.addWidget(self.create_team_label(str(new_tuple[0])), new_tuple[1], new_tuple[2])
                        else:
                            new_tuple = (parent, item[1] + (2 ** level), item[2] + 2)
                            self.data[level + 1].append(new_tuple)
                            self.add_bracket(item[1], sibling_tuple[1], new_tuple[1], item[2] + 1)
                            self.__grid.addWidget(self.create_team_label(str(new_tuple[0])), new_tuple[1], new_tuple[2])
                elif item[0].parent is not None and item[0].parent not in [it[0] for it in self.data[level + 1]]:
                    new_tuple = (item[0].parent, item[1] - (2 ** level), item[2] + 4)
                    self.data[level + 2].append(new_tuple)
                    self.__grid.addWidget(self.create_team_label(str(new_tuple[0])), new_tuple[1], new_tuple[2])

    def add_bracket(self, top, bottom, middle, left):
        self.__grid.addWidget(WestToSouth(self.__grid, top, left), top, left)
        top_height = middle - top - 1
        for i in range(0, top_height):
            top += 1
            self.__grid.addWidget(VerticalLine(self.__grid, top, left), top, left)
        top += 1
        self.__grid.addWidget(TShaped(self.__grid, top, left), top, left)
        bottom_height = bottom - middle - 1
        for i in range(0, bottom_height):
            top += 1
            self.__grid.addWidget(VerticalLine(self.__grid, top, left), top, left)
        top += 1
        self.__grid.addWidget(WestToNorth(self.__grid, top, left), top, left)

    def add_line(self, top, left):
        for i in range(0, 2):
            self.__grid.addWidget(HorizontalLine(self.__grid, top, left + i), top, left + i)

    @staticmethod
    def create_team_label(label_text):
        label = QLabel(label_text)
        label.setMaximumWidth(125)
        label.setAlignment(Qt.AlignCenter)
        return label

    def add_widget(self, widget, row, column):
        self.__grid.addWidget(widget, row, column)


class CustomWidget(QWidget):
    def __init__(self, grid, row, column, parent=None):
        super(CustomWidget, self).__init__(parent)
        self.grid = grid
        self.idx = (row, column)

    def paintEvent(self, *args, **kwargs):
        qp = QPainter()
        qp.begin(self)
        self.draw_rectangle(qp)
        qp.end()


class WestToSouth(CustomWidget):
    def __init__(self, grid, row, column, parent=None):
        super(WestToSouth, self).__init__(grid, row, column, parent)

    def draw_rectangle(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)
        rect = self.grid.cellRect(self.idx[0], self.idx[1])
        qp.drawLine(QLine(0, rect.height() // 2, rect.width() // 2, rect.height() // 2))
        qp.drawLine(QLine(rect.width() // 2, rect.height() // 2, rect.width() // 2, rect.height()))


class WestToNorth(CustomWidget):
    def __init__(self, grid, row, column, parent=None):
        super(WestToNorth, self).__init__(grid, row, column, parent)

    def draw_rectangle(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)
        rect = self.grid.cellRect(self.idx[0], self.idx[1])
        qp.drawLine(QLine(0, rect.height() // 2, rect.width() // 2, rect.height() // 2))
        qp.drawLine(QLine(rect.width() // 2, rect.height() // 2, rect.width() // 2, 0))


class TShaped(CustomWidget):
    def __init__(self, grid, row, column, parent=None):
        super(TShaped, self).__init__(grid, row, column, parent)

    def draw_rectangle(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)
        rect = self.grid.cellRect(self.idx[0], self.idx[1])
        qp.drawLine(QLine(rect.width() // 2, 0, rect.width() // 2, rect.height()))
        qp.drawLine(QLine(rect.width() // 2, rect.height() // 2, rect.width(), rect.height() // 2))


class VerticalLine(CustomWidget):
    def __init__(self, grid, row, column, parent=None):
        super(VerticalLine, self).__init__(grid, row, column, parent)

    def draw_rectangle(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)
        rect = self.grid.cellRect(self.idx[0], self.idx[1])
        qp.drawLine(QLine(rect.width() // 2, 0, rect.width() // 2, rect.height()))


class HorizontalLine(CustomWidget):
    def __init__(self, grid, row, column, parent=None):
        super(HorizontalLine, self).__init__(grid, row, column, parent)

    def draw_rectangle(self, qp):
        color = QColor(0, 0, 0)
        qp.setPen(color)
        rect = self.grid.cellRect(self.idx[0], self.idx[1])
        qp.drawLine(QLine(0, rect.height() // 2, rect.width(), rect.height() // 2))
