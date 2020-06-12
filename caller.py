import requests
from pprint import pprint

url = "http://monitoring-env.eba-kmh3ybxg.ap-south-1.elasticbeanstalk.com"

def create():
    resp = requests.post(f"{url}/create-user", json={"username": "vasu", "password": "vasu", "email": "<email-id>"})
    print(resp.json())

def add():
    resp = requests.post(f"{url}/add-instances", json={"username": "vasu", "password": "vasu",
                                                                      "InstanceId":'<instance-id>'})
    print(resp.json())

def get():
    resp = requests.get(f"{url}/get-instances", json={"username": "vasu", "password": "vasu"})
    print(resp.json())

def halt():
    resp = requests.post(f"{url}/halt", json={"username": "vasu", "password": "vasu", "InstanceId": ['<instance-id>']})
    print(resp.json())

def metrics():
    resp = requests.get(f"{url}/api/fork/metrics", json={"username": "vasu", "password": "vasu", "attributes": ["CPUUtilization", "NetworkIn"]}, verify=False)
    pprint(resp.json())

def meta():
    resp = requests.get(f"{url}/api/fork/metadata", json={"username": "vasu", "password": "vasu"})
    pprint(resp.json())

def setp():
    resp = requests.post(f"{url}/set/interval", json={"username": "vasu", "password": "vasu", "interval": 1})
    pprint(resp.json())

def getdata():
    resp = requests.get(f"{url}/get-data", json={"username": "vasu", "password": "vasu"})
    pprint(resp.json())

def thresh():
    resp = requests.post(f"{url}/check-threshold", json={"username": "vasu", "password": "vasu"})
    pprint(resp.json())

#create()
#add()
#metrics()
#meta()
#halt()
#setp()
#getdata()
#get()
#thresh()
