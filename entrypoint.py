#!/usr/local/bin/python
import json
import http.client
import urllib.parse
import sys
import os

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
    print("Could not fetch the version_manifest.json")
    print(read_manifest.status, read_manifest.reason)
    sys.exit(1)

data1 = read_manifest.read()
output = json.loads(data1)  
latest_snap = output['latest']['snapshot']

if lastknown_snap == latest_snap:
    print("Versions are equal")
    sys.exit(0)
else:
    print("Newer version detected")
    print("The new version is", latest_snap)
    connapi = http.client.HTTPSConnection(api_parsed.hostname)
    connapi.request("POST", api_parsed.path)
    response = connapi.getresponse()
    if response.status != 202:
        print("Could not POST to API")
        print(response.status, response.reason)
        sys.exit(1)
    print ("Build request was send.")
    with open('version.json', 'w', encoding='utf-8') as f:
        json.dump({"saved_version": latest_snap}, f)
    sys.exit(0)
