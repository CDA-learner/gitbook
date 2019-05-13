#!/usr/bin/python
# -*- coding:UTF-8 -*-
import os
import sys
import ast
import argparse
import requests
import json
import cowsay
from datetime import datetime
from pyfiglet import Figlet

VAULT_PASSWD = 'Lygj123!@#'
OPS_API_HOST = 'https://ops.huihuang200.com'
OPS_CI_HOST = 'http://jenkins.ops.huihuang200.com'

HOSTS_API = OPS_API_HOST + "/api/ansible/projectdetail"

DING_API = "https://oapi.dingtalk.com/robot/send?access_token=5dffd206a86572cc10f018480551a0158295461418020404f8sdfsafdf"


class opstoolbox(object):
    def __init__(self):
        pass

    def get_data(self, api, project):
        url = api + '?server_name=' + project
        try:
            res = requests.get(url, timeout=5)
        except requests.RequestException as e:
            print(e)
        else:
            return res.json()

    def args(self):
        parser = argparse.ArgumentParser(
            description='deploy system base usage, example deploy_system_base.py -p jetty-deploy-system-base')
        parser.add_argument('--project', '-p', dest='project_name', default='none', help='set jenkins project name')
        parser.add_argument('--extra', '-e', dest='extra_parameter', default='', help='set jenkins extra parameters')
        args = parser.parse_args()
        return args

    def get_disconf(self, api, project, version):
        url = api + '?server_name=' + project + '&version=' + version
        try:
            res = requests.get(url, timeout=5)
        except requests.RequestException as e:
            print (e)
        else:
            return res.json()

    def get_data_json(self, api):
        try:
            res = requests.get(api, timeout=5)
        except requests.RequestException as e:
            print
            e
        else:
            return res.json()

    def get_data_raw(self, api):
        try:
            res = requests.get(api, timeout=5)
        except requests.RequestException as e:
            print (e )
        else:
            return res

    def get_deploy_dir(self):
        return datetime.now().strftime('%Y%m%d-%H%M%S')

    def print_acsii(self, textvalue):
        f = Figlet(font='slant')
        print
        f.renderText(textvalue)

    def print_cowsay(self, textvalue):
        cowsay.cow(textvalue)

    def open_file(self, file_url):
        try:
            with open(file_url, 'r') as f:
                data = json.load(f)
        except IOError as e:
            print
            e
        else:
            return data

    def write_file(self, file_url, file_content):
        try:
            with open(file_url, 'w') as f:
                f.write(file_content)
        except IOError as e:
            print (e)
            sys.exit(1)

    def download_file(self, dl_prefix, dl_name, dl_version, dl_file, dl_dir):
        download_home = dl_prefix + dl_name + '/' + dl_dir + '/' + dl_file
        # download_home = dl_file
        download_url = OPS_API_HOST + '/api/config/file?env=%s&type=0&version=%s&key=%s' % (
        dl_name, dl_version, dl_file)
        try:
            r = requests.get(download_url, timeout=5)
            r.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("Http Error:", errh)
            sys.exit(1)
        except requests.exceptions.ConnectionError as errc:
            print("Error Connecting:", errc)
            sys.exit(1)
        except requests.exceptions.Timeout as errt:
            print("Timeout Error:", errt)
            sys.exit(1)
        except requests.exceptions.RequestException as err:
            print("OOps: Something Else", err)
            sys.exit(1)
        else:
            self.write_file(download_home, r.content)
            return 'File download successfully: ' + download_home

    def empty_inventory(self, hostvar_api):
        hosts_inventory = self.get_data_json(hostvar_api)
        return hosts_inventory

    def get_loads(self, hostvar_api):
        hosts_inventory = self.get_data_json(hostvar_api)
        data = json.dumps(hosts_inventory, sort_keys=True, indent=4)
        return data

    def host_inventory(self, host_api, hostvar_api):
        hosts_inventory = self.get_data_json(host_api)
        hosts_vars = self.get_data_json(hostvar_api)
        hosts_inventory.update(hosts_vars)
        return hosts_inventory

    def host_inventory_vars(self, host_api):
        hosts_inventory = self.get_data_json(host_api)
        return hosts_inventory

    def merge_dicts(self, *dict_args):
        """
        Given any number of dicts, shallow copy and merge into a new dict,
        precedence goes to key value pairs in latter dicts.
        """
        result = {}
        for dictionary in dict_args:
            result.update(dictionary)
        return result

    def get_filter_merge_param(self, default_var, extra_var):
        for key in extra_var.keys():
            if not extra_var[key] or not key:
                del extra_var[key]
                continue
        data = self.merge_dicts(default_var, extra_var)
        data = json.dumps(data, sort_keys=True, indent=4)
        return data
