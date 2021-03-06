#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
from random import randint, shuffle
from time import sleep

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import (QGridLayout, QGroupBox, QMessageBox)

from src.rodafiltros.FilterControl import FilterControl
from src.rodafiltros.layout import set_hbox, set_lvbox


class PrototypeFilterWheelControl(QWidget):
    def __init__(self, parent=None):
        super(PrototypeFilterWheelControl, self).__init__(parent)

        self.serial_filter_wheel_info_l = None
        self.serial_filter_wheel_info_f = None
        self.slots_filter_wheel_info_l = None
        self.slots_filter_wheel_info_f = None
        self.tempt_filter_wheel_info_l = None
        self.tempt_filter_wheel_info_f = None
        self.shutter_l = None
        self.close_open_filter_wheel = None
        self.get_filter_l = None
        self.filter_position = None
        self.btn_set_filter = None
        self.set_filter_position = None
        self.btn_stress_test = None
        self.btn_home_position_filter = None
        self.btn_random = None

        self.roda_filtros = FilterControl()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createFilterWheelInfoGroup(), 0, 0)
        grid.addWidget(self.createFilterWheelGroup(), 1, 0)
        self.setLayout(grid)

        self.button_settings()

        self.setWindowTitle("PFWC")
        self.resize(60, 60)
        self.show()

    def createFilterWheelInfoGroup(self):
        groupBox = QGroupBox("&Filter Wheel Info")

        self.serial_filter_wheel_info_l = QtWidgets.QLabel("Serial Port: ", self)
        self.serial_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        try:
            motor_door_aux = str(self.roda_filtros.motor_door)
        except Exception as e:
            print(e)
            motor_door_aux = "???"

        self.serial_filter_wheel_info_f = QtWidgets.QLabel(motor_door_aux, self)
        self.serial_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.slots_filter_wheel_info_l = QtWidgets.QLabel("Filter Slot: ", self)
        self.slots_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.slots_filter_wheel_info_f = QtWidgets.QLabel("6", self)
        self.slots_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.tempt_filter_wheel_info_l = QtWidgets.QLabel("Filter Temperature: ", self)
        self.tempt_filter_wheel_info_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.tempt_filter_wheel_info_f = QtWidgets.QLabel("25 °C", self)
        self.tempt_filter_wheel_info_f.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        groupBox.setLayout(set_lvbox(set_hbox(self.serial_filter_wheel_info_l, self.serial_filter_wheel_info_f),
                                     set_hbox(self.slots_filter_wheel_info_l, self.slots_filter_wheel_info_f),
                                     set_hbox(self.tempt_filter_wheel_info_l, self.tempt_filter_wheel_info_f)))

        return groupBox

    def createFilterWheelGroup(self):
        groupBox = QGroupBox("&Filter Weel Control")

        self.shutter_l = QtWidgets.QLabel("Shutter:", self)
        self.shutter_l.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.close_open_filter_wheel = QtWidgets.QComboBox(self)
        self.close_open_filter_wheel.setMaximumWidth(100)
        self.fill_combo_close_open_filter_wheel_shutter()

        self.get_filter_l = QtWidgets.QLabel('Current filter:', self)
        # self.filter_position = QtWidgets.QLabel(self.roda_filtros.get_filtro_atual())
        self.filter_position = QtWidgets.QLabel("getfilter")

        self.filter_position.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.filter_position.setMinimumWidth(60)

        self.btn_set_filter = QtWidgets.QPushButton('Set filter', self)
        self.set_filter_position = QtWidgets.QComboBox(self)
        self.set_filter_position.setMaximumWidth(100)
        self.fill_combo_filter_position()

        self.btn_home_position_filter = QtWidgets.QPushButton('Home Reset', self)

        self.btn_random = QtWidgets.QPushButton('Random', self)

        self.btn_stress_test = QtWidgets.QPushButton('Test', self)

        groupBox.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open_filter_wheel),
                                     set_hbox(self.get_filter_l, self.filter_position, stretch2=1),
                                     set_hbox(self.btn_set_filter, self.set_filter_position),
                                     set_hbox(self.btn_home_position_filter),
                                     set_hbox(self.btn_random),
                                     set_hbox(self.btn_stress_test)))
        return groupBox

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message',
                                     "Are you sure to quit?", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def fill_combo_close_open_ccd_shutter(self):
        self.close_open.addItem("Open", 0)
        self.close_open.addItem("Close", 1)

    def fill_combo_close_open_filter_wheel_shutter(self):
        self.close_open_filter_wheel.addItem("Open", 1)
        self.close_open_filter_wheel.addItem("Close", 2)
        self.close_open_filter_wheel.currentIndexChanged[str].connect(self.my_slot_close_open_shutter)

    def my_slot_close_open_shutter(self, item):
        if item == "Close":
            self.roda_filtros.close_shutter()
        else:
            self.roda_filtros.open_shutter()

    def fill_combo_filter_position(self):
        self.set_filter_position.addItem("1", 1)
        self.set_filter_position.addItem("2", 2)
        self.set_filter_position.addItem("3", 3)
        self.set_filter_position.addItem("4", 4)
        self.set_filter_position.addItem("5", 5)
        self.set_filter_position.addItem("6", 6)

    def func_filter_position(self):
        try:
            sleep(1)
            wish_filter_int = self.set_filter_position.currentIndex() + 1
            self.roda_filtros.FilterWheel_Control(wish_filter_int)
            sleep(1)
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText(str(wish_filter_int))

    def button_settings(self):
        self.btn_set_filter.clicked.connect(self.func_filter_position)
        self.btn_home_position_filter.clicked.connect(self.func_home_position)
        self.btn_random.clicked.connect(self.func_random_test)
        self.btn_stress_test.clicked.connect(self.func_stress_test)

    def func_home_position(self):
        try:
            sleep(1)
            print("Home Position")
            self.roda_filtros.home_reset()
            sleep(1)
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText("1")

    def func_random_test(self):
        # Funcao que testa filtros aleatoriamente.
        try:
            sleep(1)
            wish_filter_int = self.set_filter_position.currentIndex() + 1

            self.roda_filtros.FilterWheel_Control(wish_filter_int)
            sleep(1)
            i = 0

            while i < 999999:
                aux = randint(1, 6)
                print("\n\n")
                print(aux)
                print("\n\n")

                self.roda_filtros.FilterWheel_Control(aux)
                i += 1
                sleep(15)

        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText(str(wish_filter_int))

    def func_stress_test(self):

        # Funcao que testa a lista my_list.
        try:
            sleep(1)
            wish_filter_int = self.set_filter_position.currentIndex() + 1
            i = 0
            # my_list tem a sequencia de filtros que será executado
            # my_list = [5, 1, 5, 2, 6, 1, 6, 2] # FAIL
            # my_list = [1, 6, 1, 2, 6]  # FAIL
            # my_list = [2, 3, 2, 4]  # ok 24 horas rodando
            # my_list = [2, 3, 2, 4]  # ok 3 horas rodando - testar novamente
            # my_list = [3, 4, 3, 5]  # FAIL
            # my_list = [1, 2, 3, 5, 6]  #
            # my_list = [3, 4]  # FAIL -   G=4 --> "P=13333"
            # my_list = [3, 4]  # OK G=4 --> "P=13332"
            # my_list = [4, 5]  # ok G=4 --> "P=13332" e G=5 --> "P=16665"
            # my_list = [5, 6]  # ok G=5 --> "P=16665" e G=6 --> "P=19998"
            # my_list = [6, 1]  #    falhou G=1 --> "P=3333" e G=6 --> "P=19998"
            # my_list = [6, 1]  # falhou G=1 --> "P=23333" e G=6 --> "P=19998"
            # my_list = [1, 2, 1, 3, 1, 4, 1, 5]  # Falha G=1 --> "P=3333" e G=6 --> "P=19998"
            # my_list = [3, 4, 3, 5, 3, 6]  #  Falha G=1 --> "P=3333" e G=6 --> "P=19998"
            my_list = [5, 6, 1, 2]  # Falha G=1 --> "P=3333" e G=6 --> "P=19998"
            while i < 999999:
                for number in my_list:
                    print("\n\n")
                    print("Wish Filter position: " + str(number))
                    self.roda_filtros.FilterWheel_Control(number)
                    sleep(15)
                i += 1
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText(str(wish_filter_int))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PrototypeFilterWheelControl()
    sys.exit(app.exec_())
