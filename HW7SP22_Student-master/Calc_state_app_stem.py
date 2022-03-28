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
        self.setWindowTitle( 'Steam Property Calculator') #&AKO
        self.Steam = steam()  # instantiate a steam object
        # create a list of the check boxes on the main window
        self.checkBoxes = [self.chk_Press, self.chk_Temp, self.chk_Quality, self.chk_Enthalpy, self.chk_Entropy,
                           self.chk_SpV]

        self.assign_widgets()  # connects signals and slots
        self.show()

    def assign_widgets(self):
        """This function controls what happens when the GUI buttons are clicked."""
        self.pushButton_Exit.clicked.connect(self.ExitApp) #closes app when exit is clicked
        self.pushButton_Calculate.clicked.connect(self.Calculate) #calls Calculate function when Calculate is clicked

    def Calculate(self):
        """
        Here, we need to scan through the check boxes and ensure that only two are selected and define properties
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

        self.Steam.P = float(self.le_P.text()) if self.chk_Press.isChecked() else None #converts typed number to float and assigns to steam parameter if box is checked
        self.Steam.T = float(self.le_T.text()) if self.chk_Temp.isChecked() else None
        self.Steam.x = float(self.le_Q.text()) if self.chk_Quality.isChecked() else None
        self.Steam.h = float(self.le_H.text()) if self.chk_Enthalpy.isChecked() else None
        self.Steam.s = float(self.le_S.text()) if self.chk_Entropy.isChecked() else None
        self.Steam.v = float(self.le_SpV.text()) if self.chk_SpV.isChecked() else None

        self.Steam.calc()
        state = self.Steam #not used
        self.le_P.setText("{:.2f}".format(self.Steam.P)) #&AKO altered to match HW doc decimal places
        self.le_T.setText("{:.2f}".format(self.Steam.T)) #edits line outputs;prints what you input as well as what is calculated from your inputs to GUI
        self.le_Q.setText("{:.4f}".format(self.Steam.x))
        self.le_H.setText("{:.2f}".format(self.Steam.h))
        self.le_S.setText("{:.4f}".format(self.Steam.s))
        self.le_SpV.setText("{:.5f}".format(self.Steam.v))
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
    
 





