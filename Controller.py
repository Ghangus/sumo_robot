from multiprocessing import Process, Queue, Pool, Manager
from multipledispatch import *
import time

from Logger import *
from SensorManager import *


class Controller:
    pool = Pool(processes=3)
    process_manager = Manager()
    inbox = process_manager.Queue()
    logger_outbox = process_manager.Queue()
    sensor_outbox = process_manager.Queue()

    @staticmethod
    @dispatch(LoggerObject)
    def __handle_message(log_object):
        Controller.logger_outbox.put(log_object)

    @staticmethod
    def run():
        logger_thread = Controller.pool.apply_async(Logger.run, args=(Controller.logger_outbox,))
        sensor_thread = Controller.pool.apply_async(SensorManager.run, args=(Controller.sensor_outbox, Controller.inbox,))

        message = Controller.inbox.get()

        Controller.__handle_message(message)


if __name__ == "__main__":
    Controller.run()

