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
from selenium.webdriver.common import action_chains as action

reload(sys)
sys.setdefaultencoding('utf-8')

"""关于京东账号登录的测试脚本."""

#set website url
url = 'https://passport.jd.com/new/login.aspx'

#set website username and password text length
username_max_length = 20
username_min_length = 4
passwd_max_length = 20
passwd_min_length = 6

#set correct username and password
valid_username = ""
valid_password = ""
valid_max_username = ""
valid_max_password = ""
valid_min_username = ""
valid_min_password = ""

#set the wrong date 
invalid_random_password = ''.join(random.sample(valid_password,len(valid_password)))

#输入密码错误次数限制
passwd_input_limits_count = 6

#use xpath element
check_element_login_fail = "//div[@class='msg-error']"
check_element_login_success = "//ul/li[@id='ttbar-login']/a[1]"


def login(driver,check_element,username,password):
    driver.implicitly_wait(3)
    assert "京东-欢迎登录" in driver.title
    driver.find_element_by_xpath("//div/input[@id='loginname']").send_keys(username)
    driver.find_element_by_xpath("//div/input[@id='nloginpwd']").send_keys(password)

    auto_login = driver.find_element_by_xpath("//div/span[1]/input[@id='autoLogin']")
    if auto_login.is_selected() != 1:
            auto_login.click()

    driver.find_element_by_xpath("//div/a[@id='loginsubmit']").click()

    print("------------------------------------------------------------------")

    try:
        e_text = driver.find_element_by_xpath(check_element).text      
        assert e_text is not None
    except NoSuchElementException:
        print(u"-> 没有定位到元素.请检查测试输入或重新定位元素.\n")
    except:
        f_text = driver.find_element_by_xpath(check_element).text 
        print(u" Test_Input:{0},{1} \n Test_Run,return:{2} \n Test_Results_judge: 不符合预期结果,测试失败.\n" \
            .format(username,password,f_text))
    else:
        print(u" Test_Input:{0},{1} \n Test_Run,return:{2} \n Test_Results_judge: 符合预期结果,测试通过.\n" \
            .format(username,password,e_text)) 

            
class TestEnvironment(unittest.TestCase):
    """ Test Environment
        1) set Browser driver. 
        2) RunTest after,close browser
    """

    def setUp(self):
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver')
        self.driver = webdriver.Chrome('/Applications/Google Chrome.app/Contents/MacOS/chromedriver')
        self.driver.get(url)

    def tearDown(self):
        self.driver.close()

class TestLogin(TestEnvironment):
    """Test Scenario: On jd account of the Software Testing."""

    def test_login_valid(self):
        """ TestCase 01: Correct username and password."""
        login(self.driver,check_element_login_success,valid_username,valid_password)
   
    def test_login_valid_max(self):
        """ TestCase 02: Correct MaxLength username, Correct MaxLength password."""
        login(self.driver,check_element_login_success,valid_max_username,valid_max_password)
    
    def test_login_valid_min(self):
        """ TestCase 03: Correct MinLength username, MinLengthpassword."""
        login(self.driver,check_element_login_success,valid_min_username,valid_min_password)
  
    #@unittest.skip("No Run") 
    def test_login_passwd_input_count(self):
        """ TestCase 04: 多次输入错误密码，验证错误密码上限."""
        for count in range(passwd_input_limits_count):
            login(self.driver,check_element_login_fail,valid_username,invalid_random_password)
            self.driver.refresh()

    def test_login_empty(self):
        """ TestCase 05: Null or Empty."""
        empty_user = ""
        empty_passwd = "" 
        login(self.driver,check_element_login_fail,empty_user,empty_passwd)

    def test_login_validuser(self):
        """ TestCase 06: Correct username, wrong password."""
        login(self.driver,check_element_login_fail,valid_username,invalid_random_password)

    def test_login_auto(self):
        """ TestCase 07: WebStie LoginPage, AutoLogin checkbox."""
        login(self.driver,check_element_login_success,valid_username,valid_password)
        #self.driver.find_element_by_xpath("//div/span[1]/input[@id='autoLogin']").is_enabled()

#组织测试用例
def suite_jd():
    tests = [ 
                "test_login_valid",
                "test_login_valid_max",
                "test_login_valid_min",
                "test_login_empty",
                "test_login_validuser",
                "test_login_passwd_input_count",
                "test_login_auto"
            ]
    return unittest.TestSuite(map(TestLogin,tests))

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_jd())
