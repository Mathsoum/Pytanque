from PySide.QtGui import QAction, QMainWindow
from domain.models import team_model
from views.widgets import RegistrationWidget, ContestWidget

__author__ = 'Mathieu'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        menu_bar = self.menuBar()

        # Action menu
        self.action_menu = menu_bar.addMenu('A&ction')
        self.generate_match_action = QAction('&Generate matches', self)
        self.action_menu.addAction(self.generate_match_action)

        # Team menu
        self.team_menu = menu_bar.addMenu('&Team')
        self.team_del_action = QAction('&Delete a team', self)
        self.team_edt_action = QAction('&Edit a team', self)
        self.team_add_action = QAction('&Add a team', self)
        self.team_menu.addAction(self.team_add_action)
        self.team_menu.addAction(self.team_edt_action)
        self.team_menu.addAction(self.team_del_action)

        # Central widget
        central_widget = RegistrationWidget()
        central_widget.set_model(team_model)
        self.setCentralWidget(central_widget)

        # Connect action to slots
        self.generate_match_action.triggered.connect(self.start_contest)
        self.team_add_action.triggered.connect(central_widget.add_new_team_slot)
        self.team_edt_action.triggered.connect(central_widget.edt_team_slot)
        self.team_del_action.triggered.connect(central_widget.del_team_slot)

        # Setup main window
        self.setWindowTitle('Pétanque')
        self.resize(500, 400)

    def start_contest(self):
        self.generate_match_action.setEnabled(False)
        self.team_menu.setEnabled(False)
        self.setCentralWidget(ContestWidget())
        self.resize(900, 700)
        self.showMaximized()
