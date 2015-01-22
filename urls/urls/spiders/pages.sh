#!/bin/bash

# pages.sh will run "scrapy crawl urls -a pageno=x from 0 - 50.
# and it output the API urls to file "urls.txt"
# 
# Usage: sh pages.sh
# 
# Author: Peiwen Chen
# Date: Jan 21, 2015


PAGE=0

while [ $PAGE -lt 5 ];do
	scrapy crawl urls -a pageno=$PAGE
	PAGE=$(( $PAGE + 1))
done
