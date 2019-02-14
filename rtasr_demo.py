#-*- encoding:utf-8 -*-

import sys
import hashlib
from hashlib import sha1
import hmac
import base64
from socket import *
import json, time, threading
import websocket
from websocket import create_connection
from urllib import quote
import logging
from get_audio import get_audio,in_path
reload(sys)
sys.setdefaultencoding("utf8")
logging.basicConfig()

base_url = "ws://rtasr.xfyun.cn/v1/ws"
app_id = "5c5e86b7"
api_key = "bade857aa9af069ba205cd1c3bd679e4"
#get_audio()
file_path = "./input.wav"#test_1.pcm

end_tag = "{\"end\": true}"

class Client():
    def __init__(self):
        # 生成鉴权参数
        ts = str(int (time.time()))
        tmp = app_id + ts
        hl = hashlib.md5()
        hl.update(tmp.encode(encoding='utf-8'))
        my_sign = hmac.new(api_key,  hl.hexdigest(), sha1).digest()
        signa = base64.b64encode(my_sign)

        self.ws = create_connection(base_url + "?appid=" + app_id + "&ts=" + ts + "&signa=" + quote(signa))
        self.trecv = threading.Thread(target=self.recv)
        self.trecv.start()

    def send(self, file_path):
        file_object = open(file_path, 'rb')
        try:
            index = 1
            while True:
                chunk = file_object.read(1280)
                if not chunk:
                    break
                self.ws.send(chunk)

                index += 1
                time.sleep(0.04)
        finally:
            # print str(index) + ", read len:" + str(len(chunk)) + ", file tell:" + str(file_object.tell())
            file_object.close()

        self.ws.send(bytes(end_tag))
        print "send end tag success"

    def recv(self):
        try:
            while self.ws.connected:
                result = str(self.ws.recv())
                if len(result) == 0:
                    print "receive result end"
                    break
                """

                """
                result_dict = json.loads(result)

                # 解析结果
                if result_dict["action"] == "started":
                    print "handshake success, result: " + result

                if result_dict["action"] == "result":
                    #解析json串:从复杂的json串中取出识别的片段
                    data_string = []
                    data_result = json.loads(result_dict["data"])["cn"]["st"]["rt"][0]["ws"]
                    for string_cut in data_result:
                        data_string.append(string_cut["cw"][0]["w"])
                    print ("rtasr result: "),
                    print ''.join(data_string[:-1])

                if result_dict["action"] == "error":
                    print "rtasr error: " + result
                    self.ws.close()
                    return
        except websocket.WebSocketConnectionClosedException:
            print "receive result end"

    def close(self):
        self.ws.close()
        print "connection closed"

if __name__ == '__main__':
    get_audio(in_path)
    client = Client()
    client.send(file_path)