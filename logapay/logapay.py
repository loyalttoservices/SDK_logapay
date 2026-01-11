import requests

from logapay.exceptions import APINotAuthenticated, APINotAuthorized, LogApayException


class PaymentResponse:
    """Payment reponse to be sent via payment method"""

    def __init__(self, data) -> None:
        self._data = data

    def get_response(self):
        return self._data.get("response", {})

    def __str__(self) -> str:
        return "Response => " + self._data.get("redirect_url", "")


class LogapayAPI:
    """LogApay SDK for interact with LogApi api."""

    BASE_ENDPOINT = "https://logapay.net"
    BASE_ENDPOINT_TEST = "http://localhost:8000"

    TRANSFER_URL = "/v1/transfer"
    CREATE_URL = "/v1/create"
    RETRIEVORDERPAYMENT_URL = "/v1/RetrieveOrderPayment"
    LIST_TRANSACTION_URL="/v1/list-transactions"
    PREFUND_LIST="/v1/list-prefund"
    APPLICATION="/v1/application"
    def __init__(self, token: str, debug=False) -> None:
        self._token = token
        self._base = (
            LogapayAPI.BASE_ENDPOINT_TEST if debug else LogapayAPI.BASE_ENDPOINT
        )
        self.headers = {
            "Authorization": "token " + self._token,
            "Content-Type": "application/json",
        }

    def payment(self, amount: float, orderId: str, method: str = "moncash"):
        response = requests.post(
            self._base + self.CREATE_URL,
            json={"amount": amount, "orderId": orderId, "payment_method": method},
            headers=self.headers,
        )
        status_code = response.status_code
        content_type = response.headers.get("Content-Type", "")

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

    def transfer(self, amount: float, receiver: str, desc: str = "", method: str = "moncash"):
        response = requests.post(
            self._base + self.TRANSFER_URL,
            json={
                "amount": amount,
                "receiver": receiver,
                "desc": desc,
                "payment_method": method,
            },
            headers=self.headers,
        )
        status_code = response.status_code
        content_type = response.headers.get("Content-Type", "")

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
        

    def retrievePayment(self, moncashId=None, moncashOrderId=None, transactionId=None):
        if moncashId is None and moncashOrderId is None and transactionId is None:
            raise LogApayException(
                "Provide one of 'moncashOrderId', 'transactionId', 'moncashId'"
            )

        if moncashId:
            params = {"moncashId": moncashId}
        elif moncashOrderId:
            params = {"moncashOrderId": moncashOrderId}
        elif transactionId:
            params = {"transactionId": transactionId}

        response = requests.get(
            self._base + self.RETRIEVORDERPAYMENT_URL,
            params=params,
            headers=self.headers,
        )
        
        status_code = response.status_code
        content_type = response.headers.get("Content-Type", "")

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



    def getTransactionsByDateRange(
        self,
        start_date=None,
        end_date=None,
        transaction_type=None,
        phone_number=None,
        method: str = "all",
    ):
        """
        Récupère les transactions dans une plage de dates avec des filtres optionnels
        """
        # Validation des paramètres
        if not start_date and not end_date:
            raise LogApayException("Au moins une date (start_date ou end_date) doit être fournie")
        
        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        
        if transaction_type:
            params['type'] = transaction_type
        if phone_number:
            params['number'] = phone_number
        if method:
            params['payment_method'] = method
        
        try:
            response = requests.get(
                self._base + self.LIST_TRANSACTION_URL,
                params=params,
                headers=self.headers,
               
            )
            
            # Gestion de la réponse
            status_code = response.status_code
            content_type = response.headers.get("Content-Type", "")
            
            if "application/json" in content_type:
                data = response.json()
            else:
                data = {"status": status_code, "detail": response.text}
            
            if status_code >= 400:
                detail = data.get("detail", "Erreur inconnue")
                if status_code == 401:
                    raise APINotAuthenticated(detail)
                elif status_code == 403:
                    raise APINotAuthorized(detail)
                else:
                    raise LogApayException(detail)
            
            return data
        
        except requests.exceptions.RequestException as e:
            raise LogApayException(f"Erreur réseau: {str(e)}")
        except ValueError as e:
            raise LogApayException(f"Erreur de parsing JSON: {str(e)}")
        


    def getPrefundsByDateRange(self, start_date=None, end_date=None):
        """
        Récupère les prefunds dans une plage de dates avec des filtres optionnels
        
        """
        # Validation des paramètres minimum
        if not start_date and not end_date:
            raise LogApayException("Au moins une date (start_date ou end_date) doit être fournie")

        params = {}
        if start_date:
            params['start_date'] = start_date
        if end_date:
            params['end_date'] = end_date
        

        try:
            response = requests.get(
                self._base + self.PREFUND_LIST,  # Adaptez l'URL à votre endpoint
                params=params,
                headers=self.headers
               
            )
            
            # Gestion de la réponse
            status_code = response.status_code
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = response.json()
            else:
                data = {"status": status_code, "detail": response.text}

            if status_code >= 400:
                detail = data.get("detail", "Erreur inconnue")
                if status_code == 401:
                    raise APINotAuthenticated(detail)
                elif status_code == 403:
                    raise APINotAuthorized(detail)
                else:
                    raise LogApayException(detail)
            
            return data

        except requests.exceptions.RequestException as e:
            raise LogApayException(f"Erreur réseau: {str(e)}")
        except ValueError as e:
            raise LogApayException(f"Erreur de parsing JSON: {str(e)}")



    def getApplicationDetails(self, include_transactions=True):
        """
        Récupère les détails de l'application associée, y compris les statistiques et transactions récentes
    """
        try:
            params = {
                'include_transactions': str(include_transactions).lower()
            }
            
            response = requests.get(
                self._base + self.APPLICATION,
                params=params,
                headers=self.headers,
               
            )
            
            # Gestion de la réponse
            status_code = response.status_code
            content_type = response.headers.get("Content-Type", "")

            if "application/json" in content_type:
                data = response.json()
            else:
                data = {"status": status_code, "detail": response.text}

            if status_code >= 400:
                detail = data.get("detail", "Erreur inconnue")
                if status_code == 401:
                    raise APINotAuthenticated(detail)
                elif status_code == 403:
                    raise APINotAuthorized(detail)
                else:
                    raise LogApayException(detail)
            
            return data

        except requests.exceptions.RequestException as e:
            raise LogApayException(f"Erreur réseau: {str(e)}")
        except ValueError as e:
            raise LogApayException(f"Erreur de parsing JSON: {str(e)}")
