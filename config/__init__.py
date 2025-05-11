# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/28 20:34
@Author  : ShenXinjie
@Email   : 
@Desc    : 
"""

import os
import configparser


# obtain current project path
def get_project_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


my_config = configparser.ConfigParser()
my_config.read(os.path.join(get_project_root(), 'config/config.ini'))
ali_api_key = my_config.get('llm_ali', 'api_key')
