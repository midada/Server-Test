#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os,sys
import string
import time
import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

reload(sys)
sys.setdefaultencoding('utf-8')

url = 'https://passport.jd.com/new/login.aspx'

#set website username and password text length
username_max_length = 20
username_min_length = 4
passwd_max_length = 20
passwd_min_length = 4

#set username and password
valid_username = " "
valid_password = " "
valid_max_username = " "
valid_max_password = " "
valid_min_username = " "
valid_min_password = " "

#错误数据
invalid_random_password = ''.join(random.sample(valid_password,len(valid_password)))

#密码错误The input TestData:次数限制
passwd_input_limits_count = 6

def login(driver,username,password):
    driver.get(url)
    assert "京东-欢迎登录" in driver.title
    driver.find_element_by_xpath("//div/input[@id='loginname']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@id='nloginpwd']").send_keys(password)
    driver.find_element_by_xpath("//div/a[@id='loginsubmit']").click()
    
    try:
        #get nickname
        nickname = driver.find_element_by_xpath("//ul/li[@id='ttbar-login']/a[1]").text
        print("您成功登陆京东账户,您的昵称为：{0}".format(nickname))        
    except:
        msg = driver.find_element_by_xpath("//div[@class='msg-error']").text    
        if msg is not None:
            print(msg)
            
class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def setDown(self):
        self.driver.close()

class TestLogin(TestEnvironment):

    def test_login_valid(self):
        """ 1. correct username and password. """
        login(self.driver,valid_username,valid_password)

    def test_login_valid_max(self):
        """ 2. MaxLength username and password. """
        login(self.driver,valid_max_username,valid_max_password)

    def test_login_valid_min(self):
        """ 3. MinLength username and password.  """
        login(self.driver,valid_min_username,valid_min_password)
        
    def test_login_empty(self):
        """ 4. Null or Empty """
        username,password = " "," "
        login(self.driver,username,password)

    def test_login_validuser(self):
        """ 5. Correct username, wrong password. """
        login(self.driver,valid_username,invalid_random_password)

    def test_login_passwd_input_count(self):
        """ 6. 多次输入错误密码，验证错误密码上限. """
        for count in range(passwd_input_limits_count):
            login(self.driver,valid_username,invalid_random_password)

if __name__ == "__main__":
    unittest.main()
