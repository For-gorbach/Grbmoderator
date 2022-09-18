# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GRBmoderator.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1292, 1076)
        MainWindow.setMinimumSize(QtCore.QSize(1292, 1076))
        MainWindow.setMaximumSize(QtCore.QSize(1292, 1076))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QtCore.QSize(1292, 1076))
        self.centralwidget.setMaximumSize(QtCore.QSize(1292, 1076))
        self.centralwidget.setStyleSheet("background-color: #303030;")
        self.centralwidget.setObjectName("centralwidget")
        self.chat_id = QtWidgets.QLineEdit(self.centralwidget)
        self.chat_id.setGeometry(QtCore.QRect(5, 140, 1282, 70))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.chat_id.setFont(font)
        self.chat_id.setTabletTracking(True)
        self.chat_id.setStyleSheet("color: #fff;\n"
"border: 2px solid #e7e7e7;\n"
"border-radius: 10px;")
        self.chat_id.setText("")
        self.chat_id.setObjectName("chat_id")
        self.token = QtWidgets.QLineEdit(self.centralwidget)
        self.token.setGeometry(QtCore.QRect(5, 213, 1282, 70))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.token.setFont(font)
        self.token.setTabletTracking(True)
        self.token.setStyleSheet("color: #fff;\n"
"border: 2px solid #e7e7e7;\n"
"border-radius: 10px;")
        self.token.setText("")
        self.token.setObjectName("token")
        self.savedata = QtWidgets.QPushButton(self.centralwidget)
        self.savedata.setGeometry(QtCore.QRect(866, 780, 421, 121))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.savedata.setFont(font)
        self.savedata.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.savedata.setAutoFillBackground(False)
        self.savedata.setStyleSheet("color: #51ff00;\n"
"border: 2px solid #30bb00;\n"
"border-radius: 10px;")
        self.savedata.setObjectName("savedata")
        self.deletedata = QtWidgets.QPushButton(self.centralwidget)
        self.deletedata.setGeometry(QtCore.QRect(5, 780, 411, 121))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.deletedata.setFont(font)
        self.deletedata.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.deletedata.setAutoFillBackground(False)
        self.deletedata.setStyleSheet("color: #ff0000;\n"
"border: 2px solid #aa0000;\n"
"border-radius: 10px;")
        self.deletedata.setObjectName("deletedata")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(5, 910, 1281, 161))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(100)
        font.setBold(True)
        font.setWeight(75)
        self.start.setFont(font)
        self.start.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start.setAutoFillBackground(False)
        self.start.setStyleSheet("color: #0000ff;\n"
"border: 2px solid #0000aa;\n"
"border-radius: 10px;")
        self.start.setCheckable(False)
        self.start.setObjectName("start")
        self.rules = QtWidgets.QTextEdit(self.centralwidget)
        self.rules.setGeometry(QtCore.QRect(5, 286, 636, 491))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.rules.setFont(font)
        self.rules.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.rules.setMouseTracking(True)
        self.rules.setTabletTracking(True)
        self.rules.setStyleSheet("color: #fff;\n"
"border: 2px solid #e7e7e7;\n"
"border-radius: 10px;")
        self.rules.setDocumentTitle("")
        self.rules.setObjectName("rules")
        self.hello = QtWidgets.QTextEdit(self.centralwidget)
        self.hello.setGeometry(QtCore.QRect(651, 288, 636, 491))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.hello.setFont(font)
        self.hello.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.hello.setMouseTracking(True)
        self.hello.setTabletTracking(True)
        self.hello.setStyleSheet("color: #fff;\n"
"border: 2px solid #e7e7e7;\n"
"border-radius: 10px;")
        self.hello.setDocumentTitle("")
        self.hello.setObjectName("hello")
        self.doban = QtWidgets.QCheckBox(self.centralwidget)
        self.doban.setGeometry(QtCore.QRect(5, 10, 1010, 40))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.doban.setFont(font)
        self.doban.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.doban.setStyleSheet("color: #fff;")
        self.doban.setObjectName("doban")
        self.load = QtWidgets.QPushButton(self.centralwidget)
        self.load.setGeometry(QtCore.QRect(435, 780, 411, 121))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.load.setFont(font)
        self.load.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.load.setAutoFillBackground(False)
        self.load.setStyleSheet("color: #ffff00;\n"
"border: 2px solid #cccc00;\n"
"border-radius: 10px;")
        self.load.setObjectName("load")
        self.time = QtWidgets.QSpinBox(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(900, 58, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.time.setFont(font)
        self.time.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.time.setStyleSheet("color: #fff;")
        self.time.setSpecialValueText("")
        self.time.setSuffix("")
        self.time.setPrefix("")
        self.time.setMinimum(0)
        self.time.setMaximum(3600)
        self.time.setProperty("value", 0)
        self.time.setDisplayIntegerBase(10)
        self.time.setObjectName("time")
        self.timetext = QtWidgets.QLabel(self.centralwidget)
        self.timetext.setEnabled(True)
        self.timetext.setGeometry(QtCore.QRect(5, 58, 890, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.timetext.setFont(font)
        self.timetext.setStyleSheet("color: #fff;")
        self.timetext.setLineWidth(5)
        self.timetext.setTextFormat(QtCore.Qt.AutoText)
        self.timetext.setScaledContents(False)
        self.timetext.setObjectName("timetext")
        self.nums2bantext = QtWidgets.QLabel(self.centralwidget)
        self.nums2bantext.setEnabled(True)
        self.nums2bantext.setGeometry(QtCore.QRect(5, 100, 450, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.nums2bantext.setFont(font)
        self.nums2bantext.setStyleSheet("color: #fff;")
        self.nums2bantext.setLineWidth(5)
        self.nums2bantext.setTextFormat(QtCore.Qt.AutoText)
        self.nums2bantext.setScaledContents(False)
        self.nums2bantext.setObjectName("nums2bantext")
        self.nums2ban = QtWidgets.QSpinBox(self.centralwidget)
        self.nums2ban.setGeometry(QtCore.QRect(460, 100, 71, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.nums2ban.setFont(font)
        self.nums2ban.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.nums2ban.setStyleSheet("color: #fff;")
        self.nums2ban.setSpecialValueText("")
        self.nums2ban.setSuffix("")
        self.nums2ban.setPrefix("")
        self.nums2ban.setMinimum(0)
        self.nums2ban.setMaximum(100)
        self.nums2ban.setProperty("value", 0)
        self.nums2ban.setDisplayIntegerBase(10)
        self.nums2ban.setObjectName("nums2ban")
        self.topnum = QtWidgets.QSpinBox(self.centralwidget)
        self.topnum.setGeometry(QtCore.QRect(900, 100, 51, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.topnum.setFont(font)
        self.topnum.setCursor(QtGui.QCursor(QtCore.Qt.SizeVerCursor))
        self.topnum.setStyleSheet("color: #fff;")
        self.topnum.setSpecialValueText("")
        self.topnum.setSuffix("")
        self.topnum.setPrefix("")
        self.topnum.setMinimum(0)
        self.topnum.setMaximum(10)
        self.topnum.setProperty("value", 0)
        self.topnum.setDisplayIntegerBase(10)
        self.topnum.setObjectName("topnum")
        self.topnumtext = QtWidgets.QLabel(self.centralwidget)
        self.topnumtext.setEnabled(True)
        self.topnumtext.setGeometry(QtCore.QRect(605, 100, 290, 30))
        font = QtGui.QFont()
        font.setFamily("Consolas")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.topnumtext.setFont(font)
        self.topnumtext.setStyleSheet("color: #fff;")
        self.topnumtext.setLineWidth(5)
        self.topnumtext.setTextFormat(QtCore.Qt.AutoText)
        self.topnumtext.setScaledContents(False)
        self.topnumtext.setObjectName("topnumtext")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.chat_id.setPlaceholderText(_translate("MainWindow", "Введите id чата"))
        self.token.setPlaceholderText(_translate("MainWindow", "Введите токен бота"))
        self.savedata.setText(_translate("MainWindow", "Сохранить данные в файл"))
        self.deletedata.setText(_translate("MainWindow", "Удалить данные из файла"))
        self.start.setText(_translate("MainWindow", "Запуск бота"))
        self.rules.setPlaceholderText(_translate("MainWindow", "Введите правила"))
        self.hello.setPlaceholderText(_translate("MainWindow", "Введите приветствие"))
        self.doban.setText(_translate("MainWindow", "Включить автобан некоторых слов и стикеров (бета, могут быть баги)"))
        self.load.setText(_translate("MainWindow", "Загрузить данные из файла"))
        self.timetext.setText(_translate("MainWindow", "Сколько СЕКУНД нужно подождать после репорта для следующего"))
        self.nums2bantext.setText(_translate("MainWindow", "Сколько предупреждений до бана"))
        self.topnumtext.setText(_translate("MainWindow", "Сколько мест в топе"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())