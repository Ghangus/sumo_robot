import logging
import multipledispatch
import multiprocessing
from enum import IntEnum
from multipledispatch import *
import datetime

class LogLevel(IntEnum):
    CRITICAL = logging.CRITICAL
    ERROR = logging.ERROR
    WARNING = logging.WARNING
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    NONSET = 0


class LoggerObject:
    def __init__(self, _level=None, _message=None):
        self.level = _level
        self.message = _message


class Logger:
    FORMAT = '%(asctime)-15s %(levelname)s %(message)s'
    logging.basicConfig(filename='log_file_' + str(datetime.datetime.now()), level=logging.DEBUG, format=FORMAT)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(FORMAT))
    logger = logging.getLogger()
    logger.addHandler(ch)


    @staticmethod
    @dispatch(LoggerObject)
    def __handle__message(logger_object):
        Logger.logger.log(logger_object.level, logger_object.message)

    @staticmethod
    def run(inbox: 'multiprocessing.Queue'):
        while True:
            message = inbox.get()
            Logger.__handle__message(message)




