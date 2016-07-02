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

#QQ
qq = '3485126980'
qq_passwd = '098765!@#'
wx = ''
wx_passwd = ''
            
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

class TestLoginCooperationAccount(TestEnvironment):
    """
    合作网站账号登陆，主要有QQ、微信.
    """
    
    def test_login_qq(self):
        """ TestCase 01: QQ login."""

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
 
    def test_login_wx():
        """  TestCase 02: wx login."""

        pass

    def test_login_jdpay():
        """ TestCase 03: jd wallt login."""

        pass

def suite_cpt():
    tests = [ 
                "test_login_qq"
            ]
    return unittest.TestSuite(map(TestLoginCooperationAccount,tests))

if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite_cpt())
