# greeter_client.py 파일 생성
#pip install grpcio
#pip install google
#pip install protobuf
from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

def getOpstAdminToken(address):
    """OpenStack SDK를 사용하기 위해 마스터 서버에서 ('192.168.15.40') 관리자 토큰을 발급받아서 접근할 수 있기 때문에
    해당기능을 통해 토큰을 발급받을 수 있게 했다.GRPC를 통해 발급받는다.

    Args:
        address (string): ex)192.168.15.40:50052  [ipv4:port] openstack SDK를 발급받을 수 있는 grpc접근 주소

    Returns:
        string: openstack sdk admin access token
    """
    channel = grpc.insecure_channel(address)
    print(address)
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='world'))
    token = response.message
    return token

    