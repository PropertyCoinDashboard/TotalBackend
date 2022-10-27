import requests 



def test():
    url = "https://api.upbit.com/v1/market/all?isDetails=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    for d in response.json():
        print(d)
    
                
