__author__ = 'tinglev'

import logging
import json
import threading
from modules.runner import Runner
from modules.environment import Environment

class PollingException(Exception):
    pass

log = None

CMD_LOGIN = ('az login --service-principal --tenant {} '
             '--username {} '
             '--password {}')
CMD_SET_ACCOUNT = 'az account set --subscription {}'
CMD_LIST_GROUPS = 'az group list --query "[?tags.{}==\'{}\']"'
CMD_LIST_VMS = 'az vm list --resource-group {}'
CMD_LIST_LBS = 'az network lb list --resource-group {}'
CMD_LIST_NICS = 'az network nic list --resource-group {}'
CMD_SHOW_NIC = 'az network nic show --ids {}'
CMD_SHOW_PUBLIC_IP = 'az network public-ip show --ids {}'

TEST_DATA = {'clusters': [{'lbs': [{'private_ip': '10.28.23.30', 'name': 'everest-black-service-lb-internal'}, {'fqdn': 'everest-black-dns.westeurope.cloudapp.azure.com', 'public_ip': '40.68.162.133', 'name': 'everest-black-worker-lb-public'}], 'vms': [{'private_ip': '10.28.23.22', 'name': 'everest-black-service0'}, {'private_ip': '10.28.23.20', 'name': 'everest-black-service1'}, {'private_ip': '10.28.23.21', 'name': 'everest-black-service2'}, {'private_ip': '10.28.23.132', 'name': 'everest-black-worker0'}, {'private_ip': '10.28.23.133', 'name': 'everest-black-worker1'}, {'private_ip': '10.28.23.134', 'name': 'everest-black-worker2'}], 'name': 'everest-black'}, {'lbs': [{'private_ip': '10.28.22.30', 'name': 'everest-purple-service-lb-internal'}, {'fqdn': 'everest-purple-dns.westeurope.cloudapp.azure.com', 'public_ip': '52.233.198.105', 'name': 'everest-purple-worker-lb-public'}], 'vms': [{'private_ip': '10.28.22.21', 'name': 'everest-purple-service0'}, {'private_ip': '10.28.22.20', 'name': 'everest-purple-service1'}, {'private_ip': '10.28.22.22', 'name': 'everest-purple-service2'}, {'private_ip': '10.28.22.134', 'name': 'everest-purple-worker0'}, {'private_ip': '10.28.22.132', 'name': 'everest-purple-worker1'}, {'private_ip': '10.28.22.133', 'name': 'everest-purple-worker2'}], 'name': 'everest-purple'}, {'lbs': [{'private_ip': '10.28.20.30', 'name': 'everest-teal-service-lb-internal'}, {'fqdn': 'everest-teal-dns.westeurope.cloudapp.azure.com', 'public_ip': '13.80.31.209', 'name': 'everest-teal-worker-lb-public'}], 'vms': [{'private_ip': '10.28.20.20', 'name': 'everest-teal-service0'}, {'private_ip': '10.28.20.22', 'name': 'everest-teal-service1'}, {'private_ip': '10.28.20.21', 'name': 'everest-teal-service2'}, {'private_ip': '10.28.20.134', 'name': 'everest-teal-worker0'}, {'private_ip': '10.28.20.132', 'name': 'everest-teal-worker1'}, {'private_ip': '10.28.20.133', 'name': 'everest-teal-worker2'}], 'name': 'everest-teal'}, {'lbs': [{'private_ip': '10.28.24.30', 'name': 'everest-white-service-lb-internal'}, {'fqdn': 'everest-white-dns.westeurope.cloudapp.azure.com', 'public_ip': '104.46.44.26', 'name': 'everest-white-worker-lb-public'}], 'vms': [{'private_ip': '10.28.24.22', 'name': 'everest-white-service0'}, {'private_ip': '10.28.24.20', 'name': 'everest-white-service1'}, {'private_ip': '10.28.24.21', 'name': 'everest-white-service2'}, {'private_ip': '10.28.24.133', 'name': 'everest-white-worker0'}, {'private_ip': '10.28.24.134', 'name': 'everest-white-worker1'}, {'private_ip': '10.28.24.132', 'name': 'everest-white-worker2'}], 'name': 'everest-white'}]}

def login():
    cmd = CMD_LOGIN.format(
        Environment.get_azure_tenant_id(),
        Environment.get_azure_username(),
        Environment.get_azure_certificate_path()
        )
    Runner.run_with_output(cmd)
    log.debug('Logged in to Azure')

def set_account():
    cmd = CMD_SET_ACCOUNT.format(Environment.get_azure_account_id())
    Runner.run_with_output(cmd)
    log.debug('Set account')

def get_resource_groups():
    tag_name = Environment.get_resource_group_tag_name()
    tag_value = Environment.get_resource_group_tag_value()
    cmd = CMD_LIST_GROUPS
    output = Runner.run_with_output(cmd.format(tag_name, tag_value))
    log.debug('Fetched cluster resource groups')
    return json.loads(output.decode('utf-8'))

def get_virtual_machines(resource_group_name):
    cmd = CMD_LIST_VMS.format(resource_group_name)
    log.debug('Fetched all virtual machines from cluster')
    return json.loads(Runner.run_with_output(cmd).decode('utf-8'))

def get_network_interface(interface_id):
    cmd = CMD_SHOW_NIC.format(interface_id)
    log.debug('Fetched network interface for virtual machine')
    return json.loads(Runner.run_with_output(cmd).decode('utf-8'))

def get_network_interfaces(resource_group_name):
    cmd = CMD_LIST_NICS.format(resource_group_name)
    log.debug('Fetched all network interfaces for resource group')
    return json.loads(Runner.run_with_output(cmd).decode('utf-8'))

def get_load_balancers(resource_group_name):
    cmd = CMD_LIST_LBS.format(resource_group_name)
    log.debug('Fetched all load balancers from cluster')
    return json.loads(Runner.run_with_output(cmd).decode('utf-8'))

def get_public_ip(public_ip_id):
    cmd = CMD_SHOW_PUBLIC_IP.format(public_ip_id)
    log.debug('Fetched public ip for load balancer')
    return json.loads(Runner.run_with_output(cmd).decode('utf-8'))

def process_virtual_machine(cluster_data, virtual_machine, nic_list):
    log.debug('Processing virtual machine "%s"', virtual_machine['name'])
    current_vm = {'name': virtual_machine['name']}
    interface_id = virtual_machine['networkProfile']['networkInterfaces'][0]['id']
    network_interface = find_network_interface_in_list(nic_list, interface_id)
    private_ip = network_interface['ipConfigurations'][0]['privateIpAddress']
    current_vm['private_ip'] = private_ip
    cluster_data['vms'].append(current_vm)
    return cluster_data

def find_network_interface_in_list(nic_list, id_to_find):
    for interface in nic_list:
        if interface['id'] == id_to_find:
            return interface
    raise PollingException()

def process_load_balancer(cluster_data, load_balancer): 
    log.debug('Processing load balancer "%s"', load_balancer['name'])                       
    current_lb_data = {'name': load_balancer['name']}
    current_lb_data = set_lb_private_ip(current_lb_data, load_balancer)
    current_lb_data = set_lb_public_ip(current_lb_data, load_balancer)
    cluster_data['lbs'].append(current_lb_data)
    return cluster_data

def set_lb_private_ip(current_lb_data, load_balancer):
    try:
        private_ip = load_balancer['frontendIpConfigurations'][0]['privateIpAddress']
        if not private_ip:
            raise KeyError
        log.debug('Load balancer has a private ip')
        current_lb_data['private_ip'] = private_ip
    except (KeyError, TypeError):
        log.debug('Load balancer is public (has no private ip)')
    return current_lb_data

def set_lb_public_ip(current_lb_data, load_balancer):
    try:
        public_ip_id = load_balancer['frontendIpConfigurations'][0]['publicIpAddress']['id']
        public_ip = get_public_ip(public_ip_id)
        fqdn = public_ip['dnsSettings']['fqdn']
        log.debug('Load balancer has a public ip')
        current_lb_data['public_ip'] = public_ip['ipAddress']
        current_lb_data['fqdn'] = fqdn
    except (KeyError, TypeError):
        log.debug('Load balancer is private (has no public ip)')
    return current_lb_data

def create_cluster_data(data, resource_group_name):
    cluster_data = {'name': resource_group_name, 'vms': [], 'lbs': []}
    data['clusters'].append(cluster_data)
    return cluster_data

def process_cluster(data, resource_group_name):
    log.debug('Processing resource group "%s"', resource_group_name)
    virtual_machines = get_virtual_machines(resource_group_name)
    cluster_data = create_cluster_data(data, resource_group_name)
    nic_list = get_network_interfaces(resource_group_name)
    for virtual_machine in virtual_machines:
        cluster_data = process_virtual_machine(cluster_data, virtual_machine, nic_list)
    load_balancers = get_load_balancers(resource_group_name)
    for load_balancer in load_balancers:
        cluster_data = process_load_balancer(cluster_data, load_balancer)
    return cluster_data

def do_work(queue, lock):
    global log
    log = logging.getLogger('({}) {}'
                            .format(threading.currentThread().getName(),
                                    __name__))
    lock.acquire()
    try:
        if Environment.get_skip_azure():
            data = TEST_DATA
            queue_data_and_schedule_thread(data, queue, lock)
        else:
            login()
            set_account()
            resource_groups = get_resource_groups()
            data = {'clusters': []}
            for resource_group in resource_groups:
                resource_group_name = resource_group['name']
                cluster_data = process_cluster(data, resource_group_name)
                data['clusters'].append(cluster_data)
            print(data)
            queue_data_and_schedule_thread(data, queue, lock)
    finally:
        lock.release()

def queue_data_and_schedule_thread(data, queue, lock):
    queue.put(data)
    timed_thread = threading.Timer(10,
                                   do_work,
                                   (queue, lock))
    timed_thread.name = 'Azure thread'
    timed_thread.start()
