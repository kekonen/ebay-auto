KEK=`python3 -c "import datetime as dt;n=dt.datetime.now();print('{0:%H_%d-%m-%ycars.json}'.format(n))"`

lol="/media/nvidia/card/spider/$KEK"
echo run: scrapy crawl cars -o $lol

scrapy crawl cars -o $lol

