from sdk.logapay import LogapayAPI



def test_api():
    TOKEN = "f2df9c9f-e82d-499c-baf5-bc7853f7d21d"
    test = LogapayAPI(TOKEN)
    
    retData = test.payment(1200, "67908765")
    print(retData)
    



if __name__ == "__main__":
    test_api()