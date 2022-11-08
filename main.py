#pip install flask 
#pip install flask_cors
#pip install ncclient
#pip xmltodict
#pip install apscheduler

from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS, cross_origin

from ksdf_netconf import *
from ksdf_topology import *
from ksdf_packet_counter import *

from apscheduler.schedulers.background import BackgroundScheduler

# Packet Counter 수집 Sensor

collection_interval=5
cur_packet_counter=get_cur_counter()
cur_gcd=None
cur_gcd_rate=None

def packet_counter_sensor():
    global cur_packet_counter
    global cur_gcd
    global cur_gcd_rate
    next_cur_packet_counter=get_cur_counter()
    cur_gcd=get_counter_diff(next_cur_packet_counter,cur_packet_counter)
    #print(cur_gcd)
    cur_gcd_rate=get_rate_from_gcd(cur_gcd)
    cur_packet_counter=next_cur_packet_counter
    #print(cur_gcd_rate)

sched = BackgroundScheduler(daemon=True)
sched.add_job(packet_counter_sensor, 'interval', seconds=collection_interval)
sched.start()

##Flask Setup

app = Flask(__name__)  # Flask 객체 선언, 파라미터로 어플리케이션 패키지의 이름을 넣어줌.
CORS(app)
api = Api(app)  # Flask 객체에 Api 객체 등록

@api.route('/hello')  # 데코레이터 이용, '/hello' 경로에 클래스 등록
class HelloWorld(Resource):
    def get(self):  # GET 요청시 리턴 값에 해당 하는 dict를 JSON 형태로 반환
        '''
        설명 첫줄입니다
        + 항목 1 
            - 소항목 2
        '''
        return {"hello": "world!"}

@api.route('/api/ksdf/get_all')
class ksdf_get_all(Resource):
    def get(self):
        return kaloom_netconf_get_all()

@api.route('/api/ksdf/all_packet_counters')
class ksdf_all_packet_counters(Resource):
    def get(self):
        return get_ksdf_all_packet_counters()

@api.route('/api/ksdf/all_tp_oper')
class ksdf_all_tp_oper(Resource):
    def get(self):
        return get_ksdf_all_tp_oper()

@api.route('/api/ksdf/nodes_info_oper')
class ksdf_all_nodes_info_oper(Resource):
    def get(self):
        return get_ksdf_all_nodes_info_oper()

@api.route('/api/ksdf/topology/node_link')
class ksdf_topology_node_link(Resource):
    def get(self):
        return get_ksdf_topology_node_link()

#packet_counter_per_tp
@api.route('/api/ksdf/packet_counter/per_tp')
class ksdf_packet_counter(Resource):
    def get(self):
        return {
            "cur_pkt_counter": cur_packet_counter,
            "cur_gcd": cur_gcd, 
            "cur_pkt_rate": cur_gcd_rate 
        }

#telemetry system info
@api.route('/api/ksdf/telemetry/info')
class ksdf_telemetry_info(Resource):
    def get(self):
        return get_ksdf_telemetry_info()

def get_ksdf_telemetry_info(): 
    rpc="""<get><filter type="subtree"><top xmlns="urn:kaloom:faas:fabrics"/><telemetry-system></telemetry-system></filter></get>"""
    return kaloom_netconf_rpc(rpc)['data']['top']['fabrics:telemetry-system']

@api.route('/api/ksdf/telemetry/configure')
class ksdf_telemetry_configure(Resource):
    def post(self):
        '''
        Enable/disable the Kaloom SDF telemetry feature
        + request
            - body format : {"enabled": true | false}
        + response: 
            - {'ok': True} - when properly configured
            - {'ok': False} - something was wrong
        '''
        try:
            json_data=request.get_json()
            enabled=json_data['enabled']
            return set_ksdf_telemetry_configure(enabled)
        except:
            return {"error": "cannot process the request"}

@api.route('/api/ksdf/telemetry/add_flow')
class ksdf_telemetry_add_flow(Resource):
    def post(self):
        '''
        add a telemetry flow for the Kaloom SDF telemetry feature
        + request
            - body format : 
               {"flow_name": name of the flow to register,
                "priority_num": priority number, 
                "ethernet_num": protocol number,
                "sample_percentage": 1 ~ 100 (sampling percentage),
                "cidr": dst ip in the format of x.x.x.x/x
                }
        + response: 
            - {'ok': True} - when properly configured
            - {'ok': False} - something was wrong
        '''
        try:
            json_data=request.get_json()
            flow_name=json_data['flow_name']
            priority_num=json_data['priority_num']
            ethernet_num=json_data['ethernet_num']
            sample_percentage=json_data['sample_percentage']
            cidr=json_data['cidr']
            return set_ksdf_telemetry_add_flow(flow_name, priority_num, ethernet_num, sample_percentage, cidr)
        except:
            return {"error": "cannot process the request"}

def set_ksdf_telemetry_configure(enabled):
    if enabled:
        rpc = """<configure-telemetry-system xmlns="urn:kaloom:faas:fabrics-telemetry">
    <enabled> true </enabled>
    </configure-telemetry-system>"""
    else:
        rpc = """<configure-telemetry-system xmlns="urn:kaloom:faas:fabrics-telemetry">
    <enabled> false </enabled>
    </configure-telemetry-system>"""
    if 'ok' in kaloom_netconf_rpc(rpc):
        return {'ok': True}
    else: 
        return {'ok': False}

def set_ksdf_telemetry_add_flow(flow_name, priority_num, ethernet_num, sample_percentage, cidr):
    rpc="""<configure-telemetry-flow xmlns="urn:kaloom:faas:fabrics-telemetry">
  <name>{flow_name}</name>
  <priority>{prior_num}</priority>
  <ethernet-type>{eth_num}</ethernet-type>
  <destination-address-prefix>{cidr}</destination-address-prefix>
  <exclude-filter>false</exclude-filter>
  <sample-percentage>{sample_perc}</sample-percentage>
</configure-telemetry-flow>""".format(flow_name=flow_name, prior_num=priority_num, cidr=cidr,
                                      eth_num=ethernet_num, sample_perc=sample_percentage)
    try:
        res=kaloom_netconf_rpc(rpc)
        if 'ok' in res: 
            return {'ok': True}
        else: 
            return {'ok': False}
    except:
        print({"error":True})
        return {'error': "something's wrong"}

if __name__ == "__main__":
    #app.run(debug=True, host='192.168.15.131', port=8000)
    app.run(debug=True, host='0.0.0.0', port=8000)

