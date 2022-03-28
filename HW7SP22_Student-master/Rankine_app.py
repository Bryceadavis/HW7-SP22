import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui
from Rankine_GUI import Ui_Form  # from the GUI file your created
import rankineFile as rankineFile

class main_window(QWidget, Ui_Form):
    def __init__(self):
        """
        Constructor for the main window of the application.  This class inherits from QWidget and Ui_Form
        """
        super().__init__()  # run constructor of parent classes
        self.setupUi(self)  # run setupUi() (see Ui_Form)
        self.setWindowTitle('Rankine Cycle Calculator')  # set the window title
        # create a list of the labels on the main window
        self.Rankine = rankineFile.rankine()

        self.label = [self.le_PHigh, self.le_PLow, self.le_TurbineInletCondition, self.le_TurbineEff, self.le_H1,
                      self.le_H2, self.le_H3, self.le_H4, self.le_HeatAdded, self.le_PumpWork, self.le_Efficiency,
                      self.le_TurbineWork]
        self.btn_Calculate.clicked.connect(self.Calculate)
        self.show()
    def Calculate(self):
        """
        Here, we need to scan through the check boxes and ensure that only two are selected a defining properties
        for calculating the state of the steam.  Then set the properties of the steam object and calculate the
        steam state.  Finally, output the results to the line edit widgets.
        :return:
        """

        self.Rankine.p_high = float(self.le_PHigh.text())*100
        self.Rankine.p_low = float(self.le_PLow.text())*100
        self.Rankine.eff_turbine = float(self.le_TurbineEff.text())
        self.Rankine.quality = float(self.le_TurbineInletCondition.text()) if self.rdo_Quality.isChecked() else None
        self.Rankine.t_high = float(self.le_TurbineInletCondition.text()) if self.rdo_THigh.isChecked() else None
        self.Rankine.calc_efficiency()


        self.le_H1.setText("{:.2f}".format(self.Rankine.state1.h))
        self.le_H2.setText("{:.2f}".format(self.Rankine.state2.h))
        self.le_H3.setText("{:.2f}".format(self.Rankine.state3.h))
        self.le_H4.setText("{:.2f}".format(self.Rankine.state4.h))
        self.le_HeatAdded.setText("{:.2f}".format(self.Rankine.heat_added))
        self.le_PumpWork.setText("{:.2f}".format(self.Rankine.pump_work))
        self.le_Efficiency.setText("{:.2f}".format(self.Rankine.efficiency))
        self.le_TurbineWork.setText("{:.2f}".format(self.Rankine.turbine_work))


        self.lbl_SatPropHigh.setText(
            "PSat = {:.2f} bar, TSat= {:.2f} C\nhf = {:.2f} kJ/kg , hg = {:.2f} kJ/kg\nsf= {:.2f} kJ/kgK, "
            "sg= {:.2f} kJ/kgK\nvf= {:.4f} m^3/kg, vg= {:.2f} m^3/kg ".format(self.Rankine.p_high/100,
                                                                              self.Rankine.state1.T,
                                                                              self.Rankine.state1.hf,
                                                                              self.Rankine.state1.hg,
                                                                              self.Rankine.state1.sf,
                                                                              self.Rankine.state1.sg,
                                                                              self.Rankine.state1.vf,
                                                                              self.Rankine.state1.vg))
        self.lbl_SatPropLow.setText(
            "PSat={:.2f} bar, TSat = {:.2f} C\nhf = {:.2f} kJ / kg, hg = {:.2f} kJ / kg\nsf = {:.2f} kJ / kgK, "
            "sg = {:.2f} kJ / kgK\nvf = {:.4f} m ^ 3 / kg, vg = {:.2f} m ^ 3 / kg ".format(self.Rankine.p_low/100,
                                                                                           self.Rankine.state2.T,
                                                                                           self.Rankine.state2.hf,
                                                                                           self.Rankine.state2.hg,
                                                                                           self.Rankine.state2.sf,
                                                                                           self.Rankine.state2.sg,
                                                                                           self.Rankine.state2.vf,
                                                                                           self.Rankine.state2.vg))


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
