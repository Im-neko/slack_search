import os
import re
import time
import datetime
import pprint
import json
import urllib.parse
import urllib.request
from elasticsearch import Elasticsearch

pp = pprint.PrettyPrinter(indent=4)


API_URL_BASE = "https://slack.com/api/search.all?token=%s&query=%s&count=100&page=%d&sort=timestamp&sort_dir=desc"
API_TOKEN = os.environ['API_TOKEN']
SEARCH_PERIOD = 2
REQUEST_INTERVAL = 5
CHANNEL_PATTERN = "^.*$"

channels = []
re_ptn = re.compile(CHANNEL_PATTERN)
base_d = datetime.date.today() - datetime.timedelta(SEARCH_PERIOD)
q = urllib.parse.quote("after:%s" % base_d.strftime("%Y-%m-%d"))
p = 1

es = Elasticsearch("http://elastic:9200")

while True:
    url = API_URL_BASE % (API_TOKEN, q, p)
    res = urllib.request.urlopen(url)
    json_res = json.loads(res.read().decode('utf8'))
    pp.pprint(json_res)
    paging = json_res['messages']['paging']
    print("%d/%d" % (paging['page'], paging['pages']))
    for message in json_res['messages']['matches']:
        try:
            if not message['channel']['is_channel'] or message['type'] != 'message':
                continue
            data = message
            data['ts'] = float(message['ts'])
            data['datetime'] = datetime.datetime.fromtimestamp(float(data['ts']), datetime.timezone.utc).strftime('%Y/%m/%d %H:%M:%S')
            res = es.index(index=message['channel']['name'], doc_type="message", body=message)
        except Exception as e:
            print("---error---")
            print(e)
    if (p >= paging['pages']):
        break
    p = p + 1
    time.sleep(REQUEST_INTERVAL)
