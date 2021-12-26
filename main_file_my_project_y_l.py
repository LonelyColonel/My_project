# импортируем все необходимые модули
import sys
import os
import win10toast
import sqlite3
from playsound import playsound
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from main_desinge_my_project import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QMessageBox, QLabel, QTimeEdit, QDateEdit, QPushButton, QLineEdit, QComboBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
import datetime as dt
import time

# устанавливаем необходимые стили, для создания окна создания будильника
Styles = """QLabel{background-color: rgb(255, 203, 97);
                  border:5px solid #aa8925}
           QTimeEdit{background-color: rgb(255, 203, 97);
                     border:5px solid #aa8925}
           QDateEdit{background-color: rgb(255, 203, 97);
                     border:5px solid #aa8925}
           QCheckBox{background-color: rgb(255, 203, 97);
                     border:5px solid #aa8925}
           QRadioButton{background-color: rgb(255, 203, 97);
                        border:5px solid #aa8925}
           QPushButton{background-color: rgb(255, 203, 97);
                       border-radius: 20px;
                       border:5px solid #aa8925}
           QLineEdit{background-color: rgb(255, 203, 97);
                        border:5px solid #aa8925}
           QComboBox {border: 1px solid gray; border-radius: 5px;
           padding: 1px 18px 1px 3px; min-width: 6em; background-color: rgb(255, 203, 97);}"""


# реализуем основной класс в котором будут реализованы все функции главного окна
class MyWindow(QMainWindow):
    # тех. переменная для функции отображения даты
    temp = False
    timeout = pyqtSignal()

    def __init__(self):
        # инициализируем все объекты
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # задаём фиксированный размер
        self.setFixedSize(500, 600)
        # устанавливаем стартовую "страницу" приложения
        self.ui.stackedWidget.setCurrentWidget(self.ui.started_page)
        # задаём период таймеров для отбражения времени на главной странице
        self.timer = QTimer()
        self.timer.timeout.connect(self.setdata)
        self.timer.start(1000)
        # задаём период таймеров для будильника
        self.timer.timeout.connect(self.check_alarm_clock_func)
        self.timer.start(1000)
        # переменные, чтобы трек не играл больше одного раза
        self.music_flag = True
        self.timer.timeout.connect(self.func_for_alarm)
        self.timer.start(60000)
        # задаём период таймеров для секундомера
        self.timer.timeout.connect(self.stopwatch_func)
        self.timer.start(1)
        # стартовые переменные секундомера
        self.isStart = False
        self.start_time = "00:00:00"

        # переменные для реализации таймера
        self.True_for_timer = True
        self.time_hours = 0
        self.time_min = 0
        self.time_sec = 0
        self.time_res = 0
        # устанавливаем временной интервал
        self.timer_main = QTimer()
        self.timer_main.setInterval(1000)
        self.timer_main.timeout.connect(self.change_and_update_timer)
        # установление соединения кнопок начальной страницы с функциями
        self.ui.start.clicked.connect(self.back_func)
        self.ui.about_pr.clicked.connect(self.about_pr_func)
        self.ui.textEdit.setReadOnly(True)
        self.ui.take_off_button_on_start_pg.clicked.connect(self.sys_exit)

        # кнопки меню
        self.ui.back_button_on_menu.clicked.connect(self.home)
        self.ui.back_ab_pr.clicked.connect(self.home)
        self.ui.stop_watch_button.clicked.connect(self.stop_watch_button_func)
        self.ui.timer_button.clicked.connect(self.timer_button_func)
        self.ui.tasks_button.clicked.connect(self.tasks_button_func)
        self.ui.another_time_button.clicked.connect(self.another_time_button_func)

        # кнопки будильника
        self.ui.alarm_clock_button.clicked.connect(self.create_alarm_clock_button_func)

        # кнопки заметок
        self.ui.back_button_on_tasks.clicked.connect(self.back_func)
        self.ui.home_button_on_tasks.clicked.connect(self.home)
        self.ui.pushButton_save_task.clicked.connect(self.write_task)
        self.ui.pushButton_load_task.clicked.connect(self.load_task_func)
        self.ui.pushButton_clear_task.clicked.connect(self.pushbutton_clear_task_func)

        # время в других часовых поясах
        self.ui.back_another_time.clicked.connect(self.back_func)
        self.ui.home_another_time.clicked.connect(self.home)
        self.ui.comboBox_city.activated[str].connect(self.city)

        # кнопки секундомера
        self.ui.pushButton_back_stopwatch.clicked.connect(self.back_func)
        self.ui.pushButton_home_stopwhatch.clicked.connect(self.home)
        self.ui.pushButton_start.clicked.connect(self.start_stopwatch)
        self.ui.pushButton_stop.clicked.connect(self.stop_stopwatch)
        self.ui.pushButton_write.clicked.connect(self.write_stopwatch)
        self.ui.pushButton_restart.clicked.connect(self.restart_stopwatch)

        # кнопки таймера
        self.ui.pushButton_back_timer.clicked.connect(self.back_func)
        self.ui.pushButton_home_timer.clicked.connect(self.home)
        self.ui.pushButton_start_timer.clicked.connect(self.timer_main.start)
        self.ui.pushButton_stop_timer.clicked.connect(self.timer_main.stop)
        self.ui.pushButton_restart_timer.clicked.connect(self.reset)
        self.ui.spinBox.valueChanged.connect(self.technical_var_timer)
        self.ui.spinBox_2.valueChanged.connect(self.technical_var_timer2)
        self.ui.spinBox_3.valueChanged.connect(self.technical_var_timer3)

    # создание функций для перехода между страниц приложения

    def back_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.menu)

    def home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.started_page)

    # печатаем текст о программе
    def about_pr_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.about_programme)
        self.ui.textEdit.setText("Это приложение - универсальные часы-будильник, здесь есть секундомер, таймер, "
                                 "заметки, время в других часовых поясах, будильник. Приложение будет развиваться, "
                                 "будут выходить новые версии. Данное приложение предназначено только для windows10."
                                 " Чтобы начать пользоваться достаточно нажать на кнопку 'начать' на главной странице."
                                 " Перемещатся по страницам можно с помощью кнопок в верхнем левом углу."
                                 "(стрелка назад - на предыдущую страницу; кнопка 'домик' возвращает на "
                                 "стартовую страницу). У секундомера есть функция промежуточной"
                                 " записи. Приложение показывает правильное время в других часовых поясах, "
                                 "только если на пк установлено верное точное время. Если поставлен какой-либо "
                                 "будильник, то когда наступит время его включения, окно закроится на время "
                                 "проигрывания выбранной музыки.")

    # функция для отображения нового окна с созданием будильника
    def create_alarm_clock_button_func(self):
        self.temp = Alarm_clock_class(parent=self)
        self.temp.show()

    # функции для перехода к странице секундомера
    def stop_watch_button_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.stopwatch)

    # функции для перехода к странице таймера
    def timer_button_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.timer)

    # функции для перехода к странице заметок
    def tasks_button_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.tasks)

    # функции для перехода к странице времени в других часовых поясах
    def another_time_button_func(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.another_time_2)

    # функция для проверки будильника. Должен ли зазвенеть сейчас будильник. Обновляется раз в секунду
    def check_alarm_clock_func(self):
        # установливаем соединение с БД
        con = sqlite3.connect('My_project_database.sqlite')
        cur = con.cursor()
        # узнаём время на данный момент
        self.now_time = dt.datetime.now().time().strftime('%H:%M')
        # ищем значение этого времени в БД
        time_check_db = cur.execute(f"""SELECT time FROM alarms_clocks WHERE time='{str(self.now_time)}'""").fetchall()
        # сравниваем, если значение в БД нашлось, хотя бы одно(а оно может быть только в единственном числе,
        # так как в классе создания будильника стоит фильтр на одинаковые будильники и соответственно двух
        # одинаковых будильников быть не может) и музыка ещё не играла(это определяется флагом self.music_flag),
        # то выполни код прописанный в условии.
        if len(list(time_check_db)) != 0 and self.music_flag:
            # если время время на данный момент совпадает с временем будильника из БД, то выполни запросы в БД и
            # проиграй музыку
            if self.now_time == list(time_check_db)[0][0]:
                name_alarm = cur.execute(f"""SELECT name FROM alarms_clocks WHERE
                                             time='{str(self.now_time)}'""").fetchall()
                musik_id_db = cur.execute(f"""SELECT musik_id FROM alarms_clocks
                                              WHERE time='{str(self.now_time)}'""").fetchall()
                music = cur.execute(
                    f"""SELECT music FROM musik WHERE id=(SELECT musik_id FROM 
                        alarms_clocks WHERE musik_id='{musik_id_db[0][0]}')""").fetchall()
                # окно на время проигрывания музыки прячется
                self.hide()
                self.music_flag = False
                playsound(list(music)[0][0])
                # удаляем этот будильник(который только что играл) из БД
                cur.execute("""DELETE FROM 'alarms_clocks' WHERE name=?""", (list(name_alarm)[0][0],))
                self.show()
        # подтверждаем
        con.commit()
        con.close()

    # спец. функция для того чтобы трэк не играл несколько раз в
    # минуту(ведь все треки длиной меньше минуты и получается в минуту трек может проиграть
    # несколько раз и чтобы такого не было вводим флаг)
    # данная функция обновляется каждую минуту
    def func_for_alarm(self):
        if not self.music_flag:
            self.music_flag = True

    # функция записи напечатанного текста в заметках в .txt файл
    def write_task(self):
        try:
            filename = QFileDialog.getSaveFileName(self, 'Запись файла .txt', os.getenv('HOME'),
                                                   'Текстовый формат (*.txt)')
            with open(filename[0], 'w', encoding='utf-8') as f:
                text_save = self.ui.textEdit_2.toPlainText()
                f.write(text_save)
        # исключение для того, чтобы не высвечивалась ошибка в консоле, если пользователь закрыл QFileDialog
        except FileNotFoundError:
            pass

    # функция загрузки файла формата .txt
    def load_task_func(self):
        try:
            filename = QFileDialog.getOpenFileName(self, 'Загрузка текстового файла', os.getenv('HOME'),
                                                   'Текстовый формат (*.txt)')
            with open(filename[0], 'r', encoding='utf-8') as f:
                text_load = f.read()
                self.ui.textEdit_2.setText(text_load)
        # исключение для того, чтобы не высвечивалась ошибка в консоле, если пользователь закрыл QFileDialog
        except FileNotFoundError:
            pass

    # функция для очистки окна заметок
    def pushbutton_clear_task_func(self):
        self.ui.textEdit_2.clear()

    # функция для отображения времени в других часовых поясах
    def city(self):
        # определяем отправителя сигнала
        temp_city = self.sender()
        if temp_city.currentText() == 'Москва' or temp_city.currentText() == 'Санкт-Петербург':
            time_no_format = dt.datetime.now()
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])
        elif temp_city.currentText() == 'Лондон':
            time_delta_anohter_city = dt.timedelta(hours=-3)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])
        elif temp_city.currentText() == 'Вашингтон':
            time_delta_anohter_city = dt.timedelta(hours=-8)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])
        elif temp_city.currentText() == 'Пекин':
            time_delta_anohter_city = dt.timedelta(hours=5)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])
        elif temp_city.currentText() == 'Владивосток':
            time_delta_anohter_city = dt.timedelta(hours=7)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])
        elif temp_city.currentText() == 'Токио':
            time_delta_anohter_city = dt.timedelta(hours=6)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Нью-Дели':
            time_delta_anohter_city = dt.timedelta(hours=2, minutes=30)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Джакарта':
            time_delta_anohter_city = dt.timedelta(hours=4)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Берлин':
            time_delta_anohter_city = dt.timedelta(hours=-2)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Рим':
            time_delta_anohter_city = dt.timedelta(hours=-2)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Сиэтл':
            time_delta_anohter_city = dt.timedelta(hours=-11)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Сантьяго':
            time_delta_anohter_city = dt.timedelta(hours=-6)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Джорджтаун':
            time_delta_anohter_city = dt.timedelta(hours=-7)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Канберра':
            time_delta_anohter_city = dt.timedelta(hours=8)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Париж':
            time_delta_anohter_city = dt.timedelta(hours=-2)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Тель-Авив':
            time_delta_anohter_city = dt.timedelta(hours=-1)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Нью-Йорк':
            time_delta_anohter_city = dt.timedelta(hours=-8)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Сингапур':
            time_delta_anohter_city = dt.timedelta(hours=5)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Киев':
            time_delta_anohter_city = dt.timedelta(hours=-1)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Иркутск':
            time_delta_anohter_city = dt.timedelta(hours=5)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

        elif temp_city.currentText() == 'Калининград':
            time_delta_anohter_city = dt.timedelta(hours=-1)
            time_no_format = dt.datetime.now() + time_delta_anohter_city
            time_res = time_no_format.strftime("%H:%M:%S")
            time_res2 = time_no_format.strftime("%d.%m.%Y")
            self.ui.label_time_another_time.setText(time_res)
            self.ui.label_date_another_time.setText(time_res2)
            self.ui.label_day_another_time.setText(self.slovar[time_no_format.weekday()])

    # функции для реализации секундомера
    # старт секундомера
    def start_stopwatch(self):
        self.isStart = True
        start_time_0 = dt.datetime.now().strftime("%M:%S:%f")
        self.start_time = dt.datetime.strptime(start_time_0, "%M:%S:%f")

    # остановка секундомера
    def stop_stopwatch(self):
        self.isStart = False

    # 'тело секундомера', обновляется раз в миллисекунду
    def stopwatch_func(self):
        if self.isStart:
            time_r = dt.datetime.strptime(dt.datetime.now().strftime("%M:%S:%f"), "%M:%S:%f") - self.start_time
            # перевод из переменной с типом timedelta коим является time_r в тип datetime, а затем в строку для вывода
            data_temp = dt.datetime(1, 1, 1)
            time_result = ((data_temp + time_r).strftime("%M:%S:%f"))[:9]
            # максимальное кол-во минут 99, если больше, то остановливаем таймер
            if int(time_result[:2]) > 99:
                self.isStart = False
            self.ui.label_time_stopwatch.setText(time_result)

    # функция для остановки и очистки секундомера
    def restart_stopwatch(self):
        self.isStart = False
        self.ui.label_time_stopwatch.setText('00:00:000')
        self.ui.textEdit_stopwhatch.setText("")

    # функция для записи секундомера
    def write_stopwatch(self):
        self.ui.textEdit_stopwhatch.append(self.ui.label_time_stopwatch.text())

    # функции для таймера
    # функция для отслеживания вводимых данных в spinBox(значение часов) и перевода часов в секунды
    def technical_var_timer(self, hours):
        self.time_hours = hours * 3600
        self.ui.label_timer_label.setText(time.strftime('%H:%M:%S', time.gmtime(self.time_hours)))

    # функция для отслеживания вводимых данных в spinBox_2(значение минут) и перевода минут в секунды
    def technical_var_timer2(self, minut):
        self.time_min = minut * 60
        self.ui.label_timer_label.setText(time.strftime('%H:%M:%S', time.gmtime(self.time_min)))

    # функция для отслеживания вводимых данных в spinBox_3(значение секунд)
    def technical_var_timer3(self, sec):
        self.time_sec = sec
        self.ui.label_timer_label.setText(time.strftime('%H:%M:%S', time.gmtime(self.time_sec)))

    # функция для изменения времени таймера(основная функция)
    def change_and_update_timer(self):
        # проверка для того чтобы таймер суммировал вводимое время один раз(при считывании ввода в spinBox-ы)
        # а дальше введённое время оставалось бы без изменений
        if self.True_for_timer:
            self.time_res = self.time_hours + self.time_min + self.time_sec
            self.True_for_timer = False
        # вычитаем из суммированного времени в секундах 1-у секунду
        self.time_res = self.time_res - 1
        # вызываем функцию для вывода
        self.label_timer(self.time_res)
        # проверка для того чтобы значение таймера не ушло в минус
        if self.time_res == 0:
            self.timer_main.stop()
            toaster = win10toast.ToastNotifier()
            toaster.show_toast("Таймер истёк!", "Универсальные часы-будильник", icon_path="clock_icon.ico", duration=3)
            while toaster.notification_active():
                time.sleep(0.1)

    # функция вывода
    def label_timer(self, time_result):
        self.time_res = time_result
        self.ui.label_timer_label.setText(time.strftime('%H:%M:%S', time.gmtime(self.time_res)))

    # функция для обнуления таймера
    def reset(self):
        # останавливаем обновление таймера
        self.timer_main.stop()
        # обнуление переменных
        self.True_for_timer = True
        self.time_res = 0
        self.time_hours = 0
        self.time_min = 0
        self.time_sec = 0
        self.technical_var_timer(self.time_hours)
        self.technical_var_timer2(self.time_min)
        self.technical_var_timer3(self.time_sec)

    # функция для отбражения тады, времени и дня недели на начальной странице приложения
    def setdata(self):
        # создаём словарь для правильного вывода пользователю дня недели (т.к. weekday()
        # возвращает числовое значения от 0 до 6, где 0 это понедельник, а 6 это воскресенье)
        self.slovar = {0: "Понедельник",
                       1: "Вторник",
                       2: "Среда",
                       3: "Четверг",
                       4: "Пятница",
                       5: "Суббота",
                       6: "Воскресенье"}
        # чередуем флагами, для отбражения времени каждую секунду
        if self.temp:
            self.now = dt.datetime.today().strftime("%H:%M:%S")
            self.temp = False
        else:
            self.now = dt.datetime.today().strftime("%H:%M:%S")
            self.temp = True
        # выводим на табло каждое значение
        self.ui.label_on_tasks_3.setText(self.now)
        self.ui.label_on_tasks_5.setText(dt.datetime.today().strftime("%d.%m.%Y"))
        self.ui.label_on_tasks_7.setText(self.slovar[dt.datetime.today().weekday()])

    # функция для высвечивания окна подтверждения при нажатии на кнопку выхода на начальной странице
    def sys_exit(self):
        confirm = QMessageBox()
        confirm.setWindowTitle("Подтверждение")
        confirm.setText("Вы уверены, что хотите выйти?")
        confirm.setIcon(QMessageBox.Question)
        confirm.addButton('Да', QMessageBox.YesRole)
        confirm.addButton('Нет', QMessageBox.NoRole)
        confirm.buttonClicked.connect(self.yes_func)
        confirm.exec_()

    # функция для закрытия окна, если пользователь нажал кнопку с текстом "Да"
    def yes_func(self, btn):
        if btn.text() == "Да":
            sys.exit()

    # функция для высвечивания подтверждения при нажатии на крестик главного окна
    def closeEvent(self, event):
        answer = QMessageBox.question(self, 'Подтверждение', "Вы уверены, что хотите выйти?",
                                      QMessageBox.Yes, QMessageBox.No)
        if answer == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


# класс для создания окна создания будильника
class Alarm_clock_class(QWidget):
    # инициализация
    def __init__(self, parent=None, *args):
        super().__init__(parent, Qt.Window)
        self.exstra_window_desinge(args)
        self.id_music = 1

    # функция создания дизайна окна для создания окна создания будильника
    def exstra_window_desinge(self, args):
        self.setStyleSheet(Styles)
        self.setWindowTitle('Будильник')
        self.setFixedSize(500, 600)
        self.label_main = QLabel('Создание будильника', self)
        self.label_main.move(100, 10)
        self.label_main.resize(291, 41)
        self.label_main.setFont(QFont('Tahoma', 20))

        self.label_name_alarm = QLabel('Название:', self)
        self.label_name_alarm.move(20, 80)
        self.label_name_alarm.resize(141, 41)
        self.label_name_alarm.setFont(QFont('Tahoma', 20))

        self.name_alarm = QLineEdit(self)
        self.name_alarm.move(170, 80)
        self.name_alarm.resize(301, 41)
        self.name_alarm.setFont(QFont('Tahoma', 20))

        self.label_time_name = QLabel('Время:', self)
        self.label_time_name.move(20, 130)
        self.label_time_name.resize(111, 41)
        self.label_time_name.setFont(QFont('Tahoma', 20))

        self.label_mistakes = QLabel('', self)
        self.label_mistakes.move(10, 300)
        self.label_mistakes.resize(480, 41)
        self.label_mistakes.setFont(QFont('Tahoma', 16))

        self.time_Edit = QTimeEdit(self)
        self.time_Edit.move(140, 130)
        self.time_Edit.resize(221, 41)
        self.time_Edit.setFont(QFont('Tahoma', 20))

        self.create_alarm_clock_button = QPushButton('Сохранить', self)
        self.create_alarm_clock_button.move(150, 530)
        self.create_alarm_clock_button.resize(191, 51)
        self.create_alarm_clock_button.setFont(QFont('Tahoma', 20))
        self.create_alarm_clock_button.clicked.connect(self.save_alarm_clock)

        self.combobox = QComboBox(self)
        self.combobox.addItems(['Выбор музыки', 'Трек1', 'Трек2', 'Трек3', 'Трек4', 'Трек5'])
        self.combobox.move(20, 200)
        self.combobox.resize(291, 61)
        self.combobox.setFont(QFont('Tahoma', 20))
        self.combobox.activated[str].connect(self.music_alarm_in_db)

    # функция для определения id музыки(для БД)
    def music_alarm_in_db(self):
        music_name = self.sender()
        if music_name.currentText() == "Трек1":
            self.id_music = 1
        elif music_name.currentText() == 'Трек2':
            self.id_music = 2
        elif music_name.currentText() == 'Трек3':
            self.id_music = 3
        elif music_name.currentText() == 'Трек4':
            self.id_music = 4
        elif music_name.currentText() == 'Трек5':
            self.id_music = 5
        elif music_name.currentText() == 'Музыка':
            self.id_music = 1

    # сохранение будильника
    def save_alarm_clock(self):
        # устанавливаем соединения с БД
        con = sqlite3.connect('My_project_database.sqlite')
        cur = con.cursor()
        value_in_db = self.name_alarm.text()
        # проверяем чтобы время записалось првильно(не 9:00, а 09:00)
        if len(self.time_Edit.text()) == 4:
            time_Edit_new = '0' + str(self.time_Edit.text())
        else:
            time_Edit_new = str(self.time_Edit.text())
        is_unique = cur.execute(f"""SELECT name FROM alarms_clocks WHERE name='{str(value_in_db)}'""").fetchall()
        # проверки на одинаковые будильники
        if len(list(is_unique)) != 0:
            self.label_mistakes.setText('Такой будильник уже есть, измените название!')
        is_unique = cur.execute(f"""SELECT time FROM alarms_clocks
                                    WHERE time='{str(self.time_Edit.text())}'""").fetchall()
        if len(list(is_unique)) != 0:
            self.label_mistakes.setText('Такой будильник уже есть, измените время!')
        else:
            # запись данных в БД
            cur.execute(f"""INSERT INTO alarms_clocks(name, time, musik_id)
                        VALUES('{str(value_in_db)}', '{time_Edit_new}', '{self.id_music}');""")
        con.commit()
        con.close()
        # закрытие окна
        self.close()


# функция для информативного вывода ошибок в pyqt5
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# для запуска
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWindow()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
