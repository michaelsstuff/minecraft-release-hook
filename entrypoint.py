#!/usr/local/bin/python
import json
import http.client
import urllib.parse
import sys
import os
import datetime

now = datetime.datetime.now()

# API_ENDPOINT = "https://cloud.docker.com/api/build/v1/source/.../trigger/.../call/"
API_ENDPOINT = os.environ['API_ENDPOINT']
api_parsed = urllib.parse.urlparse(API_ENDPOINT)

# get the last known version
f = open(r"version.json", "r")
olddata = json.load(f)
lastknown_snap = olddata['saved_version']
f.close()

# get the current release snapshot version
conn = http.client.HTTPSConnection("launchermeta.mojang.com")
conn.request("GET", "/mc/game/version_manifest.json")
read_manifest = conn.getresponse()
if read_manifest.status != 200:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " Could not fetch the version_manifest.json")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " " + str(read_manifest.status), str(read_manifest.reason))
    sys.exit(1)

data1 = read_manifest.read()
output = json.loads(data1)  
latest_snap = output['latest']['snapshot']

if lastknown_snap == latest_snap:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " Versions are equal")
    sys.exit(0)
else:
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " Newer version detected")
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " The new version is", latest_snap)
    connapi = http.client.HTTPSConnection(api_parsed.hostname)
    connapi.request("POST", api_parsed.path)
    response = connapi.getresponse()
    if response.status != 202:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " Could not POST to API")
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + str(response.status), str(response.reason))
        sys.exit(1)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M") + " Build request was send.")
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump({"saved_version": latest_snap}, f)
    sys.exit(0)
