# Filename: motion_detector_editor.py

"""The main purpose of this program is to take Tesla Sentinal Clips and Edit them down to a highlights reel"""

import sys
import os
import cv2, time
import glob

# Import QApplication and the required widgets from PySide2.QtWidgets

from PySide2 import QtWidgets
from PySide2 import QtCore

from PySide2.QtCore import Qt
from PySide2.QtCore import QTimer
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QMainWindow
from PySide2.QtWidgets import QWidget
from PySide2.QtWidgets import QGridLayout
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QPushButton
from PySide2.QtWidgets import QHBoxLayout
from PySide2.QtWidgets import QVBoxLayout
from PySide2.QtWidgets import QComboBox
from PySide2.QtWidgets import QGroupBox
from PySide2.QtWidgets import QFrame
from PySide2.QtWidgets import QLabel
from PySide2.QtWidgets import QDialog
from PySide2.QtWidgets import QDialogButtonBox
from PySide2.QtWidgets import QFormLayout
from PySide2.QtWidgets import QLineEdit
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QProgressBar
from PySide2.QtWidgets import QMessageBox


from style import styles




class ProgramUI(QtWidgets.QDialog):
    """Generic (GUI)."""
    def __init__(self, parent=None):
        super(ProgramUI, self).__init__(parent)

        # loads an exteranl styesheet as python
        newstyle = styles()
        self.setStyleSheet(newstyle.dark_orange)

        self.setWindowTitle("Program Name")
        self.setFixedSize(375, 250)
        # create the main layout
        self.main_layout = QVBoxLayout()
       
        # create the top layout and add it
        self.createtoplayout()
        self.main_layout.addWidget(self.topGroupBox)
        # create the save botton and add it
        self.save_location_button = QtWidgets.QPushButton("Save Location")
        self.save_location_button.setAutoDefault(False)
        self.main_layout.addWidget(self.save_location_button)
        # create the bottom layout and add it
        self.createbottomlayout()
        self.main_layout.addLayout(self.proggresslayout)
       
       # resize window to match the width of what has been added
        self.setLayout(self.main_layout)
        layout_size = self.main_layout.sizeHint()
        self.setFixedSize(self.width(),layout_size.height())
    
    

    def createtoplayout(self):
        self.topGroupBox = QGroupBox("")
        self.open_location_button = QtWidgets.QPushButton("Full Path Location")
        self.open_location_button.setAutoDefault(False)
        
        self.textboxlabel = QLabel("Wildcard")
        self.textboxlabel.setMinimumWidth(100)
        self.lineEdit = QLineEdit("")
        
        text_box_layout = QHBoxLayout()
        text_box_layout.addWidget(self.textboxlabel)
        text_box_layout.addWidget(self.lineEdit )
        
        self.infoboxlabel = QLabel("Number of Videos to Process")
        self.infoboxlabel.setMinimumWidth(100)
        self.numberbox = QLabel("0")
        self.numberbox.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken )
        self.numberbox.setStyleSheet("""
            QWidget {  
                    padding: 1px;
                    border-style: solid;
                    border: 1px solid #1e1e1e;
                    border-radius: 5;
                    min-height: 15px;
                    font-size: 12px;
                }
            """)
         
        info_box_layout = QHBoxLayout()
        info_box_layout.addWidget(self.infoboxlabel)
        info_box_layout.addWidget(self.numberbox)

        layout = QVBoxLayout()
        layout.addWidget(self.open_location_button)
        layout.addLayout(text_box_layout)
        layout.addLayout(info_box_layout)
        layout.addStretch(1)
        self.topGroupBox.setLayout(layout)  
    
    def advanceProgressBar(self, percentage_complete):
        if percentage_complete < self.progressBar.maximum():
            self.progressBar.setValue(percentage_complete)
        else:
            self.progressBar.setValue(self.progressBar.maximum())
        
    def createbottomlayout(self):  
        self.proggresslayout = QHBoxLayout()  
        self.runprogram_button = QtWidgets.QPushButton("Run the Program")
        self.runprogram_button.setAutoDefault(False)
        #self.runprogram_button.setDisabled(True)
        
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 100)
        self.progressBar.setValue(0)
        self.timer = QTimer(self)
        

        self.proggresslayout.addWidget(self.runprogram_button)
        self.proggresslayout.addWidget(self.progressBar)
   
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
  

    def _getfolder(self, message, button_name):
        dialog = QFileDialog()
        #basefoldername = dialog.getExistingDirectory()
        basefoldername = dialog.getExistingDirectory(caption=message,options = QFileDialog.DontUseNativeDialog)
        button_name.setText(message + basefoldername)
        common_prefix = basefoldername
        self._model.setfolder(basefoldername)
        if basefoldername != "":
            self._model._getvideolist()
            self._wildcardchange()
            
       

    def _getsavefilename(self, message, button_name):
        dialog = QFileDialog()
        save_file_name = dialog.getSaveFileName(filter="*.avi")
        button_name.setText(message + save_file_name[0])
        self._model.setsavefilename(save_file_name[0])



    def _runtheprogram(self):

        if self._model.oktoruncheck(self._view.showdialog):            
            self._model.theprogram()  
    
    def _wildcardchange(self):
        self._model._sortvideolist(self._view.lineEdit.text())
        self._view.numberbox.setText(str(len(self._model.wildcard_video_list)))
        self._view.runprogram_button.setFocus()
        # my_text_cursor = self._view.lineEdit.cursor()
        # my_text_cursor = my_text_edit.textCursor()
        

    def _connectSignals(self):
        """Connect signals and slots."""
        self.fullpath = self._view.open_location_button.clicked.connect(lambda: self._getfolder("Full Path Location: ", self._view.open_location_button))
        self.relativepath = self._view.save_location_button.clicked.connect(lambda: self._getsavefilename("Relative Path Location: ", self._view.save_location_button))
        self._view.runprogram_button.clicked.connect(lambda: self._runtheprogram())
        self._view.lineEdit.editingFinished.connect(self._wildcardchange)
        self._view.lineEdit.returnPressed.connect(self._wildcardchange)
        self._view.timer.timeout.connect(lambda: self._view.advanceProgressBar(self._model.progress))
        self._view.timer.start(1000)
class ProgramModel:
    
    
    def __init__(self):
        """Model initializer."""
        self.folderlocation = ""
        self.savefilelocation = ""
        #self.path = "C:\\test\\motion"
        self.fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
        #self.out = cv2.VideoWriter((self.path + "out_test.avi"), self.fourcc, 24,(1280,960))
        self.video_list = []
        self.progress = 0 

    def setfolder(self, folderlocation):
        self.folderlocation = folderlocation
       

    def setsavefilename(self, savefilelocation):
        self.savefilelocation = savefilelocation
        
        
    def oktoruncheck(self, popup):
        if self.folderlocation == "" or self.savefilelocation == "":
            if self.folderlocation == "" and self.savefilelocation == "":
                popup("Please select a Folder and a Save File")
            elif self.folderlocation == "":
                popup("Please select a Folder")
            elif self.savefilelocation == "":
                popup("Please select a File to save to")
            return False
        return True

    def _capture_motion(self, video_file):
        self.out = cv2.VideoWriter((self.savefilelocation), self.fourcc, 24,(1280,960))
        self.video=cv2.VideoCapture(video_file)
        self._check = True
        self._first_frame = None
        while self._check:
            self._check, frame = self.video.read()
            
        
            self._status=0
            if self._check:
            
                gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                gray=cv2.GaussianBlur(gray,(21,21),0)
                if self._first_frame is None:
                    self._first_frame = gray
                    continue

                delta_frame=cv2.absdiff(self._first_frame,gray)
                thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
                thresh_frame= cv2.dilate(thresh_frame, None, iterations=2)

                (cnts,_)=cv2.findContours(thresh_frame.copy(),cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                for contour in cnts:
                    if cv2.contourArea(contour) < 1000:
                        continue
                    self._status = 1
                    # (x,y,w,h)=cv2.boundingRect(contour)
                    # cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 3)

                #cv2.imshow("Capturing", gray)
               # cv2.imshow("Delta Frame",delta_frame)
               # cv2.imshow("Threshold Frame",thresh_frame)
                cv2.imshow("Color Frame",frame)
                if self._status == 1:
                    self.out.write(frame)
                
                

            key = cv2.waitKey(1)
            if key ==ord('q'):
                break

    def _trim_videos(self, video_list):
        progress_amount = int(100/(len(video_list)+1))+1
        for video_file in video_list:
            self.progress = self.progress + progress_amount
            self._capture_motion(video_file)  

    def _close_video_tools(self):  
        self.progress =100
        self.out.release()
        self.video.release()
        cv2.destroyAllWindows()

    def run_the_edit(self,video_file_list):
        self._trim_videos(video_file_list)
        self._close_video_tools()
    
    def _getvideolist(self):
        videos = []
        types = ("**\**\*.mp4", "**\**\*.mp3") # the tuple of file types
        
        # grab all the files in selected directory recursively
        for files in types:
            videos.extend(glob.glob(self.folderlocation + files, recursive=True))
        self.video_list = videos
       
        #return(videos)   
        #video_file_list=["test_videos\\front.mp4", "test_videos\\front2.mp4"]

    def _sortvideolist(self, wildcard):
        newvideos = [i for i in self.video_list if wildcard in i] 
        self.wildcard_video_list = newvideos
        
      


    def theprogram(self):   
        self.progress = 0 
        self.run_the_edit(self.wildcard_video_list)

    
    


def main():
    """Main function"""
    #Create and instance of QApplication
    pyqt_interface = QApplication(sys.argv)
    # Show the Programs's GUI
    view = ProgramUI()
    view.show()
    model = ProgramModel()
    ProgramCtrl(view=view, model=model)
    # Execute the Programs's main loop
    sys.exit(pyqt_interface.exec_())

if __name__ == '__main__':
   
    main()