from PySide.QtGui import QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QHBoxLayout, QVBoxLayout

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