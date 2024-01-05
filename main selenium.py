# instagram bot for likes
from time import sleep
import random
import yaml
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.common.keys import Keys

#TODO: r_sleep(False)  >> r_sleep()
#TODO: r_sleep(False)  >> r_sleep()


## TODO: Setup check
## TODO: Install selenium
## TODO: Install selenium firefox driver
## TODO: Install selenium firefox on local machine

### Initialize
## Load config

def init():
    # Read config.yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    # Read secrets.yaml
    with open('secrets.yaml', 'r') as f:
        secrets = yaml.safe_load(f)
    config['u'] = secrets['a']
    config['p'] = secrets['z']
    
    return config

def r_sleep(use_default=True):
    """
    Generate a random sleep interval in seconds.

    Parameters:
    - use_default (bool): If True, use the range 3 to 40 seconds. If False, use the range 3 to 5 seconds.

    Returns:
    int: Random sleep interval in seconds.
    """
    if use_default:
        return random.randint(2, 40)
    else:
        return random.randint(2, 4)

class LoginPage:
    def __init__(self, browser):
        """
        Initialize a new LoginPage instance.

        Parameters:
            browser (WebDriver): The Selenium WebDriver instance.

        Returns:
            LoginPage: A new instance of the LoginPage class.
        """
        self.browser = browser

    def login(self, username, password):
        """
        Log in to the application with the provided username and password.

        Parameters:
            username (str): The username to log in with.
            password (str): The password associated with the username.

        Returns:
            MainPage: An instance of the MainPage class representing the main page after a successful login.
        """
        # username_input = self.browser.find_element_by_css_selector("input[name='username']")
        # password_input = self.browser.find_element_by_css_selector("input[name='password']")
        username_input = self.browser.find_element(by='css selector', value="input[name='username']")
        password_input = self.browser.find_element(by='css selector', value="input[name='password']")
        username_input.send_keys(username)
        password_input.send_keys(password)
        # login_button = browser.find_element_by_xpath("//button[@type='submit']")  
        login_button = browser.find_element(by='xpath', value="//button[@type='submit']")
        login_button.click()
        sleep(5)
        r_sleep(False)

        return MainPage(self.browser)

class HomePage:
    def __init__(self, browser):
        """
        Initialize the HomePage object.

        :return: An instance of the HomePage class.
        """
        self.browser = browser
        self.browser.get('https://www.instagram.com/')

        # Bypass cookie notification pop-up
        try:
            self.browser.find_element(by='xpath', value="//button[text()='Allow all cookies']").click()
        except NoSuchElementException as e:
            # assuming we are already at the login page
            print("Warning: NoSuchElementException. No Log //button[text()='Allow all cookies'.")

    def go_to_login_page(self):
        """
        Navigate to the login page. Find a element / hyperlink to the 'Log in' page. 

        :return: An instance of the LoginPage class.
        """
        # self.browser.find_element_by_xpath("//a[text()='Log in']").click()
        try:
            self.browser.find_element(by='xpath', value="//a[text()='Log in']").click()
            sleep(2)
        except NoSuchElementException as e:
            try:
                self.browser.find_element(by='xpath', value="//button[@type='submit']")
                print("Warning: NoSuchElementException. No Log in link found. Did encounter a WebElement button with text 'Log in'")
            except:
                pass # assuming we are already at the login page   

        return LoginPage(self.browser)

class MainPage:
    def __init__(self, browser):
        """
        Initialize the MainPage object. Suppress the default notification pop-ups that might block click() on other elements).

        :param browser: The Selenium WebDriver instance.
        """
        self.browser = browser
        print("+ On main page...")
        
        # Bypass 'Save your login info?' pop-up
        try:
            self.browser.find_element(by='xpath', value="//button[text()='Save info']").click()
            sleep(2)
        except NoSuchElementException as e:
            # assuming we are already at the correct page
            print("Warning: NoSuchElementException. No Log //button[text()='Save info'.")

        # Turn off notifications pop-up
        try:
            self.browser.find_element(by='xpath', value="//button[text()='Not Now']").click()
            sleep(2)
        except NoSuchElementException as e:
            # assuming we are already at the correct page
            print("Warning: NoSuchElementException. No Log //button[text()='Not Now'.")
    
    def scroll_down(self):
        """
        Scrolls down the main page by sending the 'END' key to the body element,
        sleeps for a random duration, and then sends the 'HOME' key to reset.

        Args:
            self: The object instance.

        Returns:
            None
        """
        body_elem = self.browser.find_element(by='tag name', value='body')
        for _ in range(2):
            body_elem.send_keys(Keys.END)
            sleep(r_sleep(False))
            body_elem.send_keys(Keys.HOME)
    
    def like(self):
        """
        Likes elements on the main page based on a specified class ID.

        Returns a list of elements that were liked.

        Args:
            self: The object instance.

        Returns:
            list: A list of elements that were liked.
        """
        like_class_id = "x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81"
        value = f"//div[contains(@class, \"{like_class_id}\")]"
        
        try:
            hearts = self.browser.find_elements(by='xpath', value=value)
        except NoSuchElementException as e:
            # assuming we are already at the login page
            print("Warning: NoSuchElementException. Not found : '{value}'")

        for i, heart in enumerate(hearts):
            try:
                heart.click()
                print(f"{i} / {len(hearts)}")
                sleep(r_sleep(False))
            except ElementClickInterceptedException as e:
                print(e)

        return hearts


        # Outer HTML for Like button
        # <div class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81" 
        # role="button" tabindex="0"><div class="x6s0dn4 x78zum5 xdt5ytf xl56j7k"><span class=""><svg aria-label="Like" class="x1lliihq x1n2onr6 xyb1xck" fill="currentColor" height="24" role="img" viewBox="0 0 24 24" width="24"><title>Like</title><path d="M16.792 3.904A4.989 4.989 0 0 1 21.5 9.122c0 3.072-2.652 4.959-5.197 7.222-2.512 2.243-3.865 3.469-4.303 3.752-.477-.309-2.143-1.823-4.303-3.752C5.141 14.072 2.5 12.167 2.5 9.122a4.989 4.989 0 0 1 4.708-5.218 4.21 4.21 0 0 1 3.675 1.941c.84 1.175.98 1.763 1.12 1.763s.278-.588 1.11-1.766a4.17 4.17 0 0 1 3.679-1.938m0-2a6.04 6.04 0 0 0-4.797 2.127 6.052 6.052 0 0 0-4.787-2.127A6.985 6.985 0 0 0 .5 9.122c0 3.61 2.55 5.827 5.015 7.97.283.246.569.494.853.747l1.027.918a44.998 44.998 0 0 0 3.518 3.018 2 2 0 0 0 2.174 0 45.263 45.263 0 0 0 3.626-3.115l.922-.824c.293-.26.59-.519.885-.774 2.334-2.025 4.98-4.32 4.98-7.94a6.985 6.985 0 0 0-6.708-7.218Z"></path></svg></span></div></div>

        # <div class="x1i10hfl x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x6s0dn4 xjbqb8w x1ejq31n xd10rxx x1sy0etr x17r0tee x1ypdohk x78zum5 xl56j7k x1y1aw1k x1sxyh0 xwib8y2 xurb0ha xcdnw81" 
# def test_login_page(browser):
#     home_page = HomePage(browser)
#     login_page = home_page.go_to_login_page()
#     login_page.login("<your username>", "<your password>")

#     errors = browser.find_elements_by_css_selector('#error_message')
#     assert len(errors) == 0

# if __name__ == "main":
config = init()
# Ensure UI button languages and input fields are in en-US
options = Options()
options.set_preference('intl.accept_languages', 'en-US, en')
browser = webdriver.Firefox(options=options)

browser.implicitly_wait(5)

home_page = HomePage(browser)
login_page = home_page.go_to_login_page()
# login_page.login(config['u'], config['p'])
main_page = login_page.login(config['u'], config['p'])
main_page.scroll_down()
main_page.like()

# browser.close()