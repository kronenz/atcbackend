from flask import Flask, request  # 서버 구현을 위한 Flask 객체 import
from flask_restx import Api, Resource  # Api 구현을 위한 Api 객체 import
from flask_cors import CORS, cross_origin

from opstk_topology import *

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

@api.route('/ostck/topology/servers_on_hosts')
class get_ostck_topology_servers_on_hosts(Resource):
    def get(self):
        return ostck_topology_servers_on_hosts()
        
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9000)

