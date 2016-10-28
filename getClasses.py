
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as EC
import selenium.webdriver.support.ui as ui
from datetime import datetime
from pyvirtualdisplay import Display
from sussedCredentials import getLoginDetails
import os
import time

class HelperFunctions():

    @classmethod
    def is_clickable(cls, driver, locator, timeout=4):
        try:
            ui.WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(locator))
            return True
        except TimeoutException:
            return False

    @classmethod
    def is_visable(cls, driver, locator, timeout=4):
        try:
            ui.WebDriverWait(driver, timeout).until(EC.visibility_of_element_located(locator))
            return True
        except TimeoutException:
            return False

class TimeTableClass():

    @staticmethod
    def try_parsing_date(text):
        for fmt in ('%d/%m/%Y %H:%M:%S', '%d/%m/%Y %H:%M', '%d/%m/%y'):
            try:
                return datetime.strptime(text, fmt)
            except ValueError:
                pass
        raise ValueError('no valid date format found')


    def __init__(self, name, start_time, end_time, location):
        self.name = name
        self.start_time = self.try_parsing_date(start_time)
        self.end_time = self.try_parsing_date(end_time)
        self.location = location

    def __str__(self):
        return self.name + " : starttime :" + self.start_time.toIsoFormat('T')

class LoginPage():

    USERNAME_ELEM = (By.CSS_SELECTOR, 'input.username')
    PASSWORD_ELEM = (By.CSS_SELECTOR, 'input.password')
    LOGIN_ELEM = (By.CSS_SELECTOR, "input[type='submit']")

    def __init__(self, driver):
        self.driver = driver

    def fill_out_login_form(self):
        self.driver.get("https://timetable.soton.ac.uk")
        HelperFunctions.is_clickable(self.driver, self.USERNAME_ELEM)
        login_details = getLoginDetails()
        self.driver.find_element_by_css_selector('input.username').send_keys(login_details["sussed_username"])
        self.driver.find_element_by_css_selector('input.password').send_keys(login_details["password"])
        self.driver.find_element_by_css_selector("input[type='submit']").click()


class TimeTablePage():

    CALENDER_TABLE = (By.ID,'calendarTable')
    NEXT_BUTTON = (By.CSS_SELECTOR, "button.fc-next-button")


    def __init__(self, driver):
        self.driver = driver
        self.class_list = []
        HelperFunctions.is_visable(self.driver, self.CALENDER_TABLE)


    def scrape_classes_data(self, weeks):
        for i in range(weeks):
            number_of_classes = len(self.driver.find_elements_by_css_selector('table.basic tbody tr'))
            for class_number in range(number_of_classes):
                class_finder_string = "//table[contains(@class,'basic')]/tbody/tr[{0}]/td".format(str(class_number + 1))
                table_rows = self.driver.find_elements_by_xpath(class_finder_string)
                class_name = table_rows[1].get_attribute('innerHTML')
                class_start_time = table_rows[3].get_attribute('innerHTML')
                class_end_time = table_rows[4].get_attribute('innerHTML')
                class_location = table_rows[5].get_attribute('innerHTML')
                classObject = TimeTableClass(class_name, class_start_time, class_end_time, class_location)
                self.class_list.append(classObject)
            self.click_next_week()
        return self.class_list

    def click_next_week(self):
        self.driver.find_element_by_css_selector("button.fc-next-button").click()
        time.sleep(4)

def getClasses(weeks):
    driver=""
    display=""
    class_list=[]
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        dir_path = os.path.dirname(os.path.realpath(__file__))
        driver = webdriver.Chrome(dir_path + '/drivers/chromedriverv52')
        loginPage = LoginPage(driver)
        loginPage.fill_out_login_form()
        timeTablePage = TimeTablePage(driver)
        class_list = timeTablePage.scrape_classes_data(weeks)
        return class_list
    except Exception as e:
        return e
    finally:
        driver.quit()
        display.stop()

if __name__ == "__main__":
    print(getClasses(2))
