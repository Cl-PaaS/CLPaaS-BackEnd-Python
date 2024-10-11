import requests
import os

def get_verify_list():
    response_csv = requests.get("http://data.phishtank.com/data/online-valid.csv")
    response_json = requests.get("http://data.phishtank.com/data/online-valid.json")  
    response_xml = requests.get("http://data.phishtank.com/data/online-valid.xml")

    if response_csv.status_code == 404 or response_csv.status_code == 429:
        print("CSV file NOT Updated")
    elif response_csv.status_code == 200:
        with open('./verify_list.csv', 'w', encoding='utf-8') as f:
            f.write(response_csv.text)
        print("CSV file Updated")

    if response_json.status_code == 404 or response_json.status_code == 429:
        print("JSON file NOT Updated")
    elif response_json.status_code == 200:
        with open('./verify_list.json', 'w', encoding='utf-8') as f:
            f.write(response_json.text)
        print("JSON file Updated")

    if response_xml.status_code == 404 or response_xml.status_code == 429:
        print("XML file NOT Updated")
    elif response_xml.status_code == 200:
        with open('./verify_list.xml', 'w', encoding='utf-8') as f:
            f.write(response_xml.text)
        print("XML file Updated")

    return f"csv: {response_csv.status_code}, json: {response_json.status_code}, xml: {response_xml.status_code}"