from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
from google.protobuf import json_format

client = client.Client(url='http://10.10.130.10:80',
                       username='thai',
                       password='3522175567')
mission = client.get_mission(3)
print(json_format.MessageToJson(mission))
