from ncclient import manager
from ncclient.xml_ import to_ele

import xmltodict,json

#Kaloom NETCONF 접속 정보
klm_host = "10.0.20.150"
klm_user = "admin"
klm_pwd = "Forwiz_SDF1"

#Kaloom NETCONF 연결 관련
def kaloom_netconf_get_all():
    with manager.connect(host=klm_host, port=830, username=klm_user, password=klm_pwd, hostkey_verify=False) as m:
        c = m.get().xml
        parsed_data = xmltodict.parse(c)['rpc-reply']['data']
        return parsed_data

def kaloom_netconf_rpc(rpc):
    try:
        with manager.connect(host=klm_host, port=830, username=klm_user, password=klm_pwd, hostkey_verify=False) as m:
            c = m.rpc(to_ele(rpc)).xml
            parsed_data = xmltodict.parse(c)['rpc-reply']
            return parsed_data
    except: 
        return {"error": "cannot process the request"}