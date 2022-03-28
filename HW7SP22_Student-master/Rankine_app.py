import sys
from PyQt5.QtWidgets import QWidget, QApplication
from PyQt5 import QtGui
from Rankine_GUI import Ui_Form  # from the GUI file you created
import rankineFile as rankineFile
#some code borrowed from Calc_state_app_stem.py
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
        Part 1: Here, we need to set the properties of the rankine object and calculate: the
        enthalpies of each state,heat added,pump work, and overall cycle efficiency.
        Finally, output the results to the line edit widgets.
        Part 2: Fill in the Saturated Properties labels accordingly. Necessary adjustments made to Steam_work and Dr. Smay's Rankine file
        (renamed: rankineFile and modified).
        :return:
        """

        self.Rankine.p_high = float(self.le_PHigh.text())*100 #these lines assign vals to rankine params
        self.Rankine.p_low = float(self.le_PLow.text())*100 #bar to kPa
        self.Rankine.eff_turbine = float(self.le_TurbineEff.text())
        self.Rankine.quality = float(self.le_TurbineInletCondition.text()) if self.rdo_Quality.isChecked() else None
        self.Rankine.t_high = float(self.le_TurbineInletCondition.text()) if self.rdo_THigh.isChecked() else None #doesn't work but it was a nice thought
        self.Rankine.calc_efficiency() #necessary to get access to the states in the lines below


        self.le_H1.setText("{:.2f}".format(self.Rankine.state1.h)) #fills in the unchangeable line edits at bottom according to calculations made from above inputs
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
                                                                              self.Rankine.state1.vg))   #Bryce made adjustments to rankine and steam files for these labels to work
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

    def ExitApp(self): #allows app to be exited
        app.exit()

if __name__ == "__main__":
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    app.aboutToQuit.connect(app.deleteLater)
    main_win = main_window()
    sys.exit(app.exec_())
