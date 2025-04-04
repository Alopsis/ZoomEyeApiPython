import json
import base64
import re
from datetime import datetime, timedelta, UTC, timezone
import os
import subprocess
import requests
import base64

#############################################
# Méthode avec le regex pour le HTTP HEADER #
#############################################

# On récupere les 2 premieres pages 
entity_name = "{ENTITY_NAME_HERE}"
api_key = "{API_KEY_HERE}"
sample_string_bytes = f"http.header='{entity_name}'".encode("ascii")

request = base64.b64encode(sample_string_bytes)
for i in range(1, 2):

    cmd = f"""curl -X POST "https://api.zoomeye.ai/v2/search" \
    -H "API-KEY: {api_key}" \
    -H "content-type: application/json" \
    -d '{{"qbase64": "{request}","page": {i},"fields":"header,update_time,url"}}' \
    > result/output{i}.json"""
    os.system(cmd)


date_before = 3 
date_limite = datetime.now(timezone.utc) - timedelta(days=date_before)



directory = "./result"

for filename in os.listdir(directory):
    if filename.endswith(".json"):
        file_path = os.path.join(directory, filename)
        with open(file_path, "r") as file:
            content = json.load(file)
            pattern = r'(https?://[^\s]+geodis\.[^\s]+)'
            data = content.get("data")
            if data is not None:
                for item in content["data"]:
                    try:
                        date_obj = datetime.strptime(item["update_time"], "%Y-%m-%dT%H:%M:%S.%f")
                    except ValueError:
                        date_obj = datetime.strptime(item["update_time"], "%Y-%m-%dT%H:%M:%S")
                    
                    date_obj = date_obj.replace(tzinfo=timezone.utc) 
                    if date_obj < date_limite:

                        urls = re.findall(pattern, item["header"])
                        for url in urls:
                            print(url)
