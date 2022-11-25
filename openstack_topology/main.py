from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS, cross_origin

from opstk_topology import *
from opstk_network_topology import *
###Flask Setup

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

#### topology info
@api.route('/ostck/project/id_name')
class ostck_project_id_name(Resource):
    def get(self):
        """
        get the most basic project info configured on our openstack clusters
        + for the details please refer to 
        https://docs.openstack.org/openstacksdk/latest/user/proxies/identity_v3.html
        """
        return get_ostck_project_id_name()


@api.route('/ostck/topology/servers_on_hosts')
class ostck_topology_servers_on_hosts(Resource):
    def get(self):
        """
        get server info on each compute node
        + for the details please refer to 
        https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/server.html
        """
        return get_ostck_topology_servers_on_hosts()

@api.route('/ostck/topology/server_info')
class ostck_topology_server_info(Resource):
    def get(self):
        """ 
        get detailed info of a server specified by the provided server name or id
        + server id needs be included in the request params like the following
        
            ?server_id=2f70f301-b039-42cc-b043-1ed47011e1a8
        
        + for the details please refer to 
        https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/server.html
        """

        server_id=request.args.get('server_id')
        if not server_id:
            return {"error": "server id not provided"}
        return get_ostck_topology_server_info(server_id)

@api.route('/ostck/topology/hypervisors/detailed_info')
class ostck_topology_hypervisors_detailed_info(Resource):
    def get(self):
        """ 
        get detailed info for the configured hypervisors (compute nodes)
        + for the details please refer to 
        https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/hypervisor.html
        """
        return get_ostck_topology_hypervisors_info(details=True)

@api.route('/ostck/topology/hypervisors/info')
class ostck_topology_hypervisors_info(Resource):
    def get(self):
        """ 
        get info for the configured hypervisors (compute nodes)
        + for the details please refer to 
        https://docs.openstack.org/openstacksdk/latest/user/resources/compute/v2/hypervisor.html
        """
        return get_ostck_topology_hypervisors_info(details=False)

@api.route('/ostck/topology/live_migrate')
class ostck_topology_live_migrate(Resource):
    def post(self):
        """
        live migrate a vm to another host
        - request body example
        {
            "vm_id": "2ae44f46-7f04-4280-87f7-0fdf10f75a29", (required)
            "host": "compute3.forwiz-os.com"(optional)
        }
        """
        try:
            json_data=request.get_json()
            vm_id=json_data['vm_id']
        except:
            return {"error": "no vm_id provided"}
        if 'host' in json_data:
            host=json_data['host']
        else:
            host=None
        res=live_migrate(vm_id, host=host)
        return res

#### network info

@api.route('/ostck/network/ports_on_servers')
class ostck_network_ports_on_servers(Resource):
    def get(self):
        """
        get port-info on each server
        """
        return get_ports_on_servers()

@api.route('/ostck/network/subnets_on_networks')
class ostck_network_subnets_on_networks(Resource):
    def get(self):
        """
        get subnet-info on each network
        """
        return get_subnets_on_networks()

if __name__ == "__main__":
    app.run(debug=True, host='192.168.15.131', port=9000)

