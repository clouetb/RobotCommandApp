import logging
import RPi.GPIO as GPIO

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

GPIO.setmode(GPIO.BOARD)

# DIR : 5 and 15
# PWM : 3 and 13
FREQUENCY = 50


class Motor:
    def __init__(self, _direction_pin, _speed_pin):
        log.info("Initializing motor with d=%d, s=%d", _direction_pin, _speed_pin)
        self.direction_pin = _direction_pin
        self.speed_pin = _speed_pin
        GPIO.setup(self.direction_pin, GPIO.OUT)
        GPIO.setup(self.speed_pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.speed_pin, FREQUENCY)
        self.pwm.start(0)
        log.debug("Motor initialization done %s", self.pwm)

    def run(self, speed):
        #log.debug("Setting speed to %d", speed)
        if speed > 0:
            GPIO.output(self.direction_pin, True)
        elif speed < 0:
            GPIO.output(self.direction_pin, False)
        else:
            self.pwm.ChangeDutyCycle(0)
            return
        self.pwm.ChangeDutyCycle(min(abs(speed), 100))


class Tank:
    def __init__(self, _left_direction_pin=5, _left_speed_pin=3, _right_direction_pin=15, _right_speed_pin=13):
        log.info("Initializing tank with ld=%d, ls=%d, rd=%d, rs=%d",
                 _left_direction_pin,
                 _left_speed_pin,
                 _right_direction_pin,
                 _right_speed_pin)
        self.left_motor = Motor(_left_direction_pin, _left_speed_pin)
        self.right_motor = Motor(_right_direction_pin, _right_speed_pin)
        self.left_speed = 0
        self.right_speed = 0
        log.debug("Tank initialization done")

    def set_speed(self, _left_speed, _right_speed):
        self.left_speed = _left_speed
        self.right_speed = _right_speed

    def run(self):
        #log.debug("Setting speed to l=%d, r=%d", self.left_speed, self.right_speed)
        self.left_motor.run(self.left_speed)
        self.right_motor.run(self.right_speed)

    def __del__(self):
        log.info("Cleaning-up GPIOs")
        self.left_motor = None
        self.right_motor = None
        GPIO.cleanup()
