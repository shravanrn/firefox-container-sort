# Firefox container alphabetical sort

Sort firefox containers by name. The script reads container.json. It then:

- Updates container.json with a sorted profile list so that the order of entries in the "Open in New Container Tab" context menu works as expected. The old container.json is backed up as container.jsonTimeStamp.bak
- It outputs a new value for "container-order" which is the sorted containers. Users must take this output, and manually replace the local storage of the containers addons.

To use the script

1. Get the profile path by opening "about:profiles" in Firefox. Copy the path listed in the Root Directory of the first entry
2. Run the script `python3 container-sort.py`. Paste the path you got from Step 1 and copy the string printed by the script.
3. Go to Firefox's addon debug page by opening [about:debugging#/runtime/this-firefox](about:debugging#/runtime/this-firefox)
4. Click on "Inspect" on the entry for "Firefox Multi-Account Containers"
5. Expand the "Extension Storage" tree entry and select the entry underneath it that looks like "moz://funnylongstring"
6. Enter "container-order" in the "Filter Items" textbox
7. Replace the contents of the only search result with the contents copied from Step 2
8. Restart Firefox
