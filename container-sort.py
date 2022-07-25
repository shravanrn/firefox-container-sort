#!/usr/bin/env python3
import os
import json
import shutil
import time

profile_path = str(input("Enter firefox profile path: "))

containers_json_file = os.path.join(profile_path, "containers.json")

try:
    with open(containers_json_file, 'r') as file:
        containers_json = file.read()
except:
    print("Could not open container json file: " + containers_json_file)
    exit(1)

try:
    containers_data = json.loads(containers_json)
except:
    print("Could not parse container json file: " + containers_json_file)
    exit(1)

# Data looks like this
# {
#     "version": 4,
#     "lastUserContextId": 94,
#     "identities": [
#         {
#             "userContextId": 4,
#             "public": true,
#             "icon": "cart",
#             "color": "pink",
#             "l10nID": "userContextShopping.label",
#             "accessKey": "userContextShopping.accesskey",
#             "telemetryId": 4
#         },
#         {
#             "userContextId": 5,
#             "public": false,
#             "icon": "",
#             "color": "",
#             "name": "userContextIdInternal.thumbnail",
#             "accessKey": ""
#         },
#         // ...
#     ]
# }
profiles = containers_data["identities"]

def remove_prefix_suffix(s, prefix, suffix):
    original = s
    if s.startswith(prefix):
        s = s[len(prefix):]
    else:
        return original
    if s.endswith(suffix):
        s = s[:-len(suffix)]
    else:
        return original
    return s

def get_sort_key(p):
    # Put private entries in the top
    if p["public"] is False:
        return "_" + str(p["name"])

    # Public entries without a name or l10nID (default containers like Shopping have these) go to the end
    ret = "zzz"
    if "name" in p:
        ret = p["name"]
    elif "l10nID" in p:
        ret = remove_prefix_suffix(p["l10nID"], "userContext", ".label")
    return ret.lower()

sorted_profiles = sorted(profiles, key=lambda p: get_sort_key(p))

containers_data["identities"] = sorted_profiles

try:
    new_containers_json = json.dumps(containers_data, indent=4)
except:
    print("Could not stringify modified json: " + containers_data)
    exit(1)

def current_milli_time_str():
    return str(round(time.time() * 1000))

try:
    # Make backup of containers.json, and then write to it
    containers_json_backup_file = os.path.join(profile_path, "containers.json" + current_milli_time_str() + ".bak")
    shutil.copyfile(containers_json_file, containers_json_backup_file)
except:
    print("Could not open create backup json file: " + containers_json_backup_file)
    exit(1)

try:
    with open(containers_json_file, 'w') as file:
        containers_json = file.write(new_containers_json)
except:
    print("Could not write container json file: " + containers_json_file)
    exit(1)

public_sorted_profiles = [p for p in sorted_profiles if p["public"] is True]

# Format is
# {"firefox-container-34":0, "firefox-container-36":1, ...}
out_strings = []
for i, p in enumerate(public_sorted_profiles):
    entry = "\"firefox-container-" + str(p["userContextId"]) + "\": " + str(i)
    out_strings.append(entry)

output = "{ " + ", ".join(out_strings) + "}"

print(output)

