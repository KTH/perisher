__author__ = 'tinglev'

import os

class Environment(object):

    @staticmethod
    def get_azure_username():
        return os.environ.get('AZURE_USERNAME')
    
    @staticmethod
    def get_azure_tenant_id():
        return os.environ.get('AZURE_TENANT_ID')

    @staticmethod
    def get_azure_certificate_path():
        return os.environ.get('AZURE_CERTIFICATE_PATH')

    @staticmethod
    def get_azure_account_id():
        return os.environ.get('AZURE_ACCOUNT_ID')

    @staticmethod
    def use_debug():
        return os.environ.get('DEBUG')

    @staticmethod
    def get_resource_group_tag_name():
        return os.environ.get('RESOURCE_GROUP_TAG_NAME')

    @staticmethod
    def get_resource_group_tag_value():
        return os.environ.get('RESOURCE_GROUP_TAG_VALUE')

    @staticmethod
    def get_skip_azure():
        return os.environ.get('SKIP_AZURE')
