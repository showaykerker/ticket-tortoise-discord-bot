from typing import List

from bs4 import BeautifulSoup

from crawler_base import CrawlerBase
from crawler_base import SeatArea
from crawler_base import ShowTime
from crawler_base import Activity

class TicketPlusCrawler(CrawlerBase):
    def __init__(self, urls: List[str] = []):
        super().__init__(
            name="遠大娛樂 TicketPlus",
            main_url="https://ticketplus.com.tw/",
            use_selenium=True
        )
        self.urls = urls
        soups = self.get_soups(urls)
        self.parse_all(soups)

    def parse_activity_list(self) -> None:
        pass

    def parse(self, soup: BeautifulSoup) -> bool:
        show_times = []
        # parse <title> inside <head>
        title = soup.find("title").text.strip()
        if not title:
            return False
        for _sess in soup.find_all("div", class_="sesstion-item"):
            sess = _sess.find("div")
            first_child = sess.contents[0]
            second_child = sess.contents[1]
            sess_title = first_child.contents[0].contents[0].contents[0].text.strip()
            sess_date = first_child.contents[0].contents[1].contents[0].contents[1].text.strip()
            sess_time = first_child.contents[0].contents[2].contents[0].contents[1].text.strip()
            available = second_child.find("button", class_="nextBtn float-right v-btn v-btn--block v-btn--has-bg v-btn--rounded theme--dark v-size--default") is not None # 立即購買
            show_times.append(ShowTime(
                id_=len(show_times),
                name=sess_title,
                datetime=f"{sess_date} {sess_time}",
                seat_areas=[],
                available=available
            ))
        self.activities[title] = Activity(
            name=title,
            show_times=show_times,
            available=any([show_time.available for show_time in show_times]),
            parsed=True
        )
        return True

if __name__ == "__main__":
    crawler = TicketPlusCrawler(
        urls=[
            "https://ticketplus.com.tw/activity/b9e6a9a22eea2003946b55c5924e72b2?fbclid=IwAR3wSDTOy4hoMUj-Xpu6ma5tLYiJJC2yxwArW_SDuz8QgyH3W3jYbfmWOXA",
            "https://ticketplus.com.tw/activity/ea11993dd92ca5a4b41e1c9793452e46",
            "https://ticketplus.com.tw/activity/412bc49904bbd0f6ab1ed1c2b2a22f4f",
            "https://ticketplus.com.tw/activity/b0b7808cd4e5ba73763b9c5f583b98f2"
        ]
    )
    for activity in crawler.activities.values():
        print(f"{activity.name}: {activity.available}")
        for show_time in activity.show_times:
            print(f"    {show_time.name}: {show_time.available}")
            for seat_area in show_time.seat_areas:
                print(f"        {seat_area.name}: {seat_area.available}")