"""
selenium is used with scrapy to scrape dynamic content
"""

import scrapy
from selenium import webdriver

import os

# add executable path for init
os.environ["SELENIUM_SERVER_JAR"] = "selenium-server-standalone-2.44.0.jar"

class MashapeSpider(scrapy.Spider):
	name = "mashape"
	allowed_domains = ["www.mashape.com"]
	start_urls = [
			"https://www.mashape.com/george-vustrey/ultimate-weather-forecasts"
			]
	def __init__(self):
		self.driver = webdriver.Safari()

	def parse(self, response):
		self.driver.get(response.url)
		request = self.driver.find_element_by_xpath('//div[@class="request"]')
		if request:
			print ("starting retrieving request ....")
			endpoint_name = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="endpoint-name"]/span')
			description = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="description"]')
			parameters_name = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="parameter typed required"]/div/span[@class="name"]')
			parameters_type = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="parameter typed required"]/div/span[@class="type"]')

		option = self.driver.find_element_by_xpath('//div[@class="language-selector"]/ul/li[2]/span')
		if "JAVA" == option.text:
			print("pick Java code snippet........") 
			self.driver.find_element_by_xpath('//div[@class="language-selector"]/ul/li[2]/span').click()

		response = self.driver.find_element_by_xpath('//div[@class="request"]')
		if response:
			print("starting retrieving code snippet...")
			code_snippet = self.driver.find_element_by_xpath('//div[@class="response"]/pre[@class="code"]/div[@class="code-snippet"]')
		
		print "output results"		
		print endpoint_name.text
		print description.text
		print parameters_name.text
		print parameters_type.text
		print code_snippet.text
		self.driver.close()
