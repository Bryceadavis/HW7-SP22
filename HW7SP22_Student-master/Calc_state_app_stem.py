import numpy as np 
from Calc_state import Steam_SI as steam  # import any of your own classes as you wish

import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QCursor
from PyQt5.QtCore import Qt

from Calc_state_gui import Ui_Form  # from the GUI file your created


class main_window(QWidget, Ui_Form):
    def __init__(self):
        """
        Constructor for the main window of the application.  This class inherits from QWidget and Ui_Form
        """
        super().__init__()  # run constructor of parent classes
        self.setupUi(self)  # run setupUi() (see Ui_Form)
        # $JES MISSING CODE$ ('Steam Property Calculator') # set the window title

        self.Steam = steam()  # instantiate a steam object
        # create a list of the check boxes on the main window
        self.checkBoxes = [self.chk_Press, self.chk_Temp, self.chk_Quality, self.chk_Enthalpy, self.chk_Entropy,
                           self.chk_SpV]

        self.assign_widgets()  # connects signals and slots
        self.show()

    def assign_widgets(self):
        # $JES MISSING CODE$  connect clicked signal of pushButton_Exit to self.ExitApp
        # $JES MISSING CODE$  connect clicked signal of pushButton_Calculate to self.Calculate
        self.pushButton_Exit.clicked.connect(self.ExitApp)
        self.pushButton_Calculate.clicked.connect(self.Calculate)

    def Calculate(self):
        """
        Here, we need to scan through the check boxes and ensure that only two are selected a defining properties
        for calculating the state of the steam.  Then set the properties of the steam object and calculate the
        steam state.  Finally, output the results to the line edit widgets.
        :return:
        """
        # make sure only two boxes checked
        nChecked = 0
        for c in self.checkBoxes:
            nChecked += 1 if c.isChecked() else 0
        if nChecked != 2:
            return

        self.Steam.P = float(self.le_P.text()) if self.chk_Press.isChecked() else None
        self.Steam.T = float(self.le_T.text()) if self.chk_Temp.isChecked() else None
        self.Steam.x = float(self.le_Q.text()) if self.chk_Quality.isChecked() else None
        self.Steam.h = float(self.le_H.text()) if self.chk_Enthalpy.isChecked() else None
        self.Steam.s = float(self.le_S.text()) if self.chk_Entropy.isChecked() else None
        self.Steam.v = float(self.le_SpV.text()) if self.chk_SpV.isChecked() else None

        self.Steam.calc()
        state = self.Steam
        self.le_P.setText(str(round(self.Steam.P, 4)))
        self.le_T.setText(str(round(self.Steam.T, 4)))
        self.le_Q.setText(str(round(self.Steam.x, 4)))
        self.le_H.setText(str(round(self.Steam.h, 4)))
        self.le_S.setText(str(round(self.Steam.s, 4)))
        self.le_SpV.setText(str(round(self.Steam.v, 4)))
        self.lbl_Properties.setText((str(self.Steam.region)))
        return

    def ExitApp(self):
        app.exit()

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())
    
 





