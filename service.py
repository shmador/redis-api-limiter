import requests
import redis
import json

with open('config.json') as f:
    d = json.load(f)
    print(d)

redis_conf=d['redis']
api_conf=d['api']

r = redis.Redis(host=redis_conf['host'], port=redis_conf['port'], decode_responses=redis_conf['decode_responses'], password=redis_conf['password'])
key_name = redis_conf['key_name']
ttl = int(redis_conf['ttl'])
cache = r.get(key_name)

url = api_conf['url']

if cache:
    print(json.loads(cache))
else:
    response = requests.get(url)
    data = response.json()
    r.set(key_name, json.dumps(data), ttl)
    print(data)

