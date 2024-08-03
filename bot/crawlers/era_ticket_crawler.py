from typing import List

from bs4 import BeautifulSoup

from crawler_base import CrawlerBase
from crawler_base import SeatArea
from crawler_base import ShowTime
from crawler_base import Activity

class EraTicketCrawler(CrawlerBase):
    def __init__(self, urls: List[str] = []):
        super().__init__(
            name="年代售票 Era Ticket",
            main_url="https://ticket.com.tw/application/UTK01/UTK0101_06.aspx?TYPE=1&CATEGORY=205",
            use_selenium=True
        )
        self.urls = urls

    def parse_activity_list(self) -> None:
        raise NotImplementedError()

    def parse(self, soup: BeautifulSoup) -> bool:
        title = soup.find("h1", {"align": "center"})
        if title is None: return False
        title = title.find("span", {"class": "title"})
        if title is None: return False
        title = title.text
        info_body = soup.find("tbody")
        show_times = []
        for i_sess, sess in enumerate(info_body.find_all("tr")):
            sess_info = sess.find_all("td")
            # Parse date from <time class="icon"> in first <td>
            sess_date = sess_info[0].find("time", {"class": "icon"})["datetime"].strip()
            sess_time = sess_info[0].find("span", {"class": "time"}).text.strip()
            all_prices = sess_info[2].find("span").text.strip().split("、")
            sold_out_prices = sess_info[2].find("span").find_all("del")
            sold_out_prices = list(map(lambda x: x.text.strip(), sold_out_prices))
            is_cancelled = "取消" in sess_info[3].find("button").text.strip()
            seat_areas = []
            for i_price, price in enumerate(all_prices):
                seat_areas.append(SeatArea(
                    id_ = i_price,
                    name = str(price),
                    available = price not in sold_out_prices and not is_cancelled))
            show_times.append(ShowTime(
                id_ = i_sess,
                name = f"{sess_date} {sess_time}",
                datetime = f"{sess_date} {sess_time}",
                seat_areas = seat_areas,
                available = any([area.available for area in seat_areas]),
                cancelled = is_cancelled))
        self.activities[title] = Activity(
            name=title,
            show_times=show_times,
            available=any([show_time.available for show_time in show_times]),
            parsed=True,
            cancelled=all([show_time.cancelled for show_time in show_times])
        )
        return True

if __name__ == "__main__":
    crawler = EraTicketCrawler(
        urls=[
            "https://ticket.com.tw/application/UTK02/UTK0201_00.aspx?PRODUCT_ID=P0DXG163",
            "https://ticket.com.tw/application/UTK02/UTK0201_00.aspx?PRODUCT_ID=P0CNUP9W",
            "https://ticket.com.tw/application/UTK02/UTK0201_00.aspx?PRODUCT_ID=P09ETYZR",
            "https://ticket.com.tw/application/UTK02/UTK0201_00.aspx?PRODUCT_ID=P0C9W4PE"
        ]
    )
    crawler.parse_activities()
    for activity in crawler.activities.values():
        print(f"{activity.name} | available: {activity.available} | cancelled: {activity.cancelled}")
        for show_time in activity.show_times:
            print(f"    {show_time.name} | available: {show_time.available} | cancelled: {show_time.cancelled}")
            for seat_area in show_time.seat_areas:
                print(f"        {seat_area.name}: {seat_area.available}")