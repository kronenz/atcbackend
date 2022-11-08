# pip install pyvis
# pip install networkx
# pip install pandas
# pip install requests

from pyvis.network import Network
import networkx as nx
import pandas as pd

from opst_sdk_token import *

import requests
import json

base_ipv4 = '192.168.15.40'
access_port = '8041'
grpc_port = '50052'
auth_token = ''

def set_token(token):
    """API에 접근할 수 있는 토큰값을 셋팅하는 함수

    Args:
        token (string): 서버에서 grpc_token 기능을 호출하여 받은 값을 입력
    """
    auth_token = token

def set_acces_info(ipv4, port):
    """API서버의 IP주소와 , 접근 포트 번호를 셋팅하는 기능

    Args:
        ipv4 (string): IPv4 ex) '192.168.15.40'
        port (string): Access Port ex) '8041'
    """
    base_ipv4 = ipv4
    access_port = port

def get_with_x_auth(url):
    if auth_token == '':
        raise Exception("auth_token is Empty. please set_token")

    headers = {'X-Auth-Token': auth_token}
    r=requests.get(url, headers=headers)
    return(json.loads(r.text))

def getAllMetricInfo():
    fc_path = "/v1/metric"
    access_url = "http://" + base_ipv4 + ":" + access_port + fc_path
    all_info = get_with_x_auth(url= access_url)
    return all_info

def getAllResourceInfo():
    fc_path = "/v1/resource"
    access_url = "http://" + base_ipv4 + ":" + access_port + fc_path
    all_info = get_with_x_auth(url= access_url)
    print(all_info)
    return all_info

def getAllServerInfo():
    fc_path = "/v2.1/servers"
    access_url = "http://" + base_ipv4 + ":" + access_port + fc_path
    all_info = get_with_x_auth(url= access_url)
    print(all_info)
    return all_info


if __name__ == "__main__":
    print("start")
    auth_token = getOpstAdminToken('192.168.15.40:50052')
    print(auth_token)

    allServerinfo = getAllServerInfo()
    print(allServerinfo)
