"""
a spider to query urls for all the APIs in mashape
Usage: scrapy crawl urls -a pageno=x
output is urls.txt

Author: Peiwen Chen
Date: Jan 20, 2015
"""

import scrapy
from selenium import webdriver
import os
import json
from scrapy.http import Request

from collections import Iterable

# add executable path for init
os.environ["SELENIUM_SERVER_JAR"] = "selenium-server-standalone-2.44.0.jar"

class UrlsSpider(scrapy.Spider):
	name = "urls"
	allowed_domains = ["www.mashape.com"]
	
	def __init__(self, pageno=None, *args, **kwargs):
		super(UrlsSpider, self).__init__(*args, **kwargs)
		self.driver = webdriver.Safari()
		self.url_list = []
		# if running on chrome
		#self.driver = webdriver.chrome()

		self.start_urls = [
				"https://www.mashape.com/explore?sort=developers&page=%s" %pageno
				]

	def parse(self, response):
		self.driver.get(response.url)
		blocks = self.driver.find_elements_by_xpath('//div[@class="apis blocks grid"]/div/div/div/div[@class="api api-card block panel panel-default"]/a')
	
		if isinstance(blocks, Iterable):
			for block in blocks:
				url = block.get_attribute('href')
				#url = block.find_element_by_xpath('.//a/@href').extract()
				self.url_list.append(url)
		else:
			self.url_list.append(url)	

		self.driver.close()
		with open ("urls.txt", "a") as f:
			f.write('\n')
			f.write("\n".join(url for url in self.url_list))

