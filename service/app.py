import requests
import redis
import json
import time

from kazoo.client import KazooClient
from kazoo.recipe.watchers import DataWatch

# Start Zookeeper client
zk = KazooClient(hosts='127.0.0.1:2181')
zk.start()

# Set up config from Zookeeper
def update_conf(*args):
    global r, key_name, ttl, url # Globals
    d=json.loads(zk.get("/config")[0].decode("utf-8"))
    # Redis config
    redis_conf=d['redis']
    r = redis.Redis(host=redis_conf['host'], port=redis_conf['port'], decode_responses=redis_conf['decode_responses'], password=redis_conf['password'])
    key_name = redis_conf['key_name']
    ttl = int(redis_conf['ttl'])
    # API config
    api_conf=d['api']
    url = api_conf['url']

# Fetch config on bootstrap
update_conf()

# Set watcher to update config dynamically on changes
DataWatch(zk, "/config", update_conf)

# Main service loop
def main():
    while True:
        cache = r.get(key_name)
        if cache:
            print(json.loads(cache))
        else:
            response = requests.get(url)
            data = response.json()
            r.set(key_name, json.dumps(data), ex=ttl)
            print(data)
        time.sleep(2)

# Invoke main function
if __name__ == "__main__":
    main()
