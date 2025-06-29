import requests
import redis
import json

r = redis.Redis(host='localhost', port=6379, decode_responses=True, password='eYVX7EwVmmxKPCDmwMtyKVge8oLd2t81')
cache = r.get('cache')

if cache:
    print(json.loads(cache))
else:
    url = "https://jsonplaceholder.typicode.com/todos/2"
    response = requests.get(url)
    data = response.json()
    r.set('cache', json.dumps(data), ex=10)
    print(data)

