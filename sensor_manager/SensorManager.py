import RPi.GPIO as GPIO
import time
from multipledispatch import *
from sensor_manager.Sensors import *
from Logger import *


class SensorManager:

    def __init__(self):
        self.outbox = None
        self.initiated = False

    @staticmethod
    def __handle_init(sensor_init):
        SensorManager.outbox = sensor_init.outbox

    @dispatch(SonicDistance)
    def __handle_sensor(self, sonic_sensor):
        TRIG = 23
        ECHO = 24
        GPIO.setmode(GPIO.BCM)

        median_dist = 0

        GPIO.setup(TRIG, GPIO.OUT)
        GPIO.setup(ECHO, GPIO.IN)

        GPIO.output(TRIG, False)

        for _ in range(10):
            GPIO.output(TRIG, True)
            time.sleep(0.00001)
            GPIO.output(TRIG, False)

            while GPIO.input(ECHO) == 0:
                pulse_start = time.time()

            while GPIO.input(ECHO) == 1:
                pulse_end = time.time()

            pulse_duration = pulse_end - pulse_start

            distance = pulse_duration * 17150

            distance = round(distance, 2)

            median_dist += (distance - median_dist)/10

        print("Distance:", round(median_dist, 2), "cm")
        GPIO.cleanup()

        return median_dist

    @staticmethod
    def run(inbox, outbox):
        outbox.put(LoggerObject(LogLevel.INFO, "Sensor Manager Startup"))
        while True:
            message = inbox.get()
            SensorManager.__handle_sensor(message)


