# Filename: pyqt_interface.py

"""Here is a starter interface for python programs"""

import sys
import os

# Import QApplication and the required widgets from PySide2.QtWidgets

from PySide2 import QtWidgets
from PySide2 import QtCore

from PySide2.QtCore import Qt
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QComboBox
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QFormLayout
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QFileDialog
from style import styles




fullpathfolder = "../textures/" 
relativepathfolder = "C:/MDL/fake"

class ProgramUI(QtWidgets.QDialog):
    """Generic (GUI)."""
    def __init__(self, parent=None):
        super(ProgramUI, self).__init__(parent)

        newstyle = styles()
        self.setStyleSheet(newstyle.dark_orange)

        self.setWindowTitle("Program Name")
        self.setFixedSize(300, 150)
        self.main_layout = QGridLayout()
         # This is the material selector
        self.pulldown_options = {"Option One":"option_one", "Option Two":"option_two"}
        self.pulldown_combobox = QComboBox()
        self.pulldown_combobox.addItems(self.pulldown_options.keys())
       
        self.pulldown_label = QLabel("&Options to choose from:")
        self.pulldown_label.setBuddy(self.pulldown_combobox)

        topLayout = QHBoxLayout()
        topLayout.addWidget(self.pulldown_label)
        topLayout.addWidget(self.pulldown_combobox)
        topLayout.addStretch(1)
        # This is adding that pulldown_options layout to the top of the layout grid
        self.main_layout.addLayout(topLayout, 0, 0, 1, 3)


        self.mdl_save_location_button = QtWidgets.QPushButton("Full Path Location")
        self.main_layout.addWidget(self.mdl_save_location_button, 2, 0, 1, 3)

           #relative texture path
        self.texture_location_button = QtWidgets.QPushButton("Relative Path Location")
        self.texture_location_button.setDisabled(True)
        
        self.main_layout.addWidget(self.texture_location_button, 3, 0, 1, 3)

        self.runprogram_button  = QtWidgets.QPushButton("Run the Program")
        self.runprogram_button.setDisabled(True)
        self.main_layout.addWidget(self.runprogram_button, 4, 1, 1, 1)
        self.setLayout(self.main_layout)

    def showdialog(self, message, title = "Error", details = "An error has occured"):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)

        self.msg.setText(message)
        #self.msg.setInformativeText("This is additional information")
        self.msg.setWindowTitle(title)
        self.msg.setDetailedText(details)
        self.msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        #self.msg.buttonClicked.connect(msgbtn)

        retval = self.msg.exec_()

# Create a Controller class to connect the GUI and the model
class ProgramCtrl:
    """Program Controller class."""
    def __init__(self, view, model):
        """Controller initializer."""
        self._model = model
        self._view = view
        # Connect signals and slots
        self._connectSignals()
        # this needs to change
  

    def _getfile(self, message, button_name):
        dialog = QFileDialog()
        self.basefoldername = dialog.getExistingDirectory()
        button_name.setText(message + self.basefoldername)
        common_prefix = self.basefoldername
        self._view.texture_location_button.setDisabled(False)
        self._model.setfullpath(self.basefoldername)
       

    def _getrelativefile(self, message, button_name):
        dialog = QFileDialog()
        fname = dialog.getExistingDirectory()
        common_prefix = self.basefoldername
        relative_path = os.path.relpath(fname, common_prefix)
        button_name.setText(message + relative_path)
        self._view.runprogram_button.setDisabled(False)
        self._model.setrelativepath(relative_path)

    def _runtheprogram(self, info):
        self._model.theprogram(info)
        

    def _connectSignals(self):
        """Connect signals and slots."""
        self.fullpath = self._view.mdl_save_location_button.clicked.connect(lambda: self._getfile("Full Path Location: ", self._view.mdl_save_location_button))
        self.relativepath = self._view.texture_location_button.clicked.connect(lambda: self._getrelativefile("Relative Path Location: ", self._view.texture_location_button))
        self._view.runprogram_button.clicked.connect(lambda: self._runtheprogram("I'm doing it "))
class ProgramModel:
    
    
    def __init__(self, fullpathfolder, relativepathfolder):
        """Model initializer."""
       
        self.fullpathfolder = fullpathfolder
        self.relativepathfolder = relativepathfolder
    
    def setfullpath(self, fullpath):
        self.relativepathfolder = fullpath
        print(self.relativepathfolder) 

    def setrelativepath(self, relativepath):
        relativepath = relativepath.replace("\\","/")
        self.fullpathfolder = relativepath + "/"
        print(self.fullpathfolder)
    
    def theprogram(self, info):
        """this is where the program logic is at"""
        print("this is the program " + str(info))
    
    


def main():
    """Main function"""
    #Create and instance of QApplication
    pyqt_interface = QApplication(sys.argv)
    # Show the Programs's GUI
    view = ProgramUI()
    view.show()
    model = ProgramModel(fullpathfolder=fullpathfolder,relativepathfolder=relativepathfolder)
    ProgramCtrl(view=view, model=model)
    # Execute the Programs's main loop
    sys.exit(pyqt_interface.exec_())

if __name__ == '__main__':
   
    main()