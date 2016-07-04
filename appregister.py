#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import sys
import random
import json
import requests

"""
中国手机号段说明：
    1.中国移动：19个号段; 其中 147为中国移动上网卡号段
    2.中国联通：9个号段; 145为中国联通上网卡号段
    3.中国电信：6个号段; 包括中国电信1349号段（1349 为卫星手机卡）
    4.170、171为虚拟运营商
"""

telec = [134,135,136,137,138,139,150,151,152,157,158,159,182,183,187,188,147,184,178,
        130,131,132,155,156,176,185,186,145,
        133,153,180,181,189,177,
        170,171]

area_number = [ '%04d' % an for an in range(10000) ]
user_number = '8888'

#定义URL
firstregister_url = 'http://114.113.126.8:81/api/v3/firstregister/common/'
firstregister_data = { 
                        "identifyingcode": "1234",
                        "phonenumber": "13921788889"
                    }
register_url = 'http://114.113.126.8:81/api/v3/register/common/'
register_data = {
                    "nickname": "mobile77744s",
                    "password": "a123456",
                    "phonenumber": "13921718889"
                }


def interface_test(url,data):
    json_data = json.dumps(data)
    headers = {"Connection":"keep-alive","Allow":"POST,OPTIONS","Content-Type":"application/json"}
    try:
        print('\n',json_data)
        request = requests.post(url,data=json_data,headers=headers)
    except requests.ConnectionError:
        raise requests.ConnectionError
        print(request.status_code) 
    return json.loads(request.text)

#存放失败的数据
mobile_registration_failed = []
nickname_registration_failed = []

for tc in telec:
    for area in area_number:
        mobile = str(tc) + str(area) + user_number
        try:
            #第一步：输入手机号、验证码、密码
            firstregister_data['phonenumber'] = mobile
            rep_firstregister = interface_test(firstregister_url,firstregister_data)
            print(rep_firstregister)

            if rep_firstregister["state"] == 1:
                #第二步：输入昵称
                nickname = 'test' + str(mobile)
                register_data['nickname'] = nickname
                register_data['phonenumber'] = mobile
                rep_register = interface_test(register_url,register_data)
                print(rep_register,)

                if rep_register["state"] == 1:
                    print("{0} registration successful.".format(mobile))
                else:
                    print("{0} registration Failed".format(mobile))
            else:
                print("{0} Firestregistration Failed".format(mobile))
                #使用列表记录所有注册失败的用户
                mobile_registration_failed.append(mobile)
                with open("mobile_registration_failed.txt",'a+') as f:
                    f.write(mobile +"\n")               
        except:
            print(" Please check.")

    print("注册失败的用户有: {0} 个.".fromat(len(mobile_registration_failed)))

#输出
print(mobile_registration_failed)
