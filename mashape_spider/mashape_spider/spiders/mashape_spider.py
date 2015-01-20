"""
selenium is used with scrapy to scrape dynamic content
parse the API has only one method
Author: Peiwen Chen
Date: Jan 4, 2015
"""

import scrapy
from selenium import webdriver
import os
import json

from collections import Iterable

# add executable path for init
os.environ["SELENIUM_SERVER_JAR"] = "selenium-server-standalone-2.44.0.jar"

class MashapeSpider(scrapy.Spider):
	name = "mashape"
	allowed_domains = ["www.mashape.com"]
	start_urls = [
			#"https://www.mashape.com/george-vustrey/ultimate-weather-forecasts",
			"https://www.mashape.com/mark-sutuer/ip-utils"
			]
	def __init__(self):
		self.driver = webdriver.Safari()
		self.api_all = []
		# if running on chrome
		#self.driver = webdriver.chrome()

	def parse_request(self, response, request):
			"""
			given the non-iterable request, returns a request_dict
			"""
			request_dict = {}
			if isinstance(request, Iterable):
				print "Error: parse_request() only accepts non-iterable request"
			else:
				endpoint_name = request.find_element_by_xpath('.//div[@class="endpoint-name"]/span')
				#print "PEIWENC: API request -> endpoint_name " + endpoint_name.text
				request_dict['api_name'] = endpoint_name.text

				description = request.find_element_by_xpath('.//div[@class="description"]')
				#print "PEIWENC: API request -> description " + description.text
				request_dict['description'] = description.text

				# get name and type parameters arrays
				request_dict['input_parameters'] = []
				parameters_name = request.find_elements_by_xpath('.//div[contains(@class, "parameter typed")]/div/span[@class="name"]')
				input_names = []
				input_types = []
				input_des = []
				if type(parameters_name) is list:
					for p in parameters_name:
						#print "PEIWENC:API request -> parameters_name " + p.text
						input_names.append(p.text)
				else:
					#print "PEIWENC: API request -> parameters_name " + parameters_name.text
					input_names.append(parameters_name.text)

				parameters_type = request.find_elements_by_xpath('.//div[contains(@class, "parameter typed")]/div/span[@class="type"]')
				if type(parameters_type) is list:
					for p in parameters_type:
						#print "PEIWENC: request ->parameters_type " + p.text
						input_types.append(p.text)
				else:
					#print "PEIWENC: request ->parameters_type " + parameters_type.text
					input_types.append(parameters_type.text)
				
				parameters_des = request.find_elements_by_xpath('.//div[contains(@class, "parameter typed")]/div/p')
				if type(parameters_des) is list:
					for p in parameters_des:
						#print "PEIWENC: list  request ->parameters_des appending null "
						input_des.append(p.text)
				else:
					input_des.append(parameters_des.text)
				
				# convert arrays into dicts
				i = 0
				while i < len(input_names):
					input_p = {}
					input_p['name'] = input_names[i]
					input_p['type'] = input_types[i]
					input_p['description'] = input_des[i]
					request_dict['input_parameters'].append(input_p)
					i += 1
			return request_dict

	def parse_response(self, response, response_parameter):
			"""
			given the response, return a response_dict
			"""
			response_dict = {}
			# code choice
			for option in self.driver.find_elements_by_xpath('//div[@class="language-selector"]/ul/li[2]/span'):
				if "JAVA" == option.text:
					print("PEIWENC: pick Java code snippet........") 
					option.click()
			
			response_dict["url"] = []
			response_dict["output_parameters"] = []
			container = response_parameter.find_element_by_xpath('.//pre[contains(@class,"route-container")]')
			verb = container.find_element_by_xpath('.//span[@class="verb"]')
			response_dict["api_method"] = verb.text
			routes = container.find_element_by_xpath('.//span[@class="route-definition"]')
			if not isinstance(routes, Iterable):
				response_dict["url"].append(routes.text)
			else:
				for r in routes:
					response_dict["url"].append(r.text)
			
			code = response_parameter.find_element_by_xpath('.//pre/div[@class="code-snippet"]')
			#print "PEIWENC: response -> java code snippet " + code_snippet.text
			response_dict["code_snippet"] = code.text
			
			parameter_model = response_parameter.find_element_by_xpath('.//div[@class="parameter model"]/pre/div[@class="perfectscroll-container"]')
			if not isinstance(parameter_model, Iterable):
				response_dict["output_parameters"].append(parameter_model.text)
			else:
				for p in parameter_model:
					response_dict["output_parameters"].append(p.text)
			
			return response_dict
			
	def add_api(self, request_dict, response_dict):
		"""
		given the request/response_dict, add it into the golbal api_all dict
		"""
		api = {}
		api["api_name"] = request_dict["api_name"]
		api["api_description"] = request_dict["description"]
		api["api_method"] = response_dict["api_method"]
		api["url"] = response_dict["url"]
		api["input_parameters"] = request_dict["input_parameters"]
		api["api_example"] = response_dict["code_snippet"]
		api["output_parameters"] = response_dict["output_parameters"]
		self.api_all.append(api)
		
	def parse_multiple(self, response, sections):

		request_list = []
		response_list = []
		if isinstance(sections, Iterable):
			# get request_list and response_list
			for request in self.driver.find_elements_by_xpath('.//div[@class="request"]'):
				request_dict = self.parse_request(response, request)	
				request_list.append(request_dict)
			for response_parameter in self.driver.find_elements_by_xpath('.//div[@class="response"]'):
				response_dict = self.parse_response(response, response_parameter)
				response_list.append(response_dict)

		# write request/response_list into api_all
		idx = 0
		while idx < len(request_list):
			self.add_api(request_list[idx], response_list[idx])
			idx += 1

		# write api_all to json file
		with open('api.json', 'w') as outfile:
			json.dump(self.api_all, outfile)

	def parse(self, response):
		self.driver.get(response.url)
		sections = self.driver.find_elements_by_xpath('//section[@class="endpoint"]')
		
		self.parse_multiple(response,sections)
		self.driver.close()

