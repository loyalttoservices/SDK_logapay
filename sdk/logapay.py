import requests



class NotAuthenticated(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
        
class NotAuthorized(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args) 
        
        
class PaymentResponse:
    def __init__(self, data) -> None:
        self._data = data
        
    def get_response(self):
        return self._data.get("response", {})
    
    def __str__(self) -> str:
        return f"Response => {self._data.get("redirect_url", "")}"
    
    

class LogapayAPI:
    """_summary_
    """
    BASE_ENDPOINT = "https://logapay.net"
    BASE_ENDPOINT_TEST = "http://localhost:8000"
    
    
    def __init__(self, token: str) -> None:
        self._token = token
        self._create_url = LogapayAPI.BASE_ENDPOINT_TEST + "/v1/create"
        self._transfer_url = LogapayAPI.BASE_ENDPOINT_TEST + "/v1/transfer"
        self.headers = {
            "Authorization": "token " + self._token,
            "Content-Type": "application/json"
        }

    def payment(self, amount:float, orderId: str):
        response = requests.post(self._create_url, 
            json={"amount": amount, "orderId": orderId},
            headers=self.headers
        )
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', "")
        data = response.json()
        detail = data.get("detail") if "application/json" in content_type else ""
        
        if status_code >= 400 and status_code <= 499:
            _status_code = data.get("status", status_code)
            if _status_code == 401:
                raise NotAuthenticated(detail)
            elif _status_code == 403:
                raise NotAuthorized(detail)
            else:
                raise Exception(detail)
        elif status_code >= 500 and status_code <= 599:
            raise Exception(detail)
        else:
           return PaymentResponse(data=data)
           
    
    def transfer(self, amount: float, receiver: str, desc: str = ""):
        response = requests.post(self._transfer_url, 
            json={"amount": amount, "receiver": receiver, "description": desc},
            headers=self.headers
        )
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', "")
        print(status_code, content_type)
        data = response.json()
        detail = data.get("detail") if "application/json" in content_type else ""
        
        if status_code >= 400 and status_code <= 499:
            _status_code = data.get("status", status_code)
            if _status_code == 401:
                raise NotAuthenticated(detail)
            elif _status_code == 403:
                raise NotAuthorized(detail)
            else:
                raise Exception(detail)
        elif status_code >= 500 and status_code <= 599:
            raise Exception(detail)
        else:
            return data
        
        