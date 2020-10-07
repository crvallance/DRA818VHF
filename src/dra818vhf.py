import serial


class DRA818VHF(object):
    def __init__(self, serialport='/dev/ttyO4', baud=9600, timeout=1):
        self.serialport: str = serialport
        self.baud: int = baud
        self.timeout: int = timeout

    def __del__(self):
        try:
            self.conn.close()
        except AttributeError:
            pass

    def _connect(self):
        try:
            self.conn = serial.Serial(self.serialport, self.baud, timeout=self.timeout)
        except serial.SerialException as e:
            print(f'Connection issue: {e}')

    def _handshake(self):
        self._connect()
        try:
            self.conn.write(b'AT+DMOCONNECT\r\n')
            return(self.conn.readline())
        except ValueError:
            print()
            raise ValueError('Failed handshake.  Retrying')

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
            raise ValueError('Failed handshake.  Exiting')

    def check_volume(self, setvol: int):
        try:
            if 1 <= setvol <= 8:
                return(True)
        except ValueError:
            print(f'{setvol} is not between 1 and 8')
            raise

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

    def set_freq_scan(self):
        pass

    def set_group(self):
        pass

    def set_filter(self):
        pass