import asyncio
import requests

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from pydantic import BaseModel

from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from bs4 import BeautifulSoup

class CrawlerBase:
    def __init__(self, name: str, use_selenium: bool = False):
        self.name = name
        self.use_selenium = use_selenium
        self.drivers = None
        self.soups = {}
        if use_selenium:
            self.options = ChromeOptions()
            self.options.add_argument("--disable-extenstions")
            self.options.add_argument("--headless")
            self.service = ChromeService(executable_path="/usr/bin/chromedriver")
            # sudo apt-get install chromium-chromedriver
            self.driver = webdriver.Chrome(options=self.options, service=self.service)
        #     self.driver.get(url)
        #     self.web = self.driver.page_source
        #     self.soup = BeautifulSoup(self.web, "html.parser")
        # else:
        #     self.web = requests.get(url)
        #     self.soup = BeautifulSoup(self.web.text, "html.parser")

    def get_soups(self, names: List[str], urls: List[str]) -> List[BeautifulSoup]:
        return [self.get_soup(name, url) for name, url in zip(names, urls) if name not in self.soups]

    def get_soup(self, name: str, url: str) -> BeautifulSoup:
        if name in self.soups:
            return self.soups[name]
        if self.use_selenium:
            self.driver.get(url)
            self.soups[name] = BeautifulSoup(self.driver.page_source, "html.parser")
        else:
            self.soups[name] = BeautifulSoup(requests.get(url).text, "html.parser")
        return self.soups[name]

class SeatArea(BaseModel):  # 座位區域
    name: str
    available: bool

class ShowTime(BaseModel):  # 場次
    name: str
    seat_areas: List[SeatArea]
    available: bool

class Activity(BaseModel):  # 活動
    name: str
    show_times: List[ShowTime]
    available: bool

class TicketPlusCrawler(CrawlerBase):
    def __init__(self, names: List[str], urls: List[str] = []):
        super().__init__(
            name="TicketPlus",
            use_selenium=True
        )
        self.names, self.urls = names, urls
        self.get_soups(names, urls)

    def _parse(self, name: str, soup: BeautifulSoup) -> None:
        show_times = []
        # input(soup)
        for _sess in soup.find_all("div", class_="sesstion-item"):
            sess = _sess.find("div")


    def _parse_all(self) -> None:
        for name, soup in self.soups.items():
            self._parse(name, soup)

if __name__ == "__main__":
    crawler = TicketPlusCrawler(
        names=["萬青"],
        urls=[
            "https://ticketplus.com.tw/activity/b9e6a9a22eea2003946b55c5924e72b2?fbclid=IwAR3wSDTOy4hoMUj-Xpu6ma5tLYiJJC2yxwArW_SDuz8QgyH3W3jYbfmWOXA"
        ]
    )
    crawler._parse_all()