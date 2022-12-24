import serial
from .pins import AnalogPin, DigitalPin


class Arduino:
    def __init__(
            self,
            serial_port: str,
            digital_pins: int | list[int] = 13,
            analog_pins: int | list[int] = 5,
            *,
            serial_rate: int | None = 9600,
            timeout: int | None = 5):

        if serial_rate is None:
            serial_rate = 9600
        if timeout is None:
            timeout = 5

        self.conn = serial.Serial(serial_port, serial_rate)
        self.conn.timeout = timeout

        self.d: tuple[DigitalPin] = tuple(DigitalPin(d_pin, self) for d_pin in
                                          (range(digital_pins) if isinstance(digital_pins, int) else digital_pins))
        self.a: tuple[AnalogPin] = tuple(AnalogPin(a_pin, self) for a_pin in
                                         (range(analog_pins) if isinstance(analog_pins, int) else analog_pins))

    def set_pin_mode(self, pin_number: int, mode: str):
        return self.d[pin_number].set_mode(mode)

    def digital_read(self, pin_number: int):
        return self.d[pin_number].read()

    def digital_write(self, pin_number: int, digital_value: bool | int):
        return self.d[pin_number].write(digital_value)

    def analog_read(self, pin_number: int):
        return self.a[pin_number].read()

    def analog_write(self, pin_number: int, analog_value: int):
        return self.a[pin_number].write(analog_value)


class Uno(Arduino):
    def __init__(
            self,
            serial_port: str,
            *,
            serial_rate: int | None = 9600,
            timeout: int | None = 5):
        super(Uno, self).__init__(serial_port, 13, 6, serial_rate=serial_rate, timeout=timeout)
