# Ticket-Tortoise/Crawlers
## How to Implement a New Crawler Module
This guide will walk you through the process of implementing a new crawler module in this project.

### Step 1: Create a New Python File
Create a new Python file in the `crawlers` directory. The file name should be descriptive of the website you are crawling. For example, if you are creating a crawler for a website called `TicketMaster`, you might name your file `ticketmaster_crawler.py`.

### Step 2: Import Necessary Libraries
At the top of your new Python file, import the necessary libraries. You will likely need the following:

```python
from bs4 import BeautifulSoup
from crawler_base import CrawlerBase
from crawler_base import SeatArea
from crawler_base import ShowTime
from crawler_base import Activity
```

### Step 3: Define Your Crawler Class
Next, define a new class for your crawler. This class should inherit from CrawlerBase. For example:

```python
class TicketMasterCrawler(CrawlerBase):
    def __init__(self, urls: List[str] = []):
        super().__init__(
            name="TicketMaster",
            main_url="https://www.ticketmaster.com/",
            use_selenium=True
        )
        self.urls = urls
```

Note that the argument `main_url` should be the website that list all (or most) of the activities. There's a plan to select target activity through Discord UI that will use this url.


### Step 4: Implement Required Methods
Your new crawler class needs to implement the following methods:
- `parse(self, soup: BeautifulSoup) -> bool`: This method should parse the details of a single activity and set the variable `activities: Dict[str, Activity]`. The `soup` parameter is a BeautifulSoup object representing the HTML of the activity page.
- `parse_activity_list(self) -> None` (Optional): This method should parse the list of activities from the main URL of the website.

Refer to the existing crawler classes (`EraTicketCrawler` and `TicketPlusCrawler`) for examples of how these methods can be implemented.

### Step 5: Test Your Crawler
Finally, test your new crawler by creating an instance of your crawler class and calling its methods. For example:

```python
if __name__ == "__main__":
    crawler = TicketMasterCrawler(
        urls=[
            "https://www.ticketmaster.com/event/1",
            "https://www.ticketmaster.com/event/2",
            "https://www.ticketmaster.com/event/3",
        ]
    )
    crawler.parse_activities()
    for activity in crawler.activities.values():
        print(f"{activity.name}: {activity.available}")
        for show_time in activity.show_times:
            print(f"    {show_time.name}: {show_time.available}")
```

This will print out the name and availability of each activity and show time.

Note that the function `parse_activities(self) -> None` implemented in the base class `crawler_base.py` will walk through all the urls passed into the inherit class, parse urls into soup objects then feed to the `parse(self, soup: BeautifulSoup) -> bool` function which you should implement.

That's it! You've now implemented a new crawler module. Happy crawling!

## TODO
- [ ] Activity List Parsing
- [ ] Make main_url a list that handles the categories page of each tix website.