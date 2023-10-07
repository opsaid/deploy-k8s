from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
    inventory: oneops.cmdb.test
    version_added: "2.7"
    short_description: Returns string "mooooooxxxx" for values of stuff
    description:
        - Ignores whatever you give it
        - Returns inventory containing "mooooooxxxx"
'''

EXAMPLES = r'''
    # moooooxxxx
'''

from ansible.plugins.inventory import BaseInventoryPlugin

import json
import http.client

class InventoryModule(BaseInventoryPlugin):
    NAME = 'oneops.cmdb.test'

    def _get_cmdb(self):
        api_host = "api.grpc-kit.com"
        conn = http.client.HTTPConnection(api_host, 80)

        search_host_condition = [
            { "bk_obj_id": "host", "condition": [] },
            { 
                "bk_obj_id": "biz", 
                "fields": [ "bk_biz_id", "bk_biz_name", "pm2_uuid" ], 
                "condition": [ { "field": "pm2_uuid", "operator": "$eq", "value": "b8e8022a-18f2-4a03-999f-c6ee8c784528" } ]
            },
            {
                "bk_obj_id": "module",
                "fields": [ "bk_module_id", "bk_module_name", "bk_parent_id", "bk_set_id", "bk_biz_id" ]
            },
            {
                "bk_obj_id": "set",
                "fields": [ "bk_set_id", "bk_set_name", "bk_parent_id", "bk_biz_id" ]
            }
        ]
        search_host = { "page": { "sort": "-bk_host_id", "start": 0, "limit": 10 }, "condition": search_host_condition }

		# DEBUG 请求参数
        # print(json.dumps(search_host))

        headers = {"Authorization": "Bearer token"}

        conn.request(method="POST", url="/commons/cmdb/v1/hosts/search", body=json.dumps(search_host), headers=headers)
        r2 = conn.getresponse()
        print(r2.status, r2.reason)
        data2 = r2.read()
        data3 = json.loads(data2)
        print(data3["bk_error_msg"])
        conn.close()

    def parse(self, inventory, loader, path, cache=None):
        ''' doesnt parse the inventory file, but claims it did anyway '''
        super(InventoryModule, self).parse(inventory, loader, path)

        self._get_cmdb()

        self.inventory.add_group('all')
        self.inventory.add_group('pki')
        self.inventory.add_group('binary')
        self.inventory.add_group('etcd')
        self.inventory.add_group('kube_control_plane')
        self.inventory.add_group('kube_node')

        self.inventory.add_host(host='node0', group='pki', port='22')
        self.inventory.add_host(host='node0', group='binary', port='22')
        self.inventory.add_host(host='node1', group='kube_control_plane', port='22')
        self.inventory.add_host(host='node2', group='kube_control_plane', port='22')
        self.inventory.add_host(host='node3', group='kube_control_plane', port='22')
        self.inventory.add_host(host='node4', group='kube_node', port='22')

        self.inventory.set_variable(entity='node0', varname='ansible_connection', value='local')
        self.inventory.set_variable(entity='node1', varname='ansible_connection', value='ssh')
        self.inventory.set_variable(entity='node1', varname='ansible_host', value='192.168.31.201')
        self.inventory.set_variable(entity='node2', varname='ansible_connection', value='ssh')
        self.inventory.set_variable(entity='node2', varname='ansible_host', value='192.168.31.202-test')
        self.inventory.set_variable(entity='node3', varname='ansible_connection', value='ssh')
        self.inventory.set_variable(entity='node3', varname='ansible_host', value='192.168.31.203')
        self.inventory.set_variable(entity='node4', varname='ansible_connection', value='ssh')
        self.inventory.set_variable(entity='node4', varname='ansible_host', value='192.168.31.204')

        test_val = {"resource_reserve": { "kube": { "cpu": "100m", "memory": "100Mi" }, "system": { "cpu": "50m", "memory": "50Mi" } } }
        self.inventory.set_variable(entity='node4', varname='test_val', value=test_val)

