#!/usr/bin/env python
#-*- coding:utf-8 -*-

__author__ = 'wan'

import os,sys
import string
import time
import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait

reload(sys)
sys.setdefaultencoding('utf-8')

"""
 关于京东账号登录的测试脚本.
"""

url = 'https://passport.jd.com/new/login.aspx'

#set website username and password text length
username_max_length = 20
username_min_length = 4
passwd_max_length = 20
passwd_min_length = 6

#set username and password
valid_username = "18501185504"
valid_password = "abc!@#"
valid_max_username = "test2016201720182019"
valid_max_password = "2016201720182019test"
valid_min_username = "te_1"
valid_min_password = "abc!@#"

#错误数据
invalid_random_password = ''.join(random.sample(valid_password,len(valid_password)))

#密码错误The input TestData:次数限制
passwd_input_limits_count = 6

#use xpath element
check_element_login_fail = "//div[@class='msg-error']"
check_element_login_success = "//ul/li[@id='ttbar-login']/a[1]"

def login(driver,check_element,username,password):
    driver.get(url)
    driver.implicitly_wait(10)
    assert "京东-欢迎登录" in driver.title
    driver.find_element_by_xpath("//div/input[@id='loginname']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@id='nloginpwd']").send_keys(password)
    driver.find_element_by_xpath("//div/a[@id='loginsubmit']").click()
    print("------------------------------------------------------------------")
    try:
        text = driver.find_element_by_xpath(check_element).text       
        assert text is not None
    except NoSuchElementException:
        print(u"-> 没有定位到元素.请检查测试输入数据或重新定位元素.")
    except:
        text = driver.find_element_by_xpath(check_element).text 
        print(u"-> Test_Input: {0},{1} \n  Test_Run,return: {2} \n  Test_Results_judge: 不符合预期结果,测试失败." \
                     .format(username,password,text))
    else:
        print(u"-> Test_Input: {0},{1} \n  Test_Run,return: {2} \n  Test_Results_judge: 符合预期结果,测试通过." \
                     .format(username,password,text)) 
            
class TestEnvironment(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def tearDown(self):
        self.driver.close()

class TestLogin(TestEnvironment):

    """
    京东自身用户账号
    """
    def test_login_valid(self):
        """ 1. correct username and password. """
        login(self.driver,check_element_login_success,valid_username,valid_password)

    def test_login_valid_max(self):
        """ 2. MaxLength username and password. """
        login(self.driver,check_element_login_success,valid_max_username,valid_max_password)

    def test_login_valid_min(self):
        """ 3. MinLength username and password.  """
        login(self.driver,check_element_login_success,valid_min_username,valid_min_password)
    
    def test_login_empty(self):
        """ 4. Null or Empty """
        empty_user = ""
        empty_passwd = "" 
        login(self.driver,check_element_login_fail,empty_user,empty_passwd)

    @unittest.skip("No Run") 
    def test_login_validuser(self):
        """ 5. Correct username, wrong password. """
        login(self.driver,valid_username,invalid_random_password)

    @unittest.skip("No Run") 
    def test_login_passwd_input_count(self):
        """ 6. 多次输入错误密码，验证错误密码上限. """
        for count in range(passwd_input_limits_count):
            login(self.driver,valid_username,invalid_random_password)

    def test_login_auto(self):
        """ 7. 自动登录功能 """
        pass


class TestLoginCooperationAccount(TestEnvironment):

    """
    合作网站账号登陆，主要有QQ、微信
    """

    def test_login_qq():
        pass

    def test_login_wx():
        pass

    def test_login_jdpay():
        pass


def suite():
    tests = [ 
                "test_login_valid",
                "test_login_valid_max",
                "test_login_valid_min",
                "test_login_empty",
                "test_login_validuser",
                "test_login_passwd_input_count"
            ]
    return unittest.TestSuite(map(TestLogin,tests))

if __name__ == "__main__":
    unittest.TextTestRunner().run(suite())
