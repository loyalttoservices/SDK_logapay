import requests

from logapay.exceptions import APINotAuthenticated, APINotAuthorized, LogApayException

        
        
class PaymentResponse:
    """Payment reponse to be sent via payment method
    """
    def __init__(self, data) -> None:
        self._data = data
        
    def get_response(self):
        return self._data.get("response", {})
    
    def __str__(self) -> str:
        return "Response => " + self._data.get('redirect_url', '')
    
    

class LogapayAPI:
    """LogApay SDK for interact with LogApi api.
    """
    BASE_ENDPOINT = "https://logapay.net"
    BASE_ENDPOINT_TEST = "http://localhost:8000"
    
    TRANSFER_URL = "/v1/transfer"
    CREATE_URL ="/v1/create"
    
    
    def __init__(self, token: str, debug=False) -> None:
        self._token = token
        self._base = LogapayAPI.BASE_ENDPOINT_TEST if debug else LogapayAPI.BASE_ENDPOINT
        self.headers = {
            "Authorization": "token " + self._token,
            "Content-Type": "application/json"
        }
        

    def payment(self, amount:float, orderId: str):
        response = requests.post(self._base + self.CREATE_URL, 
            json={"amount": amount, "orderId": orderId},
            headers=self.headers
        )
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', "")
        
        if "application/json" in content_type:
            data = response.json()
        else:
            data = {"status": status_code, "detail": response.text}
        
        detail = data.get("detail", "")
            
        if status_code >= 400 and status_code <= 499:
            _status_code = data.get("status", status_code)
            if _status_code == 401:
                raise APINotAuthenticated(detail)
            elif _status_code == 403:
                raise APINotAuthorized(detail)
            else:
                raise LogApayException(detail)
        elif status_code >= 500 and status_code <= 599:
            raise LogApayException(detail)
        else:
            return PaymentResponse(data=data)

        
           
    
    def transfer(self, amount: float, receiver: str, desc: str = ""):
        response = requests.post(self._base + self.TRANSFER_URL, 
            json={"amount": amount, "receiver": receiver, "desc": desc},
            headers=self.headers
        )
        status_code = response.status_code
        content_type = response.headers.get('Content-Type', "")
        
        if "application/json" in content_type:
            data = response.json()
        else:
            data = {"status": status_code, "detail": response.text}
        
        detail = data.get("detail", "")
            
        if status_code >= 400 and status_code <= 499:
            _status_code = data.get("status", status_code)
            if _status_code == 401:
                raise APINotAuthenticated(detail)
            elif _status_code == 403:
                raise APINotAuthorized(detail)
            else:
                raise LogApayException(detail)
        elif status_code >= 500 and status_code <= 599:
            raise LogApayException(detail)
        else:
            return data
        
        