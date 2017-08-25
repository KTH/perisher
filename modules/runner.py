__author__ = 'tinglev'

import subprocess

class Runner(object):

    @staticmethod
    def run_with_output(cmd):
        return subprocess.check_output("{0}".format(cmd), shell=True).rstrip()
