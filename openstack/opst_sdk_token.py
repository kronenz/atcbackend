# greeter_client.py 파일 생성

from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    channel = grpc.insecure_channel('192.168.15.40:50056')
    stub = helloworld_pb2_grpc.GreeterStub(channel)
    response = stub.SayHello(helloworld_pb2.HelloRequest(name='world'))
    print("Greeter client received: " + response.message)


if __name__ == '__main__':
    run()