import locust
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from realbrowserlocusts import HeadlessChromeLocust
from selenium.webdriver.support.ui import Select
import time
from selenium import webdriver

from locust import TaskSet, task, between
from selenium.webdriver.chrome.options import Options
import greenlet
from tests.random_data_generator import *


class LocustUserBehavior(TaskSet):

    global random_data
    random_data = DataGenerator()
    global register_page

    global search_input

    def on_quit(self):
        self.client.quit()

    def on_teardown(self):
        self.client.quit()

    def on_start(self):
        self.client.maximize_window()

    def goto_register_page(self):
        self.client.get('https://m2.leanscale.com/customer/account/create/')

    def filing_register_form(self):
        firstname_input = self.client.find_element_by_id('firstname')
        firstname_input.send_keys(random_data.firstname_generator())

        lastname_input = self.client.find_element_by_id('lastname')
        lastname_input.send_keys(random_data.lastname_generator())

        email_input = self.client.find_element_by_id('email_address')
        email_input.send_keys(random_data.email_generator())

        password_input = self.client.find_element_by_id('password')
        password_input.send_keys('Leanscale7')

        password_confirmation_input = self.client.find_element_by_id('password-confirmation')
        password_confirmation_input.send_keys('Leanscale7')

    def submit_register_form(self):
        create_button = self.client.find_element_by_xpath('//*[@id="form-validate"]/div/div[1]/button')
        create_button.click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[1]/div[2]/div/div/div')))

    def logout(self):
        self.client.find_element_by_xpath('/html/body/div[1]/header/div[1]/div/ul/li[2]').click()
        self.client.find_element_by_xpath('/html/body/div[1]/header/div[1]/div/ul/li[2]/div/ul/li[3]').click()

    def goto_product_page(self):
        self.client.get('https://m2.leanscale.com/erika-running-short.html')
        self.client.wait.until(EC.visibility_of_element_located((By.ID, 'option-label-color-93-item-5480')))

    def filing_add_to_cart_form(self):
        size = self.client.find_element_by_id('option-label-size-150-item-5599')
        color = self.client.find_element_by_id('option-label-color-93-item-5480')
        size.click()
        color.click()

    def add_to_cart(self):
        add_to_cart_button = self.client.find_element_by_id('product-addtocart-button')
        add_to_cart_button.click()
        self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="maincontent"]/div[1]/div[2]/div/div/div')))


    @task(5)
    def register(self):
        self.client.timed_event_for_locust(
            "1 - Go to",
            "[Register] Register page",
            self.goto_register_page
        )
        time.sleep(1)
        self.client.timed_event_for_locust(
            "2 - Filing",
            "[Register] Register form",
            self.filing_register_form
        )
        time.sleep(1)
        self.client.timed_event_for_locust(
            "3 - Go to",
            "[Register] Account details page",
            self.submit_register_form
        )
        time.sleep(1)
        self.client.timed_event_for_locust(
            "4 - Go to",
            "[Register] Logout",
            self.logout
        )

    @task(5)
    def add_to_cart(self):
        self.client.timed_event_for_locust(
            "1 - Go to",
            "[Add To Cart] Product page",
            self.goto_product_page
        )

        self.client.timed_event_for_locust(
            "2 - Filing",
            "[Add To Cart] Add to cart form",
            self.filing_add_to_cart_form
        )

        self.client.timed_event_for_locust(
            "3 - Submit",
            "[Add To Cart] Add to cart",
            self.add_to_cart
        )

class LocustUser(HeadlessChromeLocust):

    host = "not really used"
    timeout = 360  #in seconds in waitUntil thingies
    min_wait = 60000
    max_wait = 90000
    screen_width = 1350
    screen_height = 850
    task_set = LocustUserBehavior