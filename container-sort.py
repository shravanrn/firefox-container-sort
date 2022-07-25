#!/usr/bin/env python3
import os
import json

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
public_profiles = [p for p in profiles if p["public"] is True]

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

def get_profile_name(r):
    ret = "zzz"
    if "name" in r:
        ret = r["name"]
    elif "l10nID" in r:
        ret = remove_prefix_suffix(r["l10nID"], "userContext", ".label")
    return ret.lower()

sorted_profiles = sorted(public_profiles, key=lambda p: get_profile_name(p))


# Format is
# {"firefox-container-34":0, "firefox-container-36":1, ...}
out_strings = []
for i, p in enumerate(sorted_profiles):
    entry = "\"firefox-container-" + str(p["userContextId"]) + "\": " + str(i)
    out_strings.append(entry)

output = "{ " + ", ".join(out_strings) + "}"

print(output)

