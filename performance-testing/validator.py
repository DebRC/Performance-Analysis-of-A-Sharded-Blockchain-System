import requests, os

def getNumberOfValidators():
    url = f"{os.getenv('PROXY_NETWORK')}/v1.0/validator/statistics"
    response = requests.get(url)
    if response.status_code == 200:
        return len((response.json()['data']['statistics']).keys())
    else:
        print("Error:", response.status_code)
        return -1
    