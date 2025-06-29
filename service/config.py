from kazoo.client import KazooClient
import json

with open("config.json") as f:
    cfg_blob = f.read()

zk = KazooClient(hosts="127.0.0.1:2181")
zk.start()

if not zk.exists("/config"):
    zk.create("/config", cfg_blob.encode("utf-8"), makepath=True)
else:
    zk.set("/config", cfg_blob.encode("utf-8"))

zk.stop()

