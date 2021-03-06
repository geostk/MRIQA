"""
Log Server
"""
import sys
from time import gmtime, strftime
from enum import Enum
from core.observer import Observer
from core.base_component import BaseComponent

class LogLevel(Enum):
    """"
    Enumeration for setting a log level
    """
    INFO = '\033[0m'
    DEBUG = '\033[0;37m'
    SUCCESS = '\033[92m'
    WARNING = '\033[93m'
    ERROR = '\033[91m'

class LogServer(BaseComponent):
    """
    Class for LogServer
    """
    def __init__(self):
        BaseComponent.__init__(self)
        self.log_observer = LogServer.LogObserver(self)

    class LogObserver(Observer):
        """
        Class for log observers
        """
        def __init__(self, outer):
            self.outer = outer
        def update(self, observable, package):
            log_message = strftime("%Y-%m-%d %H:%M:%S", gmtime()) + " " + \
                       package[1] + ": " + \
                       package[0]
            log_line = package[2].value + log_message + '\033[0m'
            if package[2] == LogLevel.ERROR:
                print(log_line, file=sys.stderr)
            else:
                print(log_line)
            self.outer.send({'log_message': log_message, 'log_level': package[2].name})
