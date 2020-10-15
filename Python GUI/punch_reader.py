from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import matplotlib.pyplot as plt
import win32api
import win32con
import win32file
import sys


hit_numbers = []
hits_val = []
hits_types = []

def get_removable_drives():
    drives = [i for i in win32api.GetLogicalDriveStrings().split('\x00') if i]
    rdrives = [d for d in drives if win32file.GetDriveType(d) == win32con.DRIVE_REMOVABLE]
    return rdrives

def show_plot(hits_numbers,hits_types,hits_val):
    l_hits=[]
    r_hits=[]
    u_hits=[]

    for i in range(len(hit_numbers)):
        if (hits_types[i] == 'l'):
            l_hits.append(hits_val[i])
        else:
            l_hits.append(0)

        if (hits_types[i] == 'r'):
            r_hits.append(hits_val[i])
        else:
            r_hits.append(0)

        if (hits_types[i] == 'u'):
            u_hits.append(hits_val[i])
        else:
            u_hits.append(0)

    plt.bar(hits_numbers, l_hits, label="Left Hits",color = 'g')
    plt.bar(hits_numbers, r_hits, label="Right Hits", color='b')
    plt.bar(hits_numbers, u_hits, label="Upper Hits", color='r')
    #plt.bar([2, 4, 6, 8, 10], [8, 6, 2, 5, 6], label="Example two", color='g')
    plt.legend()
    plt.xlabel('Hits count')
    plt.ylabel('Force')

    plt.title('Hits log')

    plt.show()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setWindowIcon(QIcon('punch_icon.ico'))
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(416, 206)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 231, 121))
        self.groupBox.setObjectName("groupBox")
        self.avail_drives = QtWidgets.QComboBox(self.groupBox)
        self.avail_drives.setGeometry(QtCore.QRect(10, 30, 201, 22))
        self.avail_drives.setObjectName("avail_drives")
        self.refresh_button = QtWidgets.QPushButton(self.groupBox)
        self.refresh_button.setGeometry(QtCore.QRect(10, 70, 93, 28))
        self.refresh_button.setObjectName("refresh_button")
        self.show_results_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_results_button.setGeometry(QtCore.QRect(250, 40, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.show_results_button.setFont(font)
        self.show_results_button.setObjectName("show_results_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 416, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)


        self.refresh_list()
        self.refresh_button.clicked.connect(self.refresh_list)
        self.show_results_button.clicked.connect(self.show_results)
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hits Reader"))
        self.groupBox.setTitle(_translate("MainWindow", "SD-Card drive:"))
        self.avail_drives.setPlaceholderText(_translate("MainWindow", "None"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.show_results_button.setText(_translate("MainWindow", "Show Results"))

    def refresh_list(self):
        items = get_removable_drives()
        self.avail_drives.addItems(items)

    def show_results(self):
        global hit_numbers,hits_types,hits_val

        file = self.avail_drives.currentText()
        if(file!=None):
            file+="data.txt"
            file = open(file,'r')
            lines = file.readlines()
            for i in range(len(lines)):
                line = lines[i].strip()
                line = line.split(",")
                hit_numbers.append(i+1)
                hits_val.append(int(line[0]))
                hits_types.append(line[1])

        show_plot(hit_numbers,hits_types,hits_val)

def my_excepthook(type, value, tback):
    # log the exception here

    # then call the default handler
    sys.__excepthook__(type, value, tback)


if __name__ == "__main__":


    sys.excepthook = my_excepthook
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
