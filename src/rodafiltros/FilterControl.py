from time import sleep

import comtypes
import comtypes.client as cc
import comtypes.gen.INTEGMOTORINTERFACELib
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication

from src.rodafiltros import Leitura_portas
from src.rodafiltros.singleton import Singleton


class FilterControl(metaclass=Singleton):

    def __init__(self):
        self.hPosition = None
        self.smi = None
        self.CommInterface = None
        self.motor_door = None
        self.connect_state = False
        self.connect()
        self.CommInterface.AddressMotorChain()

    def connect(self):
        self.smi = cc.CreateObject('SMIEngine.SMIHost')
        cc.GetModule('IntegMotorInterface.dll')
        self.CommInterface = self.smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
        self.motor_door = None
        self.estabilish_link()

    def estabilish_link(self):
        sleep(1)
        self.CommInterface.BaudRate = 9600
        serial_list = Leitura_portas.serial_ports()
        count_aux = int(len(serial_list))
        for count in range(0, count_aux):
            print("Search for " + serial_list[count] + " link to Motors!")
            try:
                self.CommInterface.OpenPort(serial_list[count])
                self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
                self.CommInterface.WriteCommand("UBO")  # Make sure USER Bit B is output bit (UBO)
                self.CommInterface.WriteCommand("d=-1 GOSUB1")
                resposta = self.CommInterface.ReadResponse()
                if resposta == 'SHTR:???':
                    # print(serial_list[count] + " - Established a link to Motors!")
                    self.smi.QueryInterface(comtypes.gen.INTEGMOTORINTERFACELib.ISMIComm)
                    self.connect_state = True
                    self.motor_door = serial_list[count]
                    print("Home Reset")
                    self.home_reset()
                    break
            except Exception:
                print(serial_list[count] + " - Cannot establish a link to Motors")

    def open_shutter(self):
        try:
            self.CommInterface.WriteCommand("UB=1")  # Make sure shutter is in the closed state
            sleep(1)
        except Exception as e:
            print("Open Shutter ERROR -> {}".format(e))

    def close_shutter(self):
        try:
            self.CommInterface.WriteCommand("UB=0")
            sleep(1)
        except Exception as e:
            print("Close Shutter ERROR -> {}".format(e))

    def home_reset(self):
        QGuiApplication.setOverrideCursor(Qt.WaitCursor)

        # self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain
        # Make an SMIMotor object
        Motor = self.CommInterface.GetMotor(1)
        '''
        GOSUB5 - SMARTMOTOR
        '''
        try:
            DefaultMotor = 1
            self.CommInterface.WriteCommand("DOUTA0,b=7")
            self.CommInterface.WriteCommand("DOUTA0,b=3")
            self.CommInterface.WriteCommand("DOUTA0,b=7")
            self.CommInterface.WriteCommand("WAIT=500")

            # Initializa SMARTMOTOR variables
            self.CommInterface.WriteCommand("AMPS=100")
            self.CommInterface.WriteCommand("MP")
            self.CommInterface.WriteCommand("KGON")
            self.CommInterface.WriteCommand("KGOFF")
            self.CommInterface.WriteCommand("KP175")
            self.CommInterface.WriteCommand("KI=60")
            self.CommInterface.WriteCommand("F")

            # Sets velocity and acceleration of the motor

            self.CommInterface.WriteCommand("A=250")
            self.CommInterface.WriteCommand("V=25000")
            command = "a=UAI Ra"
            i = self.CommInterface.GetResponseOf(command)
            if i == '0':
                self.CommInterface.WriteCommand("i=@P-500")
                self.CommInterface.WriteCommand("P=i")
                self.CommInterface.WriteCommand("MP")
                self.CommInterface.WriteCommand("G")  # Make the filter move to next position
                Motor.WaitForStop()

            self.CommInterface.WriteCommand("MV")
            self.CommInterface.WriteCommand("UAI")
            self.CommInterface.WriteCommand("G")  # Make the filter move to next position

            command = "a=UAI Ra"
            i = self.CommInterface.GetResponseOf(command)

            while i == '1':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)
            while i == '0':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)

            self.CommInterface.WriteCommand("A=200")
            self.CommInterface.WriteCommand("V=-750")
            self.CommInterface.WriteCommand("G")  # Make the filter move to position

            while i == '1':
                command = "a=UAI Ra"
                i = self.CommInterface.GetResponseOf(command)

            self.CommInterface.WriteCommand("A=2000")
            self.CommInterface.WriteCommand("X")
            # Call
            Motor.WaitForStop()
            self.CommInterface.WriteCommand("WAIT=400")
            self.CommInterface.WriteCommand("O=1798")
            self.CommInterface.WriteCommand("MP")

            self.CommInterface.WriteCommand("A=250")
            self.CommInterface.WriteCommand("V=400000")
            self.CommInterface.WriteCommand("P=3333")
            self.CommInterface.WriteCommand("G")  # Make the filter move to position
            # Call
            Motor.WaitForStop()
            self.CommInterface.WriteCommand("WAIT=500")
            self.CommInterface.WriteCommand("h=1")
            self.CommInterface.WriteCommand("RETURN")
            self.hPosition = 1
            self.CommInterface.WriteCommand("g=-1")
            sleep(5)
            self.hPosition = int(self.hPosition)
            return self.hPosition

        except Exception as e:
            print("------------------------------------")
            print("Home reset ERROR -> {}".format(e))
            print("------------------------------------")
        finally:
            print("----------------------------------------------------")
            print("Filter position: " + str(self.hPosition))
            print("----------------------------------------------------\n")
            QGuiApplication.restoreOverrideCursor()

    def get_filtro_atual(self):
        if self.connect_state:
            # self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain

            sleep(0.5)
            self.CommInterface.WriteCommand("g=-1 GOSUB4")
            resposta = self.CommInterface.ReadResponse()

            print("\n\n")
            print("resposta = " + str(resposta))
            print("\n\n")

            sleep(0.5)

            return resposta[-1]
        else:
            return "None"

    def clear_buffer(self):
        self.CommInterface.ClearBuffer()

    def closePort(self):
        self.CommInterface.ClosePort()

    def FilterWheel_Control(self, FilterNumber):
        '''
        :param FilterNumber(int): numero do filtro desejado
        :return: Posição atual do filtro.
        '''

        QGuiApplication.setOverrideCursor(Qt.WaitCursor)

        # self.CommInterface.AddressMotorChain()  # Address SmartMotors in the RS232 daisy chain

        # self.hPosition = self.get_filtro_atual()

        #self.get_filtro_atual()

        #self.hPosition = self.hPosition

        #print("\n\nzzzzzzzzzzzzzzzzz")
        #print("type self.hPosition = " + str(type(self.hPosition)))
        #print("self.hPosition = " + str(self.hPosition))
        #print("type self.get_filtro_atual() = " + str(type(self.get_filtro_atual())))
        #print("zzzzzzzzzzzzzzzzzzzzzzz\n\n")

        FilterNumber = int(FilterNumber)

        if FilterNumber == 1:
            command = "g=1"
        if FilterNumber == 2:
            command = "g=2"
        if FilterNumber == 3:
            command = "g=3"
        if FilterNumber == 4:
            command = "g=4"
        if FilterNumber == 5:
            command = "g=5"
        if FilterNumber == 6:
            command = "g=6"

        #sleep(0.5)
        self.CommInterface.WriteCommand(command)  # Send filter position
        sleep(0.5)

        g = int(FilterNumber)  # Filter position
        h = int(self.hPosition)  # Present position

       # print("type FilterNumber = " + str(type(FilterNumber)))

        print("h = " + str(h))
        print("g = " + str(g))
        print("FilterNumber = " + str(FilterNumber))

        if h == 1:  # Present position is 3333
            if g == 1:
                self.CommInterface.WriteCommand("P=3333")
            if g == 2:
                self.CommInterface.WriteCommand("P=6666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=-3333") 	 # Move in opposite direction
            if g == 6:
                self.CommInterface.WriteCommand("P=0") 		 # Do not move

        if h == 2:  # Present position is 6666
            if g == 1:
                self.CommInterface.WriteCommand("P=3333")
            if g == 2:
                self.CommInterface.WriteCommand("P=6666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=16665")
            if g == 6:
                self.CommInterface.WriteCommand("P=0")

        if h == 3:  # Present position is 9999
            if g == 1:
                self.CommInterface.WriteCommand("P=3333")
            if g == 2:
                self.CommInterface.WriteCommand("P=6666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=16665")
            if g == 6:
                self.CommInterface.WriteCommand("P=19998")

        if h == 4:  # Present position is 13332
            if g == 1:
                self.CommInterface.WriteCommand("P=3333")
            if g == 2:
                self.CommInterface.WriteCommand("P=6666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=16665")
            if g == 6:
                self.CommInterface.WriteCommand("P=19998")

        if h == 5:  # Present position is 16665
            if g == 1:
                self.CommInterface.WriteCommand("P=23332")
            if g == 2:
                self.CommInterface.WriteCommand("P=26666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=16665")
            if g == 6:
                self.CommInterface.WriteCommand("P=20000")

        if h == 6:  # Present position is 20000
            if g == 1:
                self.CommInterface.WriteCommand("P=23332")
            if g == 2:
                self.CommInterface.WriteCommand("P=26666")
            if g == 3:
                self.CommInterface.WriteCommand("P=9999")
            if g == 4:
                self.CommInterface.WriteCommand("P=13332")
            if g == 5:
                self.CommInterface.WriteCommand("P=16665")
            if g == 6:
                self.CommInterface.WriteCommand("P=20000")

        self.CommInterface.WriteCommand("G")  # Make the filter move to next position
        sleep(1.5)  # Wait until the trajectory is finished

        self.CommInterface.WriteCommand("h=g")  # Reset the present filter position
        self.CommInterface.WriteCommand("O=h*3333")  # And reset the present origin
        self.CommInterface.WriteCommand("END")
        self.hPosition = FilterNumber  # h receive g for VB use

        print("----------------------------------------------------")
        print("Filter position: " + str(FilterNumber))
        print("----------------------------------------------------\n")

        self.hPosition = int(FilterNumber)

        QGuiApplication.restoreOverrideCursor()

        return FilterNumber
