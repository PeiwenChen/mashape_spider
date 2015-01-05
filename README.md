mashape_spider
==============

a spider to crape mashape.com 

mashape.com is the largest world-class marketplace to consume, 
distribute, manage, and monitor both private and public APIs 
from developers all over the world.

This project will create a spider to fetch the interfaces of the public APIs 
on mashape.com and store the data.

Requirements:
******************
1. Scrapy
To install Scrapy, please follow the official guide:
http://doc.scrapy.org/en/0.24/intro/install.html

Make sure dependencies lib installed and worked.

2. Selenium
To scrape the JS rendered content, Selenium is needed.
steps for Selenium env setup: 

a. Download selenium server from http://www.seleniumhq.org/download/   selenium-server-standalone-2.37.0.jar
b. Install Selenium Safari(or other web browers) Webdriver Extension
c. Install Selenium Client & WebDriver Language Bindings for Python: pip install selenium


Usage:
*****************
scrapy crawl mashape

This mashape_spider crawls the "https://www.mashape.com/george-vustrey/ultimate-weather-forecasts"


Next Step:
*****************
1. fix the response hover.perform() issue, the code-snippet of "Java" cannot be fetched
2. fetch more public API.
