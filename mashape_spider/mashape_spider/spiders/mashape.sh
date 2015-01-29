
#!/bin/bash
# urls.sh will run "scrapy crawl mashape -a readurl="".
# and it output the API input/output to file "api.json"

# Usage: sh urls.sh
# Author: Peiwen Chen
# Date: Jan 21. 2015

CNT=0
while read -r line;do
	echo "$line"
	CNT=$(( $CNT + 1 ))
	scrapy crawl mashape -a url=$line
	if [ $CNT -gt 10 ];then
		CNT=0
		sleep 120
		ps -a |grep "sele" | xargs kill -9
	fi
done <"urls.txt"
