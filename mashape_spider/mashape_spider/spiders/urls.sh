
#!/bin/bash
# urls.sh will run "scrapy crawl mashape -a readurl="".
# and it output the API input/output to file "api.json"

# Usage: sh urls.sh
# Author: Peiwen Chen
# Date: Jan 21. 2015

while read -r line;do
	echo "$line"
	scrapy crawl mashape -a readurl="$line"
done <"urls.txt"
