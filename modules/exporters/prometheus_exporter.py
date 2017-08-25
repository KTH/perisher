__author__ = 'tinglev'

import json
from modules.exporters.base_exporter import BaseExporter
from modules.environment import Environment
import modules.validator as validator

class PrometheusExporter(BaseExporter):

    def __init__(self):
        super(PrometheusExporter, self).__init__('Prometheus')
        self.export_path = '{}/prometheus.json'.format(self.export_dir)

    def get_interval_in_seconds(self):
        return 5

    def export_function(self, data):
        self.log.info('Running prometheus export')
        prometheus_export = []
        for cluster in data['clusters']:
            cluster_obj = {'targets': [],
                           'labels': {
                               'cluster': cluster['name']
                           }
                          }
            for vm in cluster['vms']:
                cluster_obj['targets'].append(vm['private_ip'])
                cluster_obj['labels']['vm'] = vm['name']
            prometheus_export.append(cluster_obj)
        #self.log.info('Prometheus export: %s', json.dumps(prometheus_export))
        self.log.debug('Validating prometheus export data')
        validator.validate_prometheus_array(prometheus_export)
        self.log.debug('Writing prometheus export file to "%s"', self.export_path)
        with open(self.export_path, 'w') as export_file:
            json.dump(prometheus_export, export_file,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ': '))
