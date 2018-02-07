#!/usr/bin/env python3

import yaml


class ParseConf:

    def __init__(self, config=None):
        if not config:
            config = './config.yaml'
        self.nodes = yaml.load(open(config))
        node = self.nodes['database']
        self.database = node['database']
        self.user = node['user']
        self.password = node['password']
        self.host = node['host']

    def get_node_by_name(self, nodename):
        node = self.nodes['nodes'][nodename]
        return node

    def get_all_nodes(self):
        ret = {}
        for node in self.nodes['nodes']:
            name = self.nodes['nodes'][node]['name']         
            ret[node] = (name, self.nodes['nodes'][node]['interfaces'])
        return ret

    def get_db_conn(self):
        db_conn = {}
        db_conn['user'] = self.user
        db_conn['password'] = self.password
        db_conn['host'] = self.host
        db_conn['database'] = self.database
        return db_conn

    def get_mail_server(self):
        return self.nodes['mail']['server']

    def get_from(self):
        return self.nodes['mail']['from']

    def get_to(self):
        return self.nodes['mail']['to']

