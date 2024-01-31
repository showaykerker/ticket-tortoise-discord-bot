import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from pydantic import BaseModel

from typing import List
from typing import Optional

from bs4 import BeautifulSoup

class CrawlerBase:
    def __init__(self, name: str, main_url: str, use_selenium: bool = False):
        self.name = name
        self.main_url = main_url
        self.use_selenium = use_selenium
        self.drivers = None
        self.activities = {}
        if use_selenium:
            self.options = ChromeOptions()
            self.options.add_argument("--disable-extenstions")
            self.options.add_argument("--headless")
            self.service = ChromeService(executable_path="/usr/bin/chromedriver")
            # sudo apt-get install chromium-chromedriver
            self.driver = webdriver.Chrome(options=self.options, service=self.service)

    def parse_activities(self) -> None:
        soups = self.get_soups(self.urls)
        for i_soup, soup in enumerate(soups):
            print(f"Parsing {i_soup}th soup, {self.urls[i_soup]}")
            for i in range(10):
                success = self.parse(soup)
                if success: break

    def parse_activity_list(self) -> None:
        raise NotImplementedError()

    def parse(self, soup: BeautifulSoup) -> None:
        raise NotImplementedError()

    def get_soups(self, urls: List[str]) -> List[BeautifulSoup]:
        return [self.get_soup(url) for url in urls]

    def get_soup(self, url: Optional[str] = None) -> BeautifulSoup:
        url = url or self.main_url
        if self.use_selenium:
            self.driver.get(url)
            soup = BeautifulSoup(self.driver.page_source, "html.parser")
        else:
            soup = BeautifulSoup(requests.get(url).text, "html.parser")
        return soup

class SeatArea(BaseModel):  # 座位區域
    id_: int
    name: str
    available: bool

class ShowTime(BaseModel):  # 場次
    id_: int
    name: str
    datetime: str
    seat_areas: List[SeatArea]
    available: bool
    cancelled: bool = False

class Activity(BaseModel):  # 活動
    name: str
    show_times: List[ShowTime]
    available: bool
    parsed: bool = False
    cancelled: bool = False

