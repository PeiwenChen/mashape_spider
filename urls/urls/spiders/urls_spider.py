"""
a spider to query urls for all the APIs in mashape
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
	
	def start_requests(self):
		start_urls = [
			"https://www.mashape.com/explore?sort=developers&page=10"
			]
		# read the url list from a file
		# f = open("urls.txt", "r")
		# start_urls = [url.strip() for url in f.readlines()]
		# f.close()
		#return [Request(url = start_url) for start_url in start_urls]

	def __init__(self):
		self.driver = webdriver.Safari()
		self.url_list = []
		# if running on chrome
		#self.driver = webdriver.chrome()

	def parse(self, response):
		self.driver.get(response.url)
		blocks = self.driver.find_elements_by_xpath('//div[@class="apis blocks grid"]/div/div/div/div[@class="api api-card block panel panel-default"]')
	
		if isinstance(blocks, Iterable):
			for block in blocks:
				url = block.find_element_by_xpath('.//a/@href').extract()
				print url
				self.url_list.append(url)
		else:
			print block

		self.driver.close()

