# -*- coding:utf-8 -*-
#!/usr/bin/env python 3.7
# Python version 2.7.16 or 3.7.6
'''
# FileName： path.py
# Author : YuYanQing
# Desc: PATH常量池
# Date： 2021/8/11 13:15
'''
import os
from BaseSetting import Route
from iutils.Loader import Loader
IMG_PATH = Route.getPath("test_img")
CSV_PATH = Route.getPath("test_csv")
JSON_PATH = Route.getPath("test_json")
YAML_PATH = Route.getPath("test_yaml")
VARIABLES_PATH = Route.getPath("variables")
LOCALHOST_PATH = Route.getPath("localhost")
PROPERTIES_PATH = Route.getPath("properties")
GLOBAL_VAR_PATH  = Route.joinPath("variables", "global.yaml")
APPPROPERTIES_PATH = os.path.join(Route.getPath("workspaces"),"application.properties.yaml")
PROFILES = Loader.yamlFile(APPPROPERTIES_PATH)["profiles"]
LOG_SWITCH = Loader.yamlFile(APPPROPERTIES_PATH)["log_switch"]
APPLICATION_PATH = os.path.join(Route.getPath("workspaces"),"application-{}.yaml".format(PROFILES))
DNS_PATH = os.path.join(Route.getPath("properties"),"dns_{}.yaml".format(PROFILES))
ADDRESS_PATH = os.path.join(Route.getPath("properties"),"address.yaml")
USER_VARS_PATH = os.path.join(Route.getPath("properties"),"user_vars.yaml")