import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtWidgets as qtw
from Rankine_GUI import Ui_Form  # from the GUI file your created
import rankineFile

class main_window(qtw.QWidget, Ui_Form):
    def __init__(self):
        """
        Constructor for the main window of the application.  This class inherits from QWidget and Ui_Form
        """
        super().__init__()  # run constructor of parent classes
        self.setupUi(self)  # run setupUi() (see Ui_Form)
        self.setWindowTitle('Rankine Cycle Calculator')  # set the window title
        # create a list of the labels on the main window

        self.Rankine = rankineFile.rankine()
        if self.rdo_Quality.clicked:
            self.btn_Calculate.clicked.connect(self.Calculate)
        elif self.rdo_THigh.clicked:
            self.btn_Calculate.clicked.connect(self.Calculate)
        self.show()

    def Calculate(self):
        """
        Here, we need to scan through the check boxes and ensure that only two are selected a defining properties
        for calculating the state of the steam.  Then set the properties of the steam object and calculate the
        steam state.  Finally, output the results to the line edit widgets.
        :return:
        """
        self.Rankine.p_high = (self.le_PHigh.text()) if self.le_PHigh.isEnabled() else None
        self.Rankine.p_low = (self.le_PLow.text()) if self.le_PLow.isEnabled() else None
        self.Rankine.efficiency= (self.le_Efficiency.text())  if self.le_Efficiency.isEnabled() else None
        self.Rankine.eff_turbine= (self.le_TurbineInletCondition.text())  if self.le_TurbineEff.isEnabled() else None

        self.Rankine.calc_efficiency()
        state = self.Rankine
        self.le_H1.setText(self.rankine.state1)
        self.le_H2.setText(self.rankine.state2)
        self.le_H3.setText(self.rankine.state3)
        self.le_H4.setText(self.rankine.state4)
        self.le_HeatAdded.setText(self.rankine.heat_added)
        self.le_PumpWork.setText(self.rankine.pump_work)
        self.le_Efficiency.setText(self.rankine.efficiency)
        self.le_TurbineWork.setText(self.rankine.turbine_work)
        self.show()
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
