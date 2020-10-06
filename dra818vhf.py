import serial


class DRA818VHF(object):
    def __init__(self):
        self.__serialport: str = '/dev/ttyO4'
        self.__baud: int = 9600
        self.__timeout: int = 1

    def __del__(self):
        self.conn.close()

    def _connect(self):
        try:
            self.conn = serial.Serial(self.__serialport, self.__baud, timeout=self.__timeout)
        except serial.SerialException as e:
            print(f'Connection issue: {e}')

    def _handshake(self):
        self._connect()
        try:
            self.conn.write(b'AT+DMOCONNECT\r\n')
            return(self.conn.readline())
        except ValueError:
            print()
            raise SystemExit('Failed handshake.  Retrying')

    def _ensure_connection(self):
        for _ in range(3):
            try:
                data = self._handshake()
                data == b'+DMOCONNECT:0\r\n'
            except ValueError:
                continue
            else:
                break
        else:
            raise SystemExit('Failed handshake.  Exiting')

    def set_volume(self, setvol: int):
        self._ensure_connection()
        command = f'AT+DMOSETVOLUME={setvol}\r\n'
        assert(setvol in range(1, 8)), f'{setvol} is not between 1 and 8'
        try:
            self.conn.write(bytes(command, 'utf8'))
            data = self.conn.readline()
        except ValueError:
            print('')
        if data == b'+DMOSETVOLUME:0\r\n':
            print(f'Success: vol set to {setvol}')
        elif data == b'+DMOSETVOLUME:1\r\n':
            print('Volume set failed')
        else:
            raise NotImplementedError
