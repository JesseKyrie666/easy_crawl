import os
from fake_useragent import UserAgent


def get_header():
    """生成 User-Agent的值"""
    location = os.getcwd() + '/fake_useragent.json'
    ua = UserAgent(path=location)
    return ua.random


