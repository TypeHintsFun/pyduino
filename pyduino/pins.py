
class Pin:
    def __init__(self, number: int, board): # Цикрулярный импорт толкает людей на ужасные вещи: отсутствие тайпхинтов
        self.number = number
        self.board = board

    @property
    def type(self) -> str:
        raise NotImplementedError()

    def read(self) -> int:
        command = f'R{self.type}{self.number}'.encode()
        self.board.conn.write(command)

        line_received = self.board.conn.readline().decode().strip()
        header, value = line_received.split(':')  # e.g. D13:1
        if header == f'D{self.number}':
            # If header matches
            return int(value)

    def write(self, value: int):
        command = f'W{self.type}{self.number}:{value}'.encode()
        self.board.conn.write(command)

    def set_mode(self, mode: str):
        mode = mode.upper()

        if mode != 'INPUT_PULLUP':
            mode = mode[0]
        else:
            mode = 'P'

        if mode not in ['I', 'O', 'P']:
            raise ValueError('Mode must be equal to one of the list: INPUT (I), OUTPUT (O), INPUT_PULLUP (P)')

        command = f'M{mode}{self.number}'.encode()
        self.board.conn.write(command)

    def __str__(self):
        return f'{self.type}{self.number} pin of {self.board}'

    def __int__(self):
        return self.read()


class DigitalPin(Pin):
    @property
    def type(self) -> str:
        return 'D'

    def write(self, value: int | bool):
        if isinstance(value, int) and value < 0 or value > 1:
            raise ValueError('value must be an bool or bool-like integer')

        if isinstance(value, bool):
            value = int(value)

        super(DigitalPin, self).write(value)

    def __bool__(self):
        return bool(self.read())


class AnalogPin(Pin):
    @property
    def type(self) -> str:
        return 'A'

    def write(self, value: int):
        if not 0 <= value <= 255:
            raise ValueError('value must be an integer between 0 and 255')

        super(AnalogPin, self).write(value)
