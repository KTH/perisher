__author__ = 'tinglev'

import logging
import threading
from multiprocessing import Queue
import modules.validator as validator
import modules.log as log_module
import modules.azure.poll as azure_poller
from modules.exporters.prometheus_exporter import PrometheusExporter

log_module.init_logging()
log = logging.getLogger(__name__)

def run():
    try:
        azure_data_queue = Queue()
        poll_azure_lock = threading.Lock()
        poll_thread = threading.Thread(name='Azure thread',
                                       target=azure_poller.do_work,
                                       args=(azure_data_queue, poll_azure_lock))
        poll_thread.setDaemon(True)
        poll_thread.start()
        first_run = True
        while True:
            data = azure_data_queue.get()
            validator.validate_export_data(data)
            log.info(data)
            if first_run:
                PrometheusExporter().start_thread(data)
                first_run = False
    finally:
        poll_thread.join()

if __name__ == '__main__':
    run()
