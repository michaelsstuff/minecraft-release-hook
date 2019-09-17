#!/usr/local/bin/python
import json
import urllib.request
import sys
import requests
import os

# API_ENDPOINT = "https://cloud.docker.com/api/build/v1/source/.../trigger/.../call/"
API_ENDPOINT = os.environ['API_ENDPOINT']

# get the last known version
f = open(r"version.json", "r")
olddata = json.load(f)
lastknown_snap = olddata['saved_version']
f.close()

# get the current release snapshot version
newdata = urllib.request.urlopen(
    "https://launchermeta.mojang.com/mc/game/version_manifest.json").read()
output = json.loads(newdata)
latest_snap = output['latest']['snapshot']

if lastknown_snap == latest_snap:
    print("Versions are equal")
    sys.exit()
else:
    print("Newer version detected")
    print("The new version is", latest_snap)
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump({"saved_version": latest_snap}, f)
    requests.post(url = API_ENDPOINT) 
    sys.exit()
