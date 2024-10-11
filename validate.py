import requests
from bs4 import BeautifulSoup
import re
import csv
import json
import xml.etree.ElementTree as ET

def url_parser(content):
    urls = re.findall(r'https?://[^\s]+', content)
    return urls

def validate_phishing(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        html = response.text
        links = html_parser(html) 
        isPhising = check_links(links)
        return isPhising
    except requests.exceptions.RequestException as e:
        print('Error fetching the HTML:', e)

def html_parser(content):
    http_pattern = r'https?://[^/]+'
    http_links = re.findall(http_pattern, content)

    links = set()
    for link in http_links:
        if not re.search(r'\.(png|jpg|jpeg|gif|bmp)$', link, re.IGNORECASE):
            links.add(link)
    return links
        
def check_links(links):
    # csv file
    with open('./verify_list.csv', 'r', encoding='utf-8') as csvfile:   #   file path 수정 필요
        csv_data = csv.reader(csvfile)
        csv_links = set()
        
        for row in csv_data:
            for item in row:
                csv_links.add(item.strip()) 

    if len(links.intersection(csv_links)) > 0:
        return True

    # json file
    with open('./verify_list.json', 'r', encoding='utf-8') as jsonfile:
        json_data = json.load(jsonfile)
        json_links = set()
        
        for item in json_data:
            json_links.add(item['url'].strip())

    if len(links.intersection(json_links)) > 0:
        return True

    # xml file
    tree = ET.parse('./verify_list.xml')
    root = tree.getroot()
    xml_links = set()
    for link in root.findall('.//url'):
        xml_links.add(link.text.strip())    

    if len(links.intersection(json_links)) > 0:
        return True

    return False



