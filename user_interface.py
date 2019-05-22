import sys
import os
import random
from audio_recorder import record_to_file
from speaker_recognition import task_predict
from PySide2 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        self.result_text = ["Użytkownik zidentyfikowany - Kamil", "Użytkownik niezidentyfikowany"]

        self.start_button = QtWidgets.QPushButton("Rozpocznij nagranie!")
        self.exit_button = QtWidgets.QPushButton("Wyjdź")
        self.text = QtWidgets.QLabel("Naciśnij \"Rozpocznij nagranie!")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.text)

        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.exit_button)
        self.setLayout(self.layout)

        self.start_button.clicked.connect(self.change_text)
        self.exit_button.clicked.connect(self.close)

    def change_text(self):
        self.text.setText(" ")
        self.text.setText("Powiedz hasło")
        # self.start_button.setEnabled(False)
        # self.exit_button.setEnabled(False)
        record_to_file(os.path.join("/Users/netherwulf/Documents/Repozytoria Git/python-speaker-recognition", "demo.wav"))
        self.text.setText(" ")
        self.text.setText("Przetwarzam...")
        print(os.path.join("/Users/netherwulf/Documents", "demo.wav"))
        result = task_predict(os.path.join("/Users/netherwulf/Documents/Repozytoria Git/python-speaker-recognition", "demo.wav"),
                              os.path.join("/Users/netherwulf/Documents/Repozytoria Git/python-speaker-recognition",
                                           "model.out"))
        if os.path.exists(os.path.join("/Users/netherwulf/Documents/Repozytoria Git/python-speaker-recognition", "demo.wav")):
            os.remove(os.path.join("/Users/netherwulf/Documents/Repozytoria Git/python-speaker-recognition", "demo.wav"))
        self.text.setText(" ")
        self.text.setText(
            self.result_text[0] if str(result[0]) == "latarkaKamil" and 0.5 < float(result[1]) < 0.52 else
            self.result_text[1])
        # self.start_button.setEnabled(True)
        # self.exit_button.setEnabled(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    widget = MyWidget()
    widget.show()

    sys.exit(app.exec_())
