import os
import json
import random
from bs4 import BeautifulSoup
import requests_html
from requests_html import HTMLSession, AsyncHTMLSession, HTML
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
from seleniumbase import Driver
from selenium.webdriver import Chrome
import time
import pandas as pd
from fake_useragent import UserAgent


class WebHandler:
    def __init__(self, url: str, driver: Driver):
        self.driver: Driver = driver
        self.session = HTMLSession()
        self.blocked_urls = []
        self.soup: BeautifulSoup = None
        self.url = url
        self.page_source = None
        self.article: BeautifulSoup = None
        self.actions = ActionChains(self.driver)

    @classmethod
    def initialize_driver(cls):
        try:
            print("Initializing Driver")
            # options = uc.ChromeOptions()
            ua = UserAgent()
            return Driver(
                browser="chrome",
                uc=True,
                headless2=False,
                incognito=True,
                agent=ua.random,
                do_not_track=True,
                undetectable=True
            )
        except Exception as err:
            print(err)

    @staticmethod
    def change_driver_user_agent(driver: Driver):
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": UserAgent().random})
        return driver

    def set_article(self):
        self.article = self.soup.find('article')

    def scroll_website(self, pixels='1000'):
        print(f"SCROLLING WEBSITE BY {pixels} PIXELS")
        # Scroll down by 1000 pixels
        self.driver.execute_script(f"window.scrollBy(0, {pixels});")

    def perform_mouse_movement(self):
        print("PERFORMING MOUSE MOVEMENTS...")
        try:
            self.actions.move_by_offset(random.randint(-100, 100), random.randint(-100, 100)).perform()

            time.sleep(random.randrange(2, 6))
            # Locate an element to move to
            elements_to_hover_over = self.driver.find_elements(By.TAG_NAME, "span")
            if not elements_to_hover_over:
                return

            element_to_hover_over = random.choice(elements_to_hover_over)

            # Move to the element
            self.actions.move_to_element(element_to_hover_over).perform()
        except Exception as err:
            print(err)

    def initialize_soup_from_page_source(self):
        print("Initializing BeautifulSoup")
        try:
            self.soup = BeautifulSoup(self.page_source, "lxml")
        except Exception as err:
            print(f"THERE WAS AN ERROR ==> {err}")

    def fetch_url(self):
        try:
            print("FETCHING ==> ", self.url)
            self.driver.get(self.url)
            # Wait for security check
            print("WAITING FOR SECURITY CHECK")
            time.sleep(10)
            # print(self.driver.page_source)
            WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[@id="content"]')))
            WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//input[@type="checkbox"]')))

        except Exception as err:
            pass

    def set_url_page_source(self):
        print("SETTING WEBSITE PAGE SOURCE")
        try:
            self.page_source = self.driver.page_source.lower()
        except Exception as err:
            print(f"THERE WAS AN ERROR ==> {err}")

    def get_title(self) -> str:
        try:
            if self.article is None:
                return ''

            title_element = self.article.find('h1', attrs={"property": "name"})
            if title_element is None:
                return ''
            return title_element.get_text()
        except Exception:
            return ''

    def get_author(self) -> dict:
        try:
            author_element = self.article.find('span', attrs={"property": "author"})
            first_name_element = author_element.find('span', attrs={"property": "givenName".lower()})
            last_name_element = author_element.find('span', attrs={"property": "familyName".lower()})

            author_info = {}
            if first_name_element:
                author_info["first_name"] = first_name_element.get_text()

            if last_name_element:
                author_info["last_name"] = last_name_element.get_text()

            print("author_info ==> ", author_info)
            return author_info
        except:
            return {"first_name": "", "last_name": ''}

    def get_date(self) -> str:
        try:
            date_element = self.article.find('span', attrs={"property": "volumeNumber".lower()})
            return date_element.get_text()
        except Exception:
            return ''

    def check_bot_detected(self):
        try:
            page_body = self.driver.find_element(By.XPATH, '//body')
            cloudflare_text = [
                'verify you are human',
                'checking if the site connection is secure',
                'needs to review the security of your connection'
            ]
            if any(text for text in cloudflare_text if text in page_body.get_attribute("innerHTML")):
                print('Captcha detected...')
                self.blocked_urls.append(self.url)
                captcha_boxes = page_body.find_elements(By.XPATH, '//input')
                for captcha_box in captcha_boxes:
                    # self.actions.move_to_element(captcha_box).perform()
                    self.driver.execute_script('arguments[0].click()', captcha_box)
                return True
            else:
                print('No captcha detected...')
                return False
        except Exception as err:
            print(err)

    def get_doi(self):
        try:
            doi_element = self.soup.find('div', class_='doi')
            if doi_element is not None:
                return doi_element.get_text()
        except Exception:
            return ''

    def get_content_body(self) -> dict:
        results = {}
        try:
            content_container = self.article.findAll('div', class_='core-container')

            for container in content_container:
                content_sections = container.findAll('section')
                for section in content_sections:
                    content_name = section.find('h2')
                    print("content_name", content_name)
                    content_items_element = section.findAll(attrs={"role": "paragraph"})

                    if content_name is None:
                        continue
                    content_name = content_name.get_text()
                    results[f'{content_name}'] = ''

                    for item in content_items_element:
                        if item is None:
                            continue
                        contents = results.get(f'{content_name}', '')
                        results[f'{content_name}'] = contents + ', ' + item.get_text() if contents else item.get_text()

            return results
        except Exception:
            return results


def main(url: str, driver):
    web_handler = WebHandler(url, driver)

    web_handler.fetch_url()
    time.sleep(random.randrange(3, 7))
    web_handler.perform_mouse_movement()
    bot_detected = web_handler.check_bot_detected()
    if bot_detected:
        return web_handler.blocked_urls
    web_handler.set_url_page_source()
    web_handler.scroll_website(f"{random.randrange(-27, 1001)}")

    time.sleep(random.randrange(3, 7))
    web_handler.scroll_website(f"{random.randrange(-27, 51)}")
    web_handler.initialize_soup_from_page_source()

    time.sleep(random.randrange(5, 10))
    web_handler.scroll_website(f"{random.randrange(-27, 201)}")

    time.sleep(2.3)
    web_handler.perform_mouse_movement()
    web_handler.set_article()

    author_info = web_handler.get_author()
    results = {
        "url": url,
        "title": web_handler.get_title(),
        "author": author_info['first_name'] + " " + author_info['last_name'],
        "date": web_handler.get_date(),
        "doi": web_handler.get_doi(),
        "content": web_handler.get_content_body()
    }

    return results


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    results = []
    # Read the CSV file into a DataFrame
    df = pd.read_csv('crossref.csv')

    # List all the columns
    doi_urls: list[str] = df['doi'].tolist()
    new_doi_urls = []
    for url in doi_urls[:20]:
        new_url = f"https://www.cabidigitallibrary.org/doi/{url}"
        new_doi_urls.append(new_url)

    driver = WebHandler.initialize_driver()
    for url in new_doi_urls:
        result = main(url, driver)
        results.append(result)
        time.sleep(random.randrange(5, 40))
        driver = WebHandler.change_driver_user_agent(driver)

    driver.close()
    driver.quit()

    with open('source.json', 'w') as f:
        json.dump(obj=results, fp=f, indent=2)
