import sys
from random import shuffle
from PyQt5.QtCore import QTimer
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.uic import loadUi


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Загрузка файла интерфейса .ui
        self.ui = loadUi('1.ui', self)
        self.ui.nextButton.clicked.connect(self.next)
        self.b1 = 0
        self.b2 = 0

    def next(self):
        self.counter = 0
        self.steps = 0

        self.n = self.ui.horizontalSlider.value()
        number = self.n * self.n
        self.images = [i for i in range(1, number // 2 + 1)] * 2
        if number % 2 != 0:
            self.images.append(number // 2 + 1)
        shuffle(self.images)
        self.ui = loadUi('2.ui', self)
        self.ui.backButton.clicked.connect(self.back)

        self.gd = self.ui.gridLayout
        # создание n * n кнопок и добавление их в gridLayout
        self.buttons = []
        for i in range(self.n):
            for j in range(self.n):
                button = QPushButton(str(i * self.n + j + 1))
                button.clicked.connect(self.on_button_clicked)
                button.setFixedSize(90, 90)
                self.gd.addWidget(button, i, j)
                self.buttons.append(button)

    def back(self):
        self.ui = loadUi('1.ui', self)
        self.ui.nextButton.clicked.connect(self.next)

    def on_button_clicked(self):
        sender = self.sender()
        # Получение позиции кнопки в сетке
        index = self.gd.indexOf(sender)
        x, y = self.gd.getItemPosition(index)[:2]
        button = self.gd.itemAt(index).widget()
        if button.text() == "":
            return
        QSound.play("1.wav")
        self.ui.backButton.setEnabled(False)
        button_num = x * self.n + y
        image_num = self.images[button_num]

        if self.b1 == 0:
            self.b1 = [button, image_num, button_num]
            self.update_steps()
        else:
            self.b2 = [button, image_num, button_num]

        button.setStyleSheet(
            f"QPushButton {{"
            f"    border-image: url(Images/{image_num}.png) 0 0 0 0 stretch stretch;"
            f"    text-align: center;"  # Выравниваем текст по центру кнопки
            f"}}"
        )

        button.setEnabled(False)
        button.setText("")
        if self.b2 != 0:
            self.turnOffButtons()
            QTimer.singleShot(1000, self.checkImages)

    def turnOffButtons(self):
        for b in self.buttons:
            b.setEnabled(False)

    def turnOnButtons(self):
        for b in self.buttons:
            b.setEnabled(True)

    def checkImages(self):
        self.ui.backButton.setEnabled(True)

        if self.b1[1] == self.b2[1]:
            QSound.play("2.wav")
            self.counter += 1
            if self.counter >= (self.n * self.n // 2):
                self.ui = loadUi('3.ui', self)
                QSound.play("3.wav")
                self.ui.startButton.clicked.connect(self.back)

        else:
            self.b1[0].setStyleSheet("")
            self.b2[0].setStyleSheet("")
            self.b1[0].setText(str(self.b1[2] + 1))
            self.b2[0].setText(str(self.b2[2] + 1))
        self.b1 = 0
        self.b2 = 0
        self.turnOnButtons()

    def update_steps(self):
        self.steps += 1
        self.ui.countlabel.setText(str(self.steps))


app = QApplication(sys.argv)
window = MyWindow()
window.show()
sys.exit(app.exec_())
