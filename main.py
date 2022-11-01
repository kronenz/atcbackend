#pip install flask 
#pip install flask_cors
#pip install ncclient
#pip xmltodict

from flask import Flask  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS, cross_origin

from ncclient import manager
from ncclient.xml_ import to_ele

import xmltodict,json

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
CORS(app)
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        return {"hello": "world!"}

#Kaloom NETCONF 접속 정보
klm_host = "10.0.20.150"
klm_user = "admin"
klm_pwd = "Forwiz_SDF1"

@api.route('/api/ksdf/get_all')
class ksdf_get_all(Resource):
    def get(self):
        return kaloom_netconf_get_all()

@api.route('/api/ksdf/all_packet_counters')
class ksdf_all_packet_counters(Resource):
    def get(self):
        rpc = """<GetPacketCounters xmlns="urn:kaloom:faas:fabrics"></GetPacketCounters>"""
        return kaloom_netconf_rpc(rpc)['fabrics:Results']

@api.route('/api/ksdf/get_all_tp_oper')
class ksdf_get_all_tp_oper(Resource):
    def get(self):
        rpc="""<get><filter type="subtree"><top xmlns="urn:kaloom:faas:fabrics"/><Fabric><FabricID>123</FabricID>
        <Node><Role></Role><TerminationPoint><OperState>UP</OperState></TerminationPoint></Node></Fabric></filter></get>""" 
        return kaloom_netconf_rpc(rpc)['data']['top']['fabrics:Fabric']

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

if __name__ == "__main__":
    app.run(debug=True, host='192.168.15.131', port=8000)
