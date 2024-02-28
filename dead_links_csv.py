#
#      script o search for dead links on markdown files
#

import os
import re
import requests
import csv

def link_checker(link):
    try:
        req = requests.get(link)

        if req.status_code in [400, 404, 403, 408, 409, 501, 502, 503]:
            return link, "Broken", req.status_code
        else:
            return link, "Good", req.status_code
        
    except requests.exceptions.RequestException as e: 
        return link, "Error", str(e)

def check_md_files(folder_path, output_csv):
    md_files = [f for f in os.listdir(folder_path) if f.endswith('.md')]
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(['File','Link', 'Status', 'Response Code'])
        for md_file in md_files:
            with open(os.path.join(folder_path, md_file), 'r', encoding='utf-8') as file:
                content = file.read()
                links = re.findall(r'\[.*?\]\((https?://.*?)\)', content)
                for link in links:
                    #result = (md_file, link_checker(link))
                    result = (md_file, *link_checker(link))
                    csv_writer.writerow([*result])

folder_path = "folder"
output_csv  = "folder/output.csv"

for root, dirs, files in os.walk(folder_path, topdown=False):
   for name in dirs:
      print(os.path.join(root, name))      
      check_md_files(folder_path, output_csv)
