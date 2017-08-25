__author__ = 'tinglev'

import logging
from threading import Timer, currentThread
from abc import ABCMeta, abstractmethod

class BaseExporter:
    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.log = logging.getLogger('({}) {}'.format(name, __name__))
        self.name = name
        self.export_dir = '/exports'

    @abstractmethod
    def get_interval_in_seconds(self): # pragma: no cover
        """ Number of seconds between runs """
        return -1

    @abstractmethod
    def export_function(self, data):
        """ Do the actual work - should only be called through run_export """
        return None

    def run_export(self, data):
        self.export_function(data)
        self.start_thread(data)

    def start_thread(self, data):
        timed_thread = Timer(self.get_interval_in_seconds(), self.run_export, (data,))
        timed_thread.name = self.name
        timed_thread.setDaemon(True)
        timed_thread.start()
