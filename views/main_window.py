from PySide.QtGui import QAction, QMainWindow

from domain.four_matches.models import team_model
from views.widgets import RegistrationWidget, ContestWidget, ChampionshipWidget

__author__ = 'Mathieu'


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        menu_bar = self.menuBar()

        # Action menu
        self.action_menu = menu_bar.addMenu('A&ction')
        self.generate_contest_action = QAction('Generate &contest', self)
        self.generate_championship_action = QAction('Generate c&hampionship', self)
        self.action_menu.addAction(self.generate_contest_action)
        self.action_menu.addAction(self.generate_championship_action)

        # Team menu
        self.team_menu = menu_bar.addMenu('&Team')
        self.team_del_action = QAction('&Delete a team', self)
        self.team_edt_action = QAction('&Edit a team', self)
        self.team_add_action = QAction('&Add a team', self)
        self.team_menu.addAction(self.team_add_action)
        self.team_menu.addAction(self.team_edt_action)
        self.team_menu.addAction(self.team_del_action)

        # View menu
        self.view_menu = menu_bar.addMenu('V&iew')
        self.status_action = QAction('Show s&tatus...', self)
        self.view_menu.addAction(self.status_action)
        self.status_action.setEnabled(False)

        # Central widget
        central_widget = RegistrationWidget()
        central_widget.set_model(team_model)
        self.setCentralWidget(central_widget)

        # Connect action to slots
        self.generate_contest_action.triggered.connect(self.start_contest)
        self.generate_championship_action.triggered.connect(self.start_championship)
        self.team_add_action.triggered.connect(central_widget.add_new_team_slot)
        self.team_edt_action.triggered.connect(central_widget.edt_team_slot)
        self.team_del_action.triggered.connect(central_widget.del_team_slot)

        # Setup main window
        self.setWindowTitle('Pytanque')
        self.resize(500, 400)

    def start_contest(self):
        self.generate_contest_action.setEnabled(False)
        self.generate_championship_action.setEnabled(False)
        self.team_menu.setEnabled(False)
        self.status_action.setEnabled(True)
        contest_widget = ContestWidget()
        self.setCentralWidget(contest_widget)
        self.status_action.triggered.connect(contest_widget.show_status_view)
        self.resize(900, 700)
        self.showMaximized()

    def start_championship(self):
        self.generate_contest_action.setEnabled(False)
        self.generate_championship_action.setEnabled(False)
        self.team_menu.setEnabled(False)
        championship_widget = ChampionshipWidget()
        self.setCentralWidget(championship_widget)
        self.resize(900, 700)
        self.showMaximized()
