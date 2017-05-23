#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import (QGridLayout, QGroupBox)

from rodafiltros.FilterControl import *
from rodafiltros.layout import set_hbox, set_lvbox


class PrototypeFilterWheelControl(QWidget):
    def __init__(self, parent=None):
        super(PrototypeFilterWheelControl, self).__init__(parent)

        self.roda_filtros = FilterControl()
        self.initUI()

    def initUI(self):
        grid = QGridLayout()
        grid.addWidget(self.createFilterWheelInfoGroup(), 0, 0)
        grid.addWidget(self.createFilterWheelGroup(), 1, 0)
        self.setLayout(grid)

        self.setWindowTitle("Imager Box")
        self.resize(50, 34)
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
        self.filter_position = QtWidgets.QLabel(self.roda_filtros.get_filtro_atual())
        self.filter_position.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.filter_position.setMinimumWidth(60)

        self.btn_set_filter = QtWidgets.QPushButton('Set filter', self)
        self.set_filter_position = QtWidgets.QComboBox(self)
        self.set_filter_position.setMaximumWidth(100)
        self.fill_combo_filter_position()

        self.btn_home_position_filter = QtWidgets.QPushButton('Home Reset', self)

        groupBox.setLayout(set_lvbox(set_hbox(self.shutter_l, self.close_open_filter_wheel),
                                     set_hbox(self.get_filter_l, self.filter_position, stretch2=1),
                                     set_hbox(self.btn_set_filter, self.set_filter_position),
                                     set_hbox(self.btn_home_position_filter)))
        return groupBox

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

    def func_home_position(self):
        try:
            sleep(1)
            print("func_home_position")
            self.roda_filtros.home_reset()
            sleep(1)
            self.func_get_filter()
        except Exception as e:
            print(e)
        finally:
            self.filter_position.setText("1")


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = PrototypeFilterWheelControl()
    sys.exit(app.exec_())
