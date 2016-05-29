#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import random
import json
import requests

# set telecom operators: Network identification number
# 中国移动：19个号段 中国联通：9个号段 中国电信：6个号段
# 其中 147为中国移动上网卡号段，145为中国联通上网卡号段
# 不包括中国电信1349号段（1349 为卫星手机卡）
# 170、171为虚拟运营商
telec = [134,135,136,137,138,139,150,151,152,157,158,159,182,183,187,188,147,184,178,
        130,131,132,155,156,176,185,186,145,
        133,153,180,181,189,177,
        170,171]
area_number = [ '%04d' % an for an in range(10000) ]
user_number = '8888'

#定义URL
firstregister_url = 'http://127.0.0.1/api/v3/firstregister/common/'
firstregister_data = { 
                        "identifyingcode": "1234",
                        "phonenumber": "13921788889"
                    }
register_url = 'http://127.0.0.1/api/v3/register/common/'
register_data = {
                    "nickname": "mobile77744s",
                    "password": "a123456",
                    "phonenumber": "13921718889"
                }


def interface_test(url,data):
    json_data = json.dumps(data)
    headers = {"Connection":"keep-alive","Allow":"POST,OPTIONS","Content-Type":"application/json"}
    request = requests.post(url,data=json_data,headers=headers)
    page = json.loads(request.text)
    return page

#存放失败的数据
mobile_registration_failed = []
nickname_registration_failed = []

for tc in telec:
    for area in area_number:
        mobile = str(tc) + str(area) + user_number
        try:
            firstregister_data['phonenumber'] = mobile
            rep_firstregister = interface_test(firstregister_url,firstregister_data)
            print(rep_firstregister)

            if rep_firstregister["state"] == 1:
                nickname = 'test' + str(mobile)
                register_data['nickname'] = nickname
                register_data['phonenumber'] = mobile
                print(register_data)
                rep_register = interface_test(register_url,register_data)

                if rep_register["state"] == 1:
                    print("{0} registration successful.".format(mobile))
                else:
                    print("{0} registration Failed".format(mobile))
            else:
                print("{0} Firestregistration Failed".format(mobile))
                mobile_registration_failed.append(mobile)
        except requests.ConnectionError:
            print("Possible network error. Please check.")

#输出
print(mobile_registration_failed)
