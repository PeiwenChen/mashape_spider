"""
selenium is used with scrapy to scrape dynamic content
parse the API has only one method
Author: Peiwen Chen
Date: Jan 4, 2015
"""

import scrapy
from selenium import webdriver
import pprint
import os
import json

# add executable path for init
os.environ["SELENIUM_SERVER_JAR"] = "selenium-server-standalone-2.44.0.jar"

class MashapeSpider(scrapy.Spider):
	name = "mashape"
	allowed_domains = ["www.mashape.com"]
	start_urls = [
			# "https://www.mashape.com/george-vustrey/ultimate-weather-forecasts"
			"https://www.mashape.com/mark-sutuer/ip-utils"
			]
	def __init__(self):
		self.driver = webdriver.Safari()
		# if running on chrome
		#self.driver = webdriver.chrome()

	def parse(self, response):
		self.driver.get(response.url)
		# multiple requests
		api = {}
		if self.driver.find_elements_by_xpath('//div[@class="request"]'):
			print ("starting retrieving request ....")
			request_list = {} 
			endpoint_name_list = []
			description_list = []
			parameters_name_list = []
			parameters_type_list = []

			for endpoint_name in self.driver.find_elements_by_xpath('//div[@class="request"]/div[@class="endpoint-name"]/span'):
				print "request -> endpoint_name " + endpoint_name.text
				endpoint_name_list.append(endpoint_name.text)
			for description in self.driver.find_elements_by_xpath('//div[@class="request"]/div[@class="description"]'):
				print "request -> description " + description.text
				description_list.append(description.text)
			for parameters_name in self.driver.find_elements_by_xpath('//div[@class="request"]/div[contains(@class, "parameter typed")]/div/span[@class="name"]'):
				print "request -> parameters_name " + parameters_name.text
				parameters_name_list.append(parameters_name.text)
			for parameters_type in self.driver.find_elements_by_xpath('//div[@class="request"]/div[contains(@class, "parameter typed")]/div/span[@class="type"]'):
				print "request ->parameters_type " + parameters_type.text
				parameters_type_list.append(parameters_type.text)
			
			request_list['endpoint_name'] = endpoint_name_list
			request_list['description'] = description_list
			request_list['parameters_name'] = parameters_name_list
			request_list['parameters_type'] = parameters_type_list
			api['request'] = request_list

		for option in self.driver.find_elements_by_xpath('//div[@class="language-selector"]/ul/li[2]/span'):
			if "JAVA" == option.text:
				print("pick Java code snippet........") 
				option.click()

		if self.driver.find_elements_by_xpath('//div[@class="request"]'):
			print("starting retrieving code snippet...")
			response_list = {}
			code_snippet_list = []
			for code_snippet in self.driver.find_elements_by_xpath('//div[@class="response"]/pre[@class="code"]/div[@class="code-snippet"]'):
				print "response -> java code snippet " + code_snippet.text
				code_snippet_list.append(code_snippet.text)
			response_list['java_code_snippet'] = code_snippet_list
		
		api['response'] = response_list
		
		# write it to json file
		with open('api.json', 'w') as outfile:
			json.dump(api, outfile)
		
		self.driver.close()
		"""
		below is one request
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
		"""

