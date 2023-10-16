from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from create_proxy.models import User,JobPost
from create_proxy.views import home
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.urls import reverse,resolve
import time

#
# class TestHome(StaticLiveServerTestCase):
#
#     def setUp(self):
#         self.browser = webdriver.Chrome('functional_tests/chromedriver.exe')
#
#     def tearDown(self):
#         self.browser.close()
#
#
#     def test_home(self):
#         self.browser.get(self.live_server_url)


class LoginFormTest(StaticLiveServerTestCase):

    def testform(self):
        driver=webdriver.Chrome('functional_tests/chromedriver.exe')

        driver.get('http://localhost:8000/signin')
        user_name=driver.find_element_by_name('username')
        user_password=driver.find_element_by_name('password')
        submit = driver.find_element_by_id('submit')
        user_name.send_keys('shirke@gmail.com')
        user_password.send_keys('1234')

        time.sleep(30)
        submit.send_keys(Keys.RETURN)

        url =reverse('home')
        self.assertEquals(resolve(url).func,home)


