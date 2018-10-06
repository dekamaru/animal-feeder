from feeder.base_feeder import BaseFeeder
import time


class OmegaBackend(BaseFeeder):
    def __init__(self):
        try:
            module = __import__('OmegaExpansion', globals(), locals(), ['pwmExp'], 0)
        except ImportError:
            raise ImportError

        self.pwmExp = module.pwmExp
        self.SERVO_PORT = 0
        if self.pwmExp.checkInit() == 0:
            self.pwmExp.driverInit()
            self.pwmExp.setFrequency(50)

    def convert_pulse_width_to_dc(self, pulse_width):
        return ((pulse_width / 1000.) / 20.) * 100

    def feed(self, portions):
        self.pwmExp.setupDriver(self.SERVO_PORT, self.convert_pulse_width_to_dc(1580), 0)
        time.sleep(1 * portions)
        self.pwmExp.disableChip()