from multiprocessing import Process, Queue
from multipledispatch import *
from Logger import *
import time


class Controller:
    @staticmethod
    def run():
        logger_queue = Queue()
        logger_thread = Process(target=Logger.run, args=(logger_queue,))
        logger_thread.start()

        logger_queue.put(LoggerObject(LogLevel.CRITICAL, "Test Log Message"))
        logger_queue.put(LoggerObject(LogLevel.ERROR, "Test Log Message"))
        logger_queue.put(LoggerObject(LogLevel.WARNING, "Test Log Message"))
        logger_queue.put(LoggerObject(LogLevel.INFO, "Test Log Message"))
        logger_queue.put(LoggerObject(LogLevel.DEBUG, "Test Log Message"))
        time.sleep(2)

        logger_thread.join()
