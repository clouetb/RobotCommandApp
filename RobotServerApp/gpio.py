import time
import RPi.GPIO as GPIO
import threading
from random import randint

lPWM = 3
lDIR = 5

rPWM = 13
rDIR = 15


class LedsWaver(threading.Thread):
    def __init__(self, _pwm, _dir):
        threading.Thread.__init__(self)
        self.pwm = _pwm
        self.direction = _dir
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pwm, GPIO.OUT)
        GPIO.setup(self.direction, GPIO.OUT)
        GPIO.output(self.direction, GPIO.LOW)
        self.terminating = False

    def run(self):
        p = GPIO.PWM(self.pwm, 50) #frequency=50Hz
        p.start(0)
        sleep_time = randint(1, 9)
        print "Sleep time of %d : %d is %d" % (self.pwm, self.direction, sleep_time)
        while not self.terminating:
            for dc in range(0, 101, 5):
                p.ChangeDutyCycle(dc)
                time.sleep(sleep_time * 0.1)
            GPIO.output(self.direction, not GPIO.input(self.direction))
            for dc in range(100, -1, -5):
                p.ChangeDutyCycle
                time.sleep(sleep_time * 0.1)
        p.stop()
        print "Thread %d : %d stopped successfully" % (self.pwm, self.direction)

    def stop(self):
        self.terminating = True

try:
    a = LedsWaver(lPWM, lDIR)
    b = LedsWaver(rPWM, rDIR)
    a.start()
    b.start()
    time.sleep(3600)
except KeyboardInterrupt:
    pass
a.stop()
b.stop()
a.join()
b.join()
GPIO.cleanup()
