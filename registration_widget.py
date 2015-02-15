from PySide.QtGui import QWidget, QPushButton, QIcon, QVBoxLayout, QHBoxLayout, QTableView, QAbstractItemView, QDialog, \
    QMessageBox

from team_dialog import TeamDialog


__author__ = 'Mathieu'


class RegistrationWidget(QWidget):
    def __init__(self):
        super(RegistrationWidget, self).__init__()

        # Model initialisation
        self.model = None

        # Table view
        self.table_view = QTableView()

        # Buttons
        self.add_button = QPushButton(QIcon('icons/add.png'), '&Add', self)
        self.edt_button = QPushButton(QIcon('icons/edit.png'), '&Edit', self)
        self.del_button = QPushButton(QIcon('icons/delete.png'), '&Delete', self)
        vbox = QVBoxLayout()
        vbox.addWidget(self.add_button)
        vbox.addWidget(self.edt_button)
        vbox.addWidget(self.del_button)
        vbox.addStretch(1)

        # HBox
        hbox = QHBoxLayout()
        hbox.addWidget(self.table_view)
        hbox.addLayout(vbox)

        # Set layout
        self.setLayout(hbox)

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
        dialog = TeamDialog(self, 'Some', 'Team')
        if dialog.exec_() == QDialog.Accepted:
            print('OK dialog')

    def del_team_slot(self):
        dialog = QMessageBox(self)
        dialog.setText('Du you really wish to delete this team ?')
        dialog.setInformativeText('Some (Team)')
        dialog.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        dialog.setDefaultButton(QMessageBox.Cancel)
        if dialog.exec_() == QMessageBox.Ok:
            # Delete team from model
            pass

