import smbus

class RotaryEncoderHandler(object):
    ARDUINO_ADDRESS = 0x10
    bus = smbus.SMBus(1)
    # * Register definitions:
    ARDUINO_RESET = 0x00
    ENCODER_IEN = 0x01
    ENCODER_READ_RIGHT = 0x02
    ENCODER_READ_LEFT = 0x03

    @staticmethod
    def read_address(reg_addr):
        return RotaryEncoderHandler.bus.read_byte_data(RotaryEncoderHandler.ARDUINO_ADDRESS, reg_addr)

    @staticmethod
    def resetArduino():
        RotaryEncoderHandler.bus.write_byte_data(RotaryEncoderHandler.ARDUINO_ADDRESS,
            RotaryEncoderHandler.ARDUINO_RESET, 0x01)
        RotaryEncoderHandler.enable_interrupt(is_enabled=False)
        RotaryEncoderHandler.readEncoderData()

    @staticmethod
    def readEncoderData():
        encoderVals = [0, 0]
        try:
            encoderVals[0] = RotaryEncoderHandler.read_address(RotaryEncoderHandler.ENCODER_READ_LEFT)
            encoderVals[1] = RotaryEncoderHandler.read_address(RotaryEncoderHandler.ENCODER_READ_RIGHT)
            for index, val in enumerate(encoderVals):
                if val > 127:
                    encoderVals[index] = (256-val) * -1
        except OSError:
            pass
        encoderVals[0] = -encoderVals[0]
        encoderVals[1] = -encoderVals[1]
        return encoderVals
    
    @staticmethod
    def enable_interrupt(is_enabled=False):
        RotaryEncoderHandler.bus.write_byte_data(RotaryEncoderHandler.ARDUINO_ADDRESS, 
            RotaryEncoderHandler.ENCODER_IEN, int(is_enabled))