from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QFileDialog
import sys
import os
from utils import *
from apis_call import login, getAndharBaharLastStatus, getAndharBaharDrawnoResult
import threading

class SignalHandler(QObject):
    result_ready = pyqtSignal(int, int, int)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # Create signal handler
        self.signal_handler = SignalHandler()
        self.signal_handler.result_ready.connect(self._updateUIWithResult)
        self.selected_folder = None

        self.MainWindow = MainWindow  # Store MainWindow reference
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(629, 542)
        MainWindow.setFixedSize(629, 542)
        
        # Try to login first
        self.encrypted_login_key = "NyRjXA7gqwMwXIZZFaOIUXEcGYotxtm9TOQXyvNdZudoRMpZ1kG2aQwQ5c4Q2BiYXNWvPJ7FPdBJ7Ou0e4ZK151hJtHl/050HdaMuQBoNLw="
        self.member_id = "GK00512276"
        self.andhar_bahar_version = "R1.0.0.1"
        self.timerVal = 0
        self.session_id = login(self.encrypted_login_key)
        self.drawId = ""
        
        if not self.session_id:
            # Show error dialog and close application
            msg = QtWidgets.QMessageBox()
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Login Failed")
            msg.setInformativeText("Unable to connect to the server or invalid credentials.")
            msg.setWindowTitle("Error")
            msg.exec_()
            MainWindow.close()
            return
        
        
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        # Add folder picker button
        self.folderPickerButton = QtWidgets.QPushButton(self.centralwidget)
        self.folderPickerButton.setGeometry(QtCore.QRect(240, 180, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.folderPickerButton.setFont(font)
        self.folderPickerButton.setObjectName("folderPickerButton")
        self.folderPickerButton.setText("Select Folder")
        self.folderPickerButton.clicked.connect(self.selectFolder)
        
        # Add folder path label
        self.folderPathLabel = QtWidgets.QLabel(self.centralwidget)
        self.folderPathLabel.setGeometry(QtCore.QRect(100, 240, 429, 30))
        self.folderPathLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.folderPathLabel.setText("Please select a folder to store results")
        
        # Create start button (initially disabled)
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setGeometry(QtCore.QRect(240, 280, 150, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.startButton.setObjectName("startButton")
        self.startButton.setText("Start Fetching")
        self.startButton.clicked.connect(self.showMainUI)
        self.startButton.setEnabled(False)  # Initially disabled
        
        # Create container widget for main UI (initially hidden)
        self.mainContainer = QtWidgets.QWidget(self.centralwidget)
        self.mainContainer.setGeometry(QtCore.QRect(0, 0, 629, 542))
        self.mainContainer.hide()
        
        # Move all existing UI elements to mainContainer
        self.label = QtWidgets.QLabel(self.mainContainer)
        self.label.setGeometry(QtCore.QRect(140, 40, 361, 51))
        font = QtGui.QFont()
        font.setFamily("Tibetan Machine Uni")
        font.setPointSize(18)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.resultDataField = QtWidgets.QTextEdit(self.mainContainer)
        self.resultDataField.setGeometry(QtCore.QRect(60, 140, 501, 341))
        self.resultDataField.setReadOnly(True)
        self.resultDataField.setObjectName("resultDataField")

        self.layoutWidget = QtWidgets.QWidget(self.mainContainer)
        self.layoutWidget.setGeometry(QtCore.QRect(240, 90, 117, 33))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(10, 5, 10, 5)
        self.horizontalLayout.setSpacing(23)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.TimeLabel = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Rasa")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TimeLabel.setFont(font)
        self.TimeLabel.setObjectName("TimeLabel")
        self.horizontalLayout.addWidget(self.TimeLabel)
        self.TimerLabelVal = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("P052 [UKWN]")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.TimerLabelVal.setFont(font)
        self.TimerLabelVal.setObjectName("TimerLabelVal")
        self.horizontalLayout.addWidget(self.TimerLabelVal)
        self.label_3 = QtWidgets.QLabel(self.mainContainer)
        self.label_3.setGeometry(QtCore.QRect(290, 490, 261, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def showMainUI(self):
        # Hide start button and show main UI
        self.timerVal, self.drawId = getAndharBaharLastStatus(f"{self.member_id},{self.session_id},{self.andhar_bahar_version}")
        self.TimerLabelVal.setText(str(self.timerVal))
        self.startButton.hide()
        self.mainContainer.show()
        self.updateTimer()

    def updateTimer(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self._updateCountdown)
        self.timer.start(1000) 

    def _updateCountdown(self):
        # Ensure timerVal is an int and not None
        if not isinstance(self.timerVal, int):
            self.timerVal = 45  # reset to default if invalid

        self.timerVal -= 1
        self.TimerLabelVal.setText(str(self.timerVal))

        if self.timerVal <= 0:
            self.timerVal = 45
            self.TimerLabelVal.setText(str(self.timerVal))

            # Start background thread to fetch data without blocking UI
            threading.Thread(target=self.fetchAndUpdateResult, daemon=True).start()
        

    def fetchAndUpdateResult(self):
        self.label_3.setText("Fetching New Value...")
        result, rem_time, drawId = getAndharBaharDrawnoResult(self.drawId)
        # Emit signal through signal handler
        self.signal_handler.result_ready.emit(result, drawId, rem_time)

    def selectFolder(self):
        folder = QFileDialog.getExistingDirectory(
            self.MainWindow,
            "Select Folder for Results",
            "",
            QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks
        )
        if folder:
            self.selected_folder = folder
            # Show truncated path if too long
            display_path = folder
            if len(folder) > 40:
                display_path = "..." + folder[-37:]
            self.folderPathLabel.setText(display_path)
            self.startButton.setEnabled(True)

    def _updateUIWithResult(self, result, drawId, rem_time):
        try:
            print("Updating data...")
            self.drawId = drawId
            self.result = result
            self.timerVal = rem_time if rem_time!=0 else 45
            
            # Update status label
            self.label_3.setText("Saving...")
            
            # Save to file in selected folder
            try:
                with open(os.path.join(self.selected_folder, "results.txt"), "a") as f:
                    if f.tell() == 0:  # If file is empty
                        f.write(str(result))
                    else:
                        f.write(f", {str(result)}")
            except Exception as e:
                print(f"Error saving to file: {str(e)}")
            
            # Get text cursor and move to end
            cursor = self.resultDataField.textCursor()
            cursor.movePosition(QtGui.QTextCursor.End)
            
            # Add comma separator if not first entry
            if self.resultDataField.toPlainText():
                cursor.insertText(", ")
                
            # Insert new result
            cursor.insertText(str(result))
            
            # Update display and scroll to bottom
            self.resultDataField.setTextCursor(cursor)
            self.resultDataField.ensureCursorVisible()
            
            # Restore status after 1 second
            QtCore.QTimer.singleShot(1000, lambda: self.label_3.setText("Waiting For New Value"))
            
        except Exception as e:
            print(f"UI update error: {e}")
            self.label_3.setText("Update Failed")
            # Attempt recovery after 2 seconds
            QtCore.QTimer.singleShot(2000, lambda: self.label_3.setText("Fetching New Value"))


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "funAB"))
        self.label.setText(_translate("MainWindow", "Andar Bahar Data Receiver"))
        self.TimeLabel.setText(_translate("MainWindow", "Timer"))
        self.TimerLabelVal.setText(_translate("MainWindow", str(self.timerVal)))
        self.label_3.setText(_translate("MainWindow", "Waiting For New Value"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())