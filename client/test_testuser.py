from auvsi_suas.client import client
from auvsi_suas.proto import interop_api_pb2
import json
from google.protobuf import json_format

client = client.Client(url='http://localhost:8000',
                       username='testuser',
                       password='testpass')
mission = client.get_mission(2)
print(json_format.MessageToJson(mission))
# print (mission)
