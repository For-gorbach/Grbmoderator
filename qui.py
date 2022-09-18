from PyQt5 import QtCore, QtGui, QtWidgets  # виджеты для работы с qt
from PyQt5.QtGui import QIcon  # для иконки
from GRBmoderatorUI import Ui_MainWindow  # импорт интерфейса
import json  # модуль для работы с json
import plyer  # модуль для push уведомлений
from main import main  # из файла main импортируем функцию main


def printm(msg):  # функция для того что бы писать сообщение и отправлять уведомление
    print(msg)  # пишем сообщение
    plyer.notification.notify(message=msg, app_name='GRBmoderator', app_icon='icon.ico', title='GRBmoderator', timeout=2, toast=True)  # уведомление


try:  # если в try ошибка то
    class MainWindow(QtWidgets.QMainWindow):  # класс объектов
        def __init__(self):  # инициализация класса
            super(MainWindow, self).__init__()  # создаем суперкласс
            self.ui = Ui_MainWindow()  # записываем интерфейс в объект (переменную класса)
            self.ui.setupUi(self)  # "скачивание" интерфейса
            self.init_UI()  # инициализация с интерфейсом

        def init_UI(self):  # функция инициализации с интерфейсом
            self.setWindowTitle("GRBmoderator bot")  # ставим название программе
            self.setWindowIcon(QIcon("icon.ico"))  # ставим иконку программе
            self.ui.start.clicked.connect(self.start)  # если нажали на кнопку запуска бота, то запускаем функцию start
            self.ui.deletedata.clicked.connect(self.deletedata)  # если нажали на кнопку удаления данных, то запускаем функцию deletedata
            self.ui.savedata.clicked.connect(self.savedata)  # если нажали на кнопку сохранения данных, то запускаем функцию savedata
            self.ui.load.clicked.connect(self.load)  # если нажали на кнопку загрузки данных, то запускаем функцию load

        def start(self):  # функция старта
            ################################################################################################
            chat_id = self.ui.chat_id.text().strip()
            token = self.ui.token.text().strip()
            rules = self.ui.rules.toPlainText().strip()
            hello = self.ui.hello.toPlainText().strip()
            doban = self.ui.doban.isChecked()
            time = self.ui.time.value()
            nums2ban = self.ui.nums2ban.value()
            topnum = self.ui.topnum.value()

            # выше мы получаем значения из интерфейса

            if chat_id == "":  # если chat_id пустой то
                printm("Вы не указали id чата!")  # пишем сообщение и создаем уведомление
            elif token == "":  # если if неверен и token пустой то
                printm("Вы не указали токен бота!")  # пишем сообщение и создаем уведомление
            else:  # если if и elif неверны то
                printm("Бот запущен!\n(При запуске окно перестанет 'отвечать', это связанно с особенностями языка).")  # пишем сообщение и создаем уведомление
                main(token, chat_id, rules, hello, doban, time, nums2ban, topnum)  # запускаем функцию main

        def deletedata(self):  # функция удаления данных
            with open("quisettings.txt", "w") as f:  # открываем файл настроек
                f.write("{'chat_id': '', 'token': '', 'rules': '', 'hello': '', 'doban': 'False', 'time': '', 'nums2ban': '', 'topnum': ''}")  # записываем пустые данные в файл
                printm("Данные из файла удалены...")  # пишем сообщение и создаем уведомление

        def savedata(self):  # функция сохранения данных
            with open("quisettings.txt", "w", encoding="utf-8") as f:  # открываем файл настроек
                f.write(
                    f"{{'chat_id': '{self.ui.chat_id.text().strip()}', "
                    f"'token': '{self.ui.token.text().strip()}', "
                    f"'rules': '{self.ui.rules.toPlainText().strip()}', "
                    f"'hello': '{self.ui.hello.toPlainText().strip()}', "
                    f"'doban': '{self.ui.doban.isChecked()}', "
                    f"'time': '{self.ui.time.value()}', "
                    f"'nums2ban': '{self.ui.nums2ban.value()}', "
                    f"'topnum': '{self.ui.topnum.value()}'}}"
                )  # записываем данные в файл
            printm("Данные сохранены...")  # пишем сообщение и создаем уведомление

        def load(self):  # функция загрузки данных
            with open("quisettings.txt", "r", encoding="utf-8") as f:  # открываем файл настроек
                try:  # если в try ошибка то
                    data = json.loads(f.read().replace("'", '"').replace("\n", "\\n").replace("\\", "\\\\"))  # загружаем в json значение из файла настроек, меняя ', \n и \\ на ", \\n и \\\\ соответствено
                    for key in data.keys():  # проходим по значениям словаря
                        data[key] = data[key].replace("\\n", "\n").replace("\\\\", "\\")  # изменяем \\n и \\\\ на \n и \\ соответствено

                    self.ui.chat_id.setText(data["chat_id"])  # ставим значение на параметр id чата
                    self.ui.token.setText(data["token"])  # ставим значение на параметр токена
                    self.ui.rules.setText(data["rules"])  # ставим значение на параметр правила
                    self.ui.hello.setText(data["hello"])  # ставим значение на параметр приветствия
                    self.ui.time.setValue(int(data["time"]))  # ставим значение на параметр ожидания для репорта
                    self.ui.nums2ban.setValue(int(data["nums2ban"]))  # ставим значение на параметр предупреждений до бана
                    self.ui.topnum.setValue(int(data["topnum"]))  # ставим значение на параметр топа
                    self.ui.doban.setChecked(False if data["doban"] == "False" else True)  # ставим (или не ставим) галочку на параметр бана

                    printm("Данные загружены...")  # пишем сообщение и создаем уведомление
                except Exception as ex:  # записываем ошибку в ex
                    printm(ex)  # пишем ошибку


    app = QtWidgets.QApplication([])  # интерфейс
    application = MainWindow()  # окно программы
    application.show()  # добавляем интерфейс в окно программы

    app.exec_()  # запускаем интерфейс

except Exception as ex:  # записываем ошибку в ex
    print(ex)  # пишем ошибку
