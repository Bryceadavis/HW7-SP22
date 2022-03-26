import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtWidgets as qtw
from Rankine_GUI import Ui_Form  # from the GUI file your created
import rankineFile
#banana
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
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.show()
    def Calculate(self):
        """
        Here, we need to scan through the check boxes and ensure that only two are selected a defining properties
        for calculating the state of the steam.  Then set the properties of the steam object and calculate the
        steam state.  Finally, output the results to the line edit widgets.
        :return:
        """
        if self.rdo_Quality.clicked:
            self.Rankine.p_high = float(self.le_PHigh.text()) if self.le_PHigh.isEnabled() else None
            self.Rankine.p_low = float(self.le_PLow.text()) if self.le_PLow.isEnabled() else None
            self.Rankine.efficiency = float(self.le_Efficiency.text()) if self.le_Efficiency.isEnabled() else None
            self.Rankine.eff_turbine = float(
                self.le_TurbineInletCondition.text()) if self.le_TurbineEff.isEnabled() else None

            self.Rankine.calc_efficiency()
            state = self.Rankine
            self.le_H1.setText(str(round(self.Rankine.state1.h, 2)))
            self.le_H2.setText(str(round(self.Rankine.state2.h, 2)))
            self.le_H3.setText(str(round(self.Rankine.state3.h, 2)))
            self.le_H4.setText(str(round(self.Rankine.state4.h, 2)))
            self.le_HeatAdded.setText(str(round(self.Rankine.heat_added, 2)))
            self.le_PumpWork.setText(str(round(self.Rankine.pump_work, 2)))
            self.le_Efficiency.setText(str(round(self.Rankine.efficiency, 2)))
            self.le_TurbineWork.setText(str(round(self.Rankine.turbine_work, 2)))
            self.show()
            return

        elif self.rdo_THigh.clicked:
            self.Rankine.p_high = float(self.le_PHigh.text()) if self.le_PHigh.isEnabled() else None
            self.Rankine.p_low = float(self.le_PLow.text()) if self.le_PLow.isEnabled() else None
            self.Rankine.efficiency = float(self.le_Efficiency.text()) if self.le_Efficiency.isEnabled() else None
            self.Rankine.eff_turbine = float(
                self.le_TurbineInletCondition.text()) if self.le_TurbineEff.isEnabled() else None

            self.Rankine.calc_efficiency()
            state = self.Rankine
            self.le_H1.setText(str(round(self.Rankine.state1.h, 2)))
            self.le_H2.setText(str(round(self.Rankine.state2.h, 2)))
            self.le_H3.setText(str(round(self.Rankine.state3.h, 2)))
            self.le_H4.setText(str(round(self.Rankine.state4.h, 2)))
            self.le_HeatAdded.setText(str(round(self.Rankine.heat_added, 2)))
            self.le_PumpWork.setText(str(round(self.Rankine.pump_work, 2)))
            self.le_Efficiency.setText(str(round(self.Rankine.efficiency, 2)))
            self.le_TurbineWork.setText(str(round(self.Rankine.turbine_work, 2)))
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