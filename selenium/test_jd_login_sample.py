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

#QQ
qq = '3485126980'
qq_passwd = '098765!@#'
wx = ''
wx_passwd = ''

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

    # TestCase 01: Correct username and password.
    def test_login_valid(self):
        print("1. correct username and password.")
        login(self.driver,check_element_login_success,valid_username,valid_password)
   
    # TestCase 02: Correct MaxLength username, Correct MaxLength password.
    def test_login_valid_max(self):
        print("2. MaxLength username and password.")
        login(self.driver,check_element_login_success,valid_max_username,valid_max_password)
    
    # TestCase 03: Correct MinLength username, MinLengthpassword.
    def test_login_valid_min(self):
        print("3. MinLength username and password.")
        login(self.driver,check_element_login_success,valid_min_username,valid_min_password)
    
    # TestCase 04: 多次输入错误密码，验证错误密码上限.
    #@unittest.skip("No Run") 
    def test_login_passwd_input_count(self):
        print("6. 多次输入错误密码，验证错误密码上限.")
        for count in range(passwd_input_limits_count):
            login(self.driver,check_element_login_fail,valid_username,invalid_random_password)
            self.driver.refresh()

    # TestCase 05: Null or Empty.
    def test_login_empty(self):
        print("4. Null or Empty.")
        empty_user = ""
        empty_passwd = "" 
        login(self.driver,check_element_login_fail,empty_user,empty_passwd)

    # TestCase 06: Correct username, wrong password.
    def test_login_validuser(self):
        print("5. Correct username, wrong password.")
        login(self.driver,check_element_login_fail,valid_username,invalid_random_password)


    # TestCase 07: WebStie LoginPage, AutoLogin checkbox.
    def test_login_auto(self):
        print("7. Auto login Test.")
        login(self.driver,check_element_login_success,valid_username,valid_password)
        #self.driver.find_element_by_xpath("//div/span[1]/input[@id='autoLogin']").is_enabled()

class TestLoginCooperationAccount(TestEnvironment):
    """
    合作网站账号登陆，主要有QQ、微信.
    """
    
    # TestCase 01: QQ login
    def test_login_qq(self):
        driver = self.driver
        driver.find_element_by_xpath("//ul/li[2]/a").click()

        driver.switch_to_window(driver.window_handles[0])
        driver.switch_to.frame(0)
        driver.find_element_by_xpath("//div[@id='bottom_qlogin']//a[@id='switcher_plogin']").click()
        driver.find_element_by_xpath("//div[@class='inputOuter']/input[@id='p']").send_keys(qq_passwd)
        driver.find_element_by_xpath("//div[@class='inputOuter']/input[@id='u']").send_keys(qq)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath("//div[@class='submit']/a/input[@id='login_button']").click()
        time.sleep(5)
 
    # TestCase 02: wx login
    def test_login_wx():
        pass

    # TestCase 03: jd wallt login
    def test_login_jdpay():
        pass


def suite():
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

def suite_1():
    tests = [ 
                "test_login_qq"
            ]
    return unittest.TestSuite(map(TestLoginCooperationAccount,tests))

if __name__ == "__main__":
    #unittest.TextTestRunner().run(suite())
    unittest.TextTestRunner().run(suite_1())
