__author__ = 'tinglev'

import logging
from jsonschema import validate, FormatChecker, ValidationError
import modules.schema as schema

log = logging.getLogger(__name__)

def validate_prometheus_array(obj_array):
    try:
        for obj in obj_array:
            validate(obj, schema.SCHEMA_PROMETHEUS)
    except ValidationError as va_err:
        log.error('Json schema validation failed of prometheus export data: %s', va_err.message)
        raise

def validate_export_data(data):
    try:
        validate_data(data)
    except ValidationError as va_err:
        log.error('Json schema validation failed of Azure data: %s', va_err.message)
        raise

def validate_data(data):
    validate_root(data)
    for cluster in data["clusters"]:
        validate_cluster(cluster)
        log.debug('Validating VMs for cluster')
        for vm in cluster["vms"]:
            validate_vm(vm)
        log.debug('Validating LBs for cluster')
        for lb in cluster["lbs"]:
            validate_lb(lb)

def validate_cluster(cluster):
    log.debug('Validating cluster "%s"', cluster["name"])
    validate(cluster, schema.SCHEMA_CLUSTER)

def validate_vm(vm):
    validate(vm, schema.SCHEMA_VM, format_checker=FormatChecker())

def validate_lb(lb):
    validate(lb, schema.SCHEMA_LB, format_checker=FormatChecker())

def validate_root(data):
    log.debug('Validating root schema')
    validate(data, schema.SCHEMA_ROOT)
            
