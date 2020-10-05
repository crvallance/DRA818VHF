import serial


class DRA818VHF(object):
    def __init__(self):
        self.__serialport = '/dev/ttyO4'
        self.__baud = 9600
        self.__timeout = 1

    def connect(self):
        # conn = serial.Serial('/dev/ttyO4', 9600, timeout=1)
        try:
            self.conn = serial.Serial(self.__serialport, self.__baud, self.__timeout)
            return(self.conn)
        except serial.SerialException as e:
            print(f'Connection issue: {e}')

    def handshake(self):
        self.conn.write(b'AT+DMOCONNECT\r\n')
