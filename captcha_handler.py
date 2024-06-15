from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
    NoSuchElementException,
    InvalidArgumentException
)
import time
import requests
import os
from dotenv import load_dotenv

load_dotenv()
from twocaptcha import TwoCaptcha

# Initialize 2Captcha Solver with your API key
solver = TwoCaptcha(os.getenv("_2captcha_api_key"))

class CaptchaHandler:
    def __init__(self, driver, session: requests.Session):
        self.driver = driver
        self.session = session
        self._2captcha_api_key = os.getenv("_2captcha_api_key")

    def detect_captcha(self):
        # Google ReCAPTCHA v2/v3
        recaptcha_v2 = "g-recaptcha"
        recaptcha_v3 = "g-recaptcha-response"
        if (
                len(self.driver.find_elements(By.CSS_SELECTOR, f"[class^='{recaptcha_v2}']")) > 0
                or len(self.driver.find_elements(By.NAME, f"[class^='{recaptcha_v3}']")) > 0
                or len(self.driver.find_elements(By.ID, f"[id^='{recaptcha_v2}']")) > 0
                or len(self.driver.find_elements(By.ID, f"[id^='{recaptcha_v3}']")) > 0
        ):
            return "Google ReCAPTCHA v2/v3"

        # hCaptcha
        hcaptcha = "h-captcha-response"
        if len(self.driver.find_elements(By.NAME, hcaptcha)) > 0:
            return "hCaptcha"

        # Solve Media
        solvemedia = "AC_Click"
        if len(self.driver.find_elements(By.CLASS_NAME, solvemedia)) > 0:
            return "Solve Media"

        # Recapthca Mailhide
        recaptcha_mailhide = "recaptcha_challenge_field"
        if len(self.driver.find_elements(By.NAME, recaptcha_mailhide)) > 0:
            return "Recapthca Mailhide"

        # KeyCAPTCHA
        keycaptcha = "keycaptcha_div_select"
        if len(self.driver.find_elements(By.ID, keycaptcha)) > 0:
            return "KeyCAPTCHA"

        # reCAPTCHA Mailhide
        recaptcha_mailhide = "recaptcha_response_field"
        if len(self.driver.find_elements(By.NAME, recaptcha_mailhide)) > 0:
            return "reCAPTCHA Mailhide"

        # BotDetect Captcha
        botdetect = "BDC_VC"
        if len(self.driver.find_elements(By.ID, botdetect)) > 0:
            return "BotDetect Captcha"

        # JCaptcha
        jcaptcha = "jcaptcha"
        if len(self.driver.find_elements(By.ID, jcaptcha)) > 0:
            return "JCaptcha"

        # Secure image CAPTCHA
        secure_image_captcha = "siimage"
        if len(self.driver.find_elements(By.ID, secure_image_captcha)) > 0:
            return "Secure image CAPTCHA"

        # math CAPTCHA
        math_captcha = "math_captcha_input"
        if len(self.driver.find_elements(By.NAME, math_captcha)) > 0:
            return "math CAPTCHA"

        # text CAPTCHA
        text_captcha = "text_captcha_input"
        if len(self.driver.find_elements(By.NAME, text_captcha)) > 0:
            return "text CAPTCHA"

        # picture puzzle CAPTCHA
        picture_puzzle_captcha = "picture_puzzle_captcha"
        if len(self.driver.find_elements(By.CLASS_NAME, picture_puzzle_captcha)) > 0:
            return "picture puzzle CAPTCHA"

        # geo-location CAPTCHA
        geo_location_captcha = "geo_location_captcha"
        if len(self.driver.find_elements(By.ID, geo_location_captcha)) > 0:
            return "geo-location CAPTCHA"

        # time-based CAPTCHA
        time_based_captcha = "time_based_captcha"
        if len(self.driver.find_elements(By.ID, time_based_captcha)) > 0:
            return "time-based CAPTCHA"

        # question and answer CAPTCHA
        question_answer_captcha = "question_answer_captcha"
        if len(self.driver.find_elements(By.ID, question_answer_captcha)) > 0:
            return "question and answer CAPTCHA"

        # honeypot CAPTCHA
        honeypot_captcha = "honeypot_captcha"
        if len(self.driver.find_elements(By.ID, honeypot_captcha)) > 0:
            return "honeypot CAPTCHA"

        # slider CAPTCHA
        slider_captcha = "slider_captcha"
        if len(self.driver.find_elements(By.ID, slider_captcha)) > 0:
            return "slider CAPTCHA"

        # checkbox CAPTCHA
        checkbox_captcha = "checkbox_captcha"
        if len(self.driver.find_elements(By.ID, checkbox_captcha)) > 0:
            return "checkbox CAPTCHA"

        # audio CAPTCHA
        audio_captcha = "audio_captcha"
        if len(self.driver.find_elements(By.ID, audio_captcha)) > 0:
            return "audio CAPTCHA"

        return False

    def solve_captcha(self):
        # print(f"Solving {captcha}...")

        try:
            # sitekey_elements = self.driver.find_elements(By.XPATH, "//*[@data-sitekey]")
            #
            # if len(sitekey_elements) == 0:
            #     print('No visible CAPTCHA found.')
            #
            # sitekey = ''
            # for sitekey_element in sitekey_elements:
            #     try:
            #         sitekey = sitekey_element.get_attribute("data-sitekey")
            #         if sitekey:
            #             break
            #     except Exception:
            #         pass
            # if not sitekey:
            #     # Get the sitekey from the iframe src
            #     try:
            #         sitekey = \
            #             self.driver.find_element(By.CSS_SELECTOR, "[class^='g-recaptcha']").get_attribute(
            #                 "src").split("k=")[
            #                 1].split("&")[0]
            #     except Exception:
            #         pass
            #
            # if not sitekey:
            #     return False

            # Get the page url
            page_url = self.driver.current_url

            # http://2captcha.com/in.php?key=1abc234de56fab7c89012d34e56fa7b8&method=userrecaptcha&googlekey=6Le-wvkSVVABCPBMRTvw0Q4Muexq1bi0DJwx_mJ-&pageurl=http://mysite.com/page/with/recaptcha

            # Get the captcha id
            result = solver.turnstile(
                sitekey='0x4aaaaaaadnpidrormt1wwj',
                url=page_url,
            )
            print(result)
            return
            captcha_response = self.session.get(
                f"http://2captcha.com/in.php?key={self._2captcha_api_key}&method=TurnstileTaskProxyless&websiteKey={'6aac8896f227'}&websiteURL={page_url}",
                timeout=20).text
            captcha_id = captcha_response.split("|")[1]

            # Wait for the captcha to be solved
            times_checked = 0
            while times_checked < 12:
                print("SOLVING CAPTCHA")
                time.sleep(5)
                captcha_response = self.session.get(
                    f"http://2captcha.com/res.php?key={self._2captcha_api_key}&action=get&id={captcha_id}",
                    timeout=20).text
                times_checked += 1
                if captcha_response.split("|")[0] == "OK":
                    print("SOLVED CAPTCHA")
                    break

            # Get the captcha solution
            captcha_solution = captcha_response.split("|")[1]

            # Submit the captcha solution
            self.driver.execute_script(
                f"document.getElementById('g-recaptcha-response').innerHTML = '{captcha_solution}';")
            self.driver.execute_script("document.getElementById('g-recaptcha-response').style.display = 'block';")
            self.driver.execute_script(
                "document.getElementById('g-recaptcha-response').style.visibility = 'visible';")
            self.driver.execute_script("document.getElementById('g-recaptcha-response').style.opacity = '1';")
            self.driver.execute_script("document.getElementById('g-recaptcha-response').style.height = 'auto';")
            self.driver.execute_script("document.getElementById('g-recaptcha-response').style.width = 'auto';")

            print("Captcha solved successfully!")

        except Exception as err:
            print(err)
