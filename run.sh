# pip3 install scrapy-rotating-proxies --user
curl -sSf "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list.txt" | sed '1,3d; $d; s/\s.*//; /^$/d' > proxies.txt
scrapy crawl cars -o 'cars.json'
