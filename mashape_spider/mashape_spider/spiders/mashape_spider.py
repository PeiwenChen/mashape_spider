"""
selenium is used with scrapy to scrape dynamic content
"""

import scrapy
from selenium import webdriver

import os
import pprint

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
		pprint.pprint( "starting loading url....")
		self.driver.get(response.url)
		request = self.driver.find_element_by_xpath('//div[@class="request"]')
		if request:
			pprint.pprint ("starting retrieving request ....")
			endpoint_name = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="endpoint-name"]/span')
			description = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="description"]')
			parameters_name = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="parameter typed required"]/div/span[@class="name"]')
			parameters_type = self.driver.find_element_by_xpath('//div[@class="request"]/div[@class="parameter typed required"]/div/span[@class="type"]')

		lang_to_hover_over = self.driver.find_element_by_css_selector("div.language-selector > ul")
		print "moving to element......"
		hover = webdriver.ActionChains(self.driver).move_to_element(lang_to_hover_over)
		print "try to perform ......."
		hover.perform()
		print "try to find current ...."
		if "Java" == self.driver.find_element_by_css_selector("span.current").text:
			print "find the current span........." 
			self.driver.find_element_by_css_selector("span.current").click()

		response = self.driver.find_element_by_xpath('//div[@class="request"]')
		if response:
			pprint.pprint("starting retrieving code snippet...")
			code_snippet = self.driver.find_element_by_xpath('//div[@class="response"]/pre[@class="code"]/div[@class="code-snippet"]')
		
		print "starting output results"		
		print endpoint_name.text
		print description.text
		print parameters_name.text
		print parameters_type.text
		print code_snippet.text
		self.driver.close()
