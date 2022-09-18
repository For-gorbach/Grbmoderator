import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon
from GRBmoderatorUI import Ui_MainWindow
import json
import plyer


def printm(msg):
    print(msg)
    plyer.notification.notify(message=msg, app_name='GRBmoderator', app_icon='icon.ico', title='GRBmoderator', timeout=2, toast=True)


try:
    class MainWindow(QtWidgets.QMainWindow):
        def __init__(self):
            super(MainWindow, self).__init__()
            self.ui = Ui_MainWindow()
            self.ui.setupUi(self)
            self.init_UI()

        def init_UI(self):
            self.setWindowTitle("GRBmoderator bot")
            self.setWindowIcon(QIcon("icon.ico"))
            self.ui.start.clicked.connect(self.start)
            self.ui.deletedata.clicked.connect(self.deletedata)
            self.ui.savedata.clicked.connect(self.savedata)
            self.ui.load.clicked.connect(self.load)

        def start(self):
            chat_id = self.ui.chat_id.text().strip()
            token = self.ui.token.text().strip()
            rules = self.ui.rules.toPlainText().strip()
            hello = self.ui.hello.toPlainText().strip()
            doban = self.ui.doban.isChecked()
            time = self.ui.time.value()
            nums2ban = self.ui.nums2ban.value()
            topnum = self.ui.topnum.value()

            if chat_id == "":
                printm("Вы не указали id чата!")
            elif token == "":
                printm("Вы не указали токен бота!")
            else:
                printm("Бот запущен!\n(При запуске окно перестанет 'отвечать', это связанно с особенностями языка).")
                from main import main
                main(token, chat_id, rules, hello, doban, time, nums2ban, topnum)

        def deletedata(self):
            with open("quisettings.txt", "w") as f:
                f.write("{'chat_id': '', 'token': '', 'rules': '', 'hello': '', 'doban': 'False'}")
                printm("Данные из файла удалены...")

        def savedata(self):
            with open("quisettings.txt", "w", encoding="utf-8") as f:
                f.write(
                    f"{{'chat_id': '{self.ui.chat_id.text().strip()}', "
                    f"'token': '{self.ui.token.text().strip()}', "
                    f"'rules': '{self.ui.rules.toPlainText().strip()}', "
                    f"'hello': '{self.ui.hello.toPlainText().strip()}', "
                    f"'doban': '{self.ui.doban.isChecked()}', "
                    f"'time': '{self.ui.time.value()}', "
                    f"'nums2ban': '{self.ui.nums2ban.value()}', "
                    f"'topnum': '{self.ui.topnum.value()}'}}"
                )
            printm("Данные сохранены...")

        def load(self):
            with open("quisettings.txt", "r", encoding="utf-8") as f:
                try:
                    data = json.loads(f.read().replace("'", '"').replace("\n", "\\n").replace("\\", "\\\\"))
                    for key in data.keys():
                        data[key] = data[key].replace("\\n", "\n").replace("\\\\", "\\")

                    self.ui.chat_id.setText(data["chat_id"])
                    self.ui.token.setText(data["token"])
                    self.ui.rules.setText(data["rules"])
                    self.ui.hello.setText(data["hello"])
                    self.ui.time.setValue(int(data["time"]))
                    self.ui.nums2ban.setValue(int(data["nums2ban"]))
                    self.ui.topnum.setValue(int(data["topnum"]))
                    self.ui.doban.setChecked(False if data["doban"] == "False" else True)

                    printm("Данные загружены...")
                except Exception as ex:
                    printm(ex)


    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    app.exec_()

except Exception as ex:
    print(ex)
