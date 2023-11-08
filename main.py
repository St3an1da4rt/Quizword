from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton, QApplication, QWidget, QTextBrowser, QStackedWidget, \
    QMainWindow, QLabel, QHBoxLayout, QVBoxLayout, QComboBox, QFileDialog, QSlider, QLineEdit, QTableWidget, QProgressBar, QTableWidgetItem
import sys
import random
import csv
import os.path
import time
import sqlite3
import googletrans
import json

############################################### global_containers######################################################

first_value = 0
general_language = ''
language_matrix = {
    'English': 'en',
    'French': 'fr',
    'Russia': 'ru'
}

with open('words.json', 'r') as f:
    join = json.loads(f.read())
# print(join[])
filename = ''
tim = time.localtime().tm_mday
setting_words_count = 0

my_cwd = os.getcwd()
new_dir = 'all_files'
path = os.path.join(my_cwd, new_dir)
os.mkdir(path)

#############################################################################################################

style = '''
#stackWidget {
    background-color: #330099;
    color: #fff;
}

QPushButton {
    border-bottom: 2px solid #6622CC;
    border-radius: 6px;
    height: 20px;
    min-width: 50px;
    color: #fff;
    background-color: '#6633CC';
}

QSlider {
    height: 20px;
}

QComboBox {
    border-radius: 0px;
    padding: 1px 18px 1px 3px;
    height: 20px;
}

QComboBox:!editable, QComboBox::drop-down:editable {
     background: '#6633CC';
     border-radius: 5px;
}

/* QComboBox gets the "on" state when the popup is open */
QComboBox:!editable:on, QComboBox::drop-down:editable:on {
    background: '#6699CC'
}

QComboBox:on { /* shift the text when the popup opens */
    padding-top: 3px;
    padding-left: 4px;
}

QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 15px;

    border-left-width: 1px;
    border-left-color: darkgray;
    border-left-style: solid; /* just a single line */
    border-top-right-radius: 3px; /* same radius as the QComboBox */
    border-bottom-right-radius: 3px;
}

QComboBox::down-arrow {
    image: url(/usr/share/icons/crystalsvg/16x16/actions/1downarrow.png);
}

QComboBox::down-arrow:on { /* shift the arrow when popup is open */
    top: 1px;
    left: 1px;
}

QComboBox QAbstractItemView {
    border-radius: 10px;
    selection-background-color: lightgray;
}

QTableWidget {
    border-radius: 10px;
    width: 100vw;
    background-color: #6633CC;
}

QProgressBar {
    border: 2px solid #333399;
    border-radius: 5px;
    text-align: center;
}

QProgressBar::chunk {
    background-color: #9966CC;
    width: 10px;
    margin: 0.5px;
}

QTextBrowser {
    padding: 30px;
    border: 2px solid #9966CC;
    border-radius: 20px;
}
'''

back_main = '#331199'
back_widget = '#330099'
value_slider_and_progressbar = '#9966CC'
back_for_tableandprogressbar = '#6633CC'

################################################# database####################################################
connection = sqlite3.connect('datebase.db')
cursor = connection.cursor()

cursor.execute(f"""CREATE TABLE IF NOT EXISTS learned_table  (
            name_lesson TEXT,
            word TEXT,
            word_translate TEXT

);
""")

cursor.execute(f"""CREATE TABLE IF NOT EXISTS current_table (
            name_lesson TEXT,
            word TEXT,
            word_translate TEXT

);
""")

cursor.execute(f"""CREATE TABLE IF NOT EXISTS days_learn (
            count_words INTEGER,
            day INTEGER UNIQUE
);
""")

tim = time.localtime().tm_mday
cursor = connection.cursor()
if cursor.execute(f'''SELECT * FROM days_learn WHERE day = {tim}''').fetchall() == []:
    cursor.execute(f'''INSERT INTO days_learn VALUES ({0}, {tim})''')
    connection.commit()

connection.commit()

#############################################################################################################


############################################### Class - Setting###############################################
class setting(QMainWindow):
    def __init__(self, parent=None):  # root function
        super().__init__()
        self.value = '0'
        self.parent = parent
        self.setupUI()

    def setupUI(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.documentation = QTextBrowser()
        _translate = QtCore.QCoreApplication.translate
        self.documentation.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                              "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                              "p, li { white-space: pre-wrap; }\n"
                                              "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; font-style:italic;\">         Это приложение поможет вам изучать Английский язык, а точнее лексику английского языка.</span></p>\n"
                                              "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:12pt; font-weight:600; font-style:italic;\">На подобие Quizlet и Reword, только удобней. Ну чтож начнём, для начала укажите какой язык вы хотите изучать.</span></p></body></html>"))
        self.documentation.setAlignment(QtCore.Qt.AlignCenter)
        self.documentation.verticalScrollBar().hide()
        self.documentation.horizontalScrollBar().hide()

        self.language = QComboBox()
        self.language.addItem('English')
        self.language.addItem('French')
        self.language.addItem('German')

        model = self.language.model()
        model.item(1).setEnabled(False)
        model.item(2).setEnabled(False)
        self.language.setCurrentIndex(0)

        self.current_folder_documentation = QTextBrowser()
        _translate = QtCore.QCoreApplication.translate
        self.current_folder_documentation.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                             "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                             "p, li { white-space: pre-wrap; }\n"
                                                             "</style></head><body style=\" font-family:\'Ubuntu\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
                                                             "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:11pt; font-weight:600;\">А теперь выбирем нашу папку в которой будут сохраняться наши результаты.</span></p></body></html>"))
        self.current_folder_documentation.setAlignment(QtCore.Qt.AlignCenter)
        self.choose_folder = QPushButton('Выбрать файл')
        self.choose_folder.clicked.connect(self.take_fname)

        layout11 = QVBoxLayout()
        layout11.addWidget(self.documentation)
        layout11.addWidget(self.language)

        layout12 = QVBoxLayout()
        layout12.addWidget(self.current_folder_documentation)
        layout12.addWidget(self.choose_folder)

        layout1 = QHBoxLayout()
        layout1.addLayout(layout11)
        layout1.addLayout(layout12)

        self.difficult_word = QLabel('0')
        self.slider = QSlider()
        self.slider.setOrientation(QtCore.Qt.Horizontal)
        self.slider.setRange(0, 30)
        self.slider.valueChanged[int].connect(self.changeValue)
        self.forward = QPushButton('Далее')
        self.forward.clicked.connect(self._page_2)

        layout2 = QHBoxLayout()
        layout2.addWidget(self.difficult_word)
        layout2.addWidget(self.slider)
        layout2.addWidget(self.forward)

        self.indicator = QLabel()

        layout = QVBoxLayout(self.centralwidget)
        layout.addLayout(layout1)
        layout.addLayout(layout2)
        layout.addWidget(self.indicator)

        if os.path.exists('dictwriter.csv'):
            with open('dictwriter.csv', 'r', newline='', encoding="utf8") as f:
                global filename, setting_words_count
                setting_words_count, setting_language, setting_filename = list(
                    csv.reader(f, delimiter=',', quotechar='"'))[1]
                self.language.setEditText(setting_language)
                self.slider.setValue(int(setting_words_count))
                filename = setting_filename

    def changeValue(self, value):
        self.value = value
        self.difficult_word.setText(str(value))
        if 0 < value < 10:
            self.indicator.setText("Мало, но не плохо")
        elif 10 <= value < 20:
            self.indicator.setText("Хорошо!")
        elif 20 <= value < 30:
            self.indicator.setText(
                "Ты уверен? Ты действительно хочешь летать в английском языке?")

    def take_fname(self):
        self.filename = QFileDialog.getExistingDirectory(
            self,
            "Open a folder",
            "",
            QFileDialog.ShowDirsOnly
        )
        global filename
        filename = self.filename

    def _page_2(self):
        global general_language, setting
        data = {
            "word_on_day": int(self.value),
            "language": self.language.currentText(),
            "fname": filename if filename is not None else '/'
        }
        # print(data)
        with open('dictwriter.csv', 'w', newline='', encoding="utf8") as f:
            fieldnames = [i for i in data.keys()]
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerow(data)
        general_language = self.language.currentText()
        global tim
        tim = time.localtime().tm_mday
        cursor = connection.cursor()
        if cursor.execute(f'''SELECT * FROM days_learn WHERE day = {tim}''').fetchall() is None:
            cursor.execute(f'''INSERT INTO days_learn VALUES ({0}, {tim})''')
            connection.commit()
        self.parent.stackWidget.setCurrentIndex(1)

############################################### Progress class#################################################


class Progress(QMainWindow):
    def __init__(self, parent=None):  # root function
        super().__init__()
        global tim
        tim = time.localtime().tm_mday
        self.parent = parent
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        self.back_button = QPushButton('Настройки')
        self.back_button.clicked.connect(self.back_to_setting)

        self.teach_word = QPushButton('Учить новые слова')
        self.teach_word.clicked.connect(self._page_3)
        self.repeat_word = QPushButton('Повторить слова')
        self.repeat_word.clicked.connect(self._page_4)

        self.layouttrans = QHBoxLayout()

        self.first_lang = QLineEdit()
        self.trans = QPushButton('->')
        self.trans.clicked.connect(self.translator)
        self.second_lang = QLineEdit()

        self.layouttrans.addWidget(self.first_lang)
        self.layouttrans.addWidget(self.trans)
        self.layouttrans.addWidget(self.second_lang)

        self.table = QTableWidget(10, 3)
        self.table.verticalScrollBar().hide()
        self.table.horizontalHeader().setSectionResizeMode(1)
        result = connection.cursor().execute(
            f'''SELECT * FROM learned_table''').fetchall()[::-1][:10]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                cel = QTableWidgetItem(str(val))
                cel.setSizeHint(QtCore.QSize(
                    self.table.sizeHint().width(), 10))
                cel.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table.setItem(i, j, cel)

        cursor = connection.cursor()
        count = cursor.execute(
            f'''SELECT count_words FROM days_learn WHERE day = {tim}''').fetchone()
        connection.commit()
        self.progress_bar = QProgressBar()
        self.count_learn_words = int(
            (list(count)[0] / int(setting_words_count)) * 100)
        if self.count_learn_words > 100:
            self.progress_bar.setValue(100)
        else:
            self.progress_bar.setValue(self.count_learn_words)

        layout = QVBoxLayout(self.centralwidget)
        layout.addWidget(self.back_button)
        layout.addWidget(self.teach_word)
        layout.addWidget(self.repeat_word)
        layout.addLayout(self.layouttrans)
        layout.addWidget(self.table)
        layout.addWidget(self.progress_bar)

    def back_to_setting(self):
        self.parent.stackWidget.setCurrentIndex(0)

    def translator(self):
        try:
            text = self.first_lang.text()
            src = 'ru'
            dest = language_matrix[general_language]
            translator = googletrans.Translator()
            translation = translator.translate(text, src, dest)

            self.second_lang.setText(translation.text)
        except Exception as ex:
            print(ex)

    def _page_3(self):
        self.parent.stackWidget.setCurrentIndex(2)

    def _page_4(self):
        global first_value
        cur = connection.cursor()
        result = cur.execute('''SELECT * FROM current_table''').fetchall()
        first_value = len(result)
        self.parent.stackWidget.setCurrentIndex(3)
##############################################################################################################
################################################ word_learn_card class#########################################


class Learn_word(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.count = 0
        self.rand = 0
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.setupUi()
        print

    def setupUi(self):
        self.word_random()
        self.button_word = QPushButton(
            [self.word_translate, self.word][self.rand])
        self.button_word.clicked.connect(self._page_5)
        if len(self.word) < 200:
            self.button_word.setStyleSheet('width: 300px; min-height: 300px;')
        else:
            self.button_word.setStyleSheet('width: 500px;')
        self.button_back = QPushButton('Назад')
        self.button_back.clicked.connect(self._page_2)
        self.button_back.setStyleSheet('max-width: 40px;')
        self.label_lesson = QLabel(self.lesson)

        layouth = QHBoxLayout()
        self.button_know = QPushButton('Знаю')
        self.button_know.clicked.connect(self.next_word)
        self.button_notknow = QPushButton('Учить')
        self.button_notknow.clicked.connect(self.database_update)
        layouth.addWidget(self.button_know)
        layouth.addWidget(self.button_notknow)

        layout = QVBoxLayout(self.centralwidget)
        layout.addWidget(self.button_back)
        layout.addWidget(self.label_lesson, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.button_word, alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(layouth)

    def database_update(self):
        try:
            cur = connection.cursor()
            cur.execute(
                f'''INSERT INTO current_table (name_lesson, word, word_translate) VALUES ('{self.lesson}', '{self.word}', '{self.word_translate}');''')
            connection.commit()
            self.next_word()
        except:
            self.next_word()

    def _page_2(self):
        self.parent.stackWidget.setCurrentIndex(1)

    def _page_5(self):
        if self.count == 0:
            self.count = 1

            mat = [f"""{self.word}: {self.word_translate}""", f"""{self.word_translate}: {self.word}"""][self.rand]
            self.button_word.setText(mat)
            self.label_lesson.setText(self.lesson)
        else:
            self.count = 0
            self.button_word.setText(
                [self.word_translate, self.word][self.rand])
        if len(self.button_word.text()) > 50:
            self.button_word.setStyleSheet('width: 600px;')
        else:
            self.button_word.setStyleSheet('width: 300px; min-height: 300px;')

    def next_word(self):
        self.rand = random.randrange(2)
        self.word_random()
        self.label_lesson.setText(self.lesson)
        self.button_word.setText([self.word_translate, self.word][self.rand])

    def word_random(self):
        try:
            self.lesson = list(join)[random.randrange(len(join))]
            c = list(join[self.lesson])[
                random.randrange(len(join[self.lesson]))]
            self.word, self.word_translate = c
        except Exception as ex:
            self.word_random()

############################################## class - word_repeate#############################################


class Repeat_word(QMainWindow):
    def __init__(self, parent=None, page_2=None):
        super().__init__()
        self.page_2 = page_2
        self.parent = parent
        self.bul = 0
        self.count = 0
        self.rand = 0
        self.word = ''
        self.word_translate = ''
        self.lesson = ''

        self.setupUi()

    def setupUi(self):
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)

        layouth = QHBoxLayout()
        self.button_know = QPushButton('Вспомнил')
        self.button_notknow = QPushButton('Учить')
        layouth.addWidget(self.button_know)
        layouth.addWidget(self.button_notknow)
        self.button_know.clicked.connect(self.button_learn)
        self.button_notknow.clicked.connect(self.button_notlearn)

        self.label_lesson = QLabel(self.lesson)

        self.word_random()
        if self.bul == 0:
            self.button_word = QPushButton(
                [self.word_translate, self.word][self.rand])
            self.button_word.setStyleSheet('width: 300px; min-height: 300px;')
        else:
            self.label_lesson.hide()
            self.button_word = QPushButton('У вас нет выбранных слов')
            self.button_know.setEnabled(False)
            self.button_notknow.setEnabled(False)
        self.button_word.clicked.connect(self._page_5)
    

        layoutback = QHBoxLayout()
        self.button_back = QPushButton('Назад')
        self.button_back.clicked.connect(self._page_2)
        self.button_back.setStyleSheet('max-width: 40px;')
        self.progress = QProgressBar()
        layoutback.addWidget(self.button_back)
        layoutback.addWidget(self.progress)

        layout = QVBoxLayout(self.centralwidget)
        layout.addLayout(layoutback)
        layout.addWidget(self.label_lesson, alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.button_word, alignment=QtCore.Qt.AlignCenter)
        layout.addLayout(layouth)

    def word_random(self):
        cur = connection.cursor()
        result = cur.execute('''SELECT * FROM current_table''').fetchall()
        if result != []:
            self.bul = 0
            self.mat = result[random.randrange(len(result))]
            self.lesson, self.word, self.word_translate = self.mat
        else:
            self.bul = 1

    def button_learn(self):
        if self.progress.value() == 100:
            self.progress.setValue(0)
            cursor = connection.cursor()
            count = cursor.execute(
                f'''SELECT count_words FROM days_learn WHERE day = {tim}''').fetchone()
            cursor.execute(f'''UPDATE days_learn
                           SET count_words = {list(count)[0] + self.col_learn_words_now}
WHERE day = {tim};''')
            connection.commit()
            self.button_word.setText('Вы выучили все выбранные слова')
            self.button_know.setEnabled(False)
            self.button_notknow.setEnabled(False)
        else:
            with open(f'{filename + "/"}learned_words.txt', 'a+') as f:
                f.write(f'lesson: {self.lesson}, word: {self.word}, translate word: {self.word_translate};\n')

            cur = connection.cursor()
            cur.execute(
                f'''INSERT INTO learned_table (name_lesson, word, word_translate) VALUES ('{self.lesson}', '{self.word}', '{self.word_translate}');''')
            cur.execute(
                f'''DELETE FROM current_table WHERE word = "{self.word}"''')
            self.second_value = len(cur.execute(
                '''SELECT * FROM current_table''').fetchall())
            connection.commit()
            self.col_learn_words_now = first_value - self.second_value
            if first_value != 0:
                self.progress.setValue(
                    int((self.col_learn_words_now / first_value) * 100))
            self.button_notlearn()

    def button_notlearn(self):
        self.rand = random.randrange(2)
        self.word_random()
        self.label_lesson.setText(self.lesson)
        self.button_word.setText([self.word_translate, self.word][self.rand])

    def _page_2(self):
        result = connection.cursor().execute(
            f'''SELECT * FROM learned_table''').fetchall()[::-1][:10]
        for i, elem in enumerate(result):
            for j, val in enumerate(elem):
                cel = QTableWidgetItem(str(val))
                cel.setSizeHint(QtCore.QSize(
                    self.page_2.table.sizeHint().width(), 10))
                cel.setFlags(QtCore.Qt.ItemIsEnabled)
                self.page_2.table.setItem(i, j, cel)
        cursor = connection.cursor()
        count = cursor.execute(
            f'''SELECT count_words FROM days_learn WHERE day = {tim}''').fetchone()

        connection.commit()
        count_learn_words = int(
            (list(count)[0] / int(setting_words_count)) * 100)
        if count_learn_words > 100:
            self.page_2.progress_bar.setValue(100)
        else:
            self.page_2.progress_bar.setValue(count_learn_words)
        self.parent.stackWidget.setCurrentIndex(1)

    def _page_5(self):
        cur = connection.cursor()
        len_cur = len(cur.execute(
            '''SELECT * FROM current_table''').fetchall())
        if len_cur > 0:
            self.label_lesson.show()
            self.button_know.setEnabled(True)
            self.button_notknow.setEnabled(True)
            if self.count == 0:
                self.count = 1
                self.rand = random.randrange(2)
                if self.lesson != '':
                    mat = [f"""{self.word}: {self.word_translate}""",
                           f"""{self.word_translate}: {self.word}"""][self.rand]
                    self.button_word.setText(mat)
                else:
                    self.word_random()
                    mat = [f"""{self.word}: {self.word_translate}""", f"""{self.lesson}
        {self.word_translate}: {self.word}"""][self.rand]
                    self.label_lesson.setText(self.lesson)
                    self.button_word.setText(mat)
            else:
                self.count = 0
                self.button_word.setText(
                    [self.word_translate, self.word][self.rand])
                self.label_lesson.setText(self.lesson)
            if len(self.button_word.text()) > 100:
                self.button_word.setStyleSheet('width: 600px;')
            else:
                self.button_word.setStyleSheet(
                    'width: 300px; min-height: 300px;')
        else:
            self.label_lesson.hide()
            self.button_word.setText('У вас нет выбранных слов')

        # except Exception as ex:
        #     self.word_random()

################################## general class - main_window#################################################


class Main_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Quizword')
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
# create a stackwidget
        self.stackWidget = QStackedWidget()
        self.stackWidget.setStyleSheet(style)

        layout = QHBoxLayout(self.centralwidget)
        layout.addWidget(self.stackWidget)
# add page in the stackwidget
        self.page_1 = setting(self)
        self.stackWidget.addWidget(self.page_1)

        self.page_2 = Progress(self)
        self.stackWidget.addWidget(self.page_2)

        self.page_3 = Learn_word(self)
        self.stackWidget.addWidget(self.page_3)

        self.page_4 = Repeat_word(self, self.page_2)
        self.stackWidget.addWidget(self.page_4)

        self.stackWidget.setCurrentIndex(1)


##############################################################################################################


# initializiation
if "__main__" == __name__:
    app = QApplication(sys.argv)
    win = Main_Window()
    win.setStyleSheet(f'''background-color: {back_main};
                    color: #fff;''')
    win.show()
    sys.exit(app.exec())