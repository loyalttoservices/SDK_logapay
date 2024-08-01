


## Overview

The LogapayAPI SDK is designed for interacting with the LogApay payment gateway API. It provides methods to perform payment creation and money transfer operation.


### Installation

- From github

    - pip install git+https://github.com/loyalttoservices/SDK_logapay.git


## Classes


### PaymentResponse

Represents a response received from the LogApay API for payment.

Methods

Initializes the PaymentResponse with response data.

- `__init__(self, data)`


Retrieves the "response" field from the response data.

- `get_response(self)`

Returns a string representation of the response, specifically the "redirect_url" if available.

- `__str__(self)`




### LogApayException

Base exception class for all exceptions related to LogApay.

- Inheritance
    - Exception

### APINotAuthenticated

Exception raised when the API authentication fails.

- Inheritance
    - LogApayException


### APINotAuthorized

Exception raised when the API authorization fails.

- Inheritance
    - LogApayException


### LogapayAPI

Main class for interacting with the LogApay API. for now only support `MONCASH`

Methods

Initializes the LogapayAPI instance with an authentication token.

- `__init__(self, token: str, debug=False)`


Creates a payment request.

- `payment(self, amount: float, orderId: str)`

    - Parameters:

        - amount (float): The amount to be paid.
        - orderId (str): The unique identifier for the order.

    - Returns:

        - PaymentResponse: The response from the API if the request is successful.

    - Raises:

        - APINotAuthenticated: If the authentication fails (401 status code).
        - APINotAuthorized: If authorization fails (403 status code).
        - LogApayException: For server errors (500-599 status codes).  



Transfers money to a receiver.

- `transfer(self, amount: float, receiver: str, desc: str = "")`

    - Parameters:

        - amount (float): The amount to be transferred.
        - receiver (str): The recipient's identifier.
        - desc (str, optional): Description for the transfer.

    - Returns:

        - dict: The response data from the API if the request is successful.

    - Raises:

        - APINotAuthenticated: If the authentication fails (401 status code).
        - APINotAuthorized: If authorization fails (403 status code).
        - LogApayException: For server errors (500-599 status codes).


Retrieve Transaction Details.

- `retrievePayment(self, moncashId=None, moncashOrderId=None, transactionId=None):`

    - Parameters:

        - moncashOrderId (optional): The Moncash Order ID to retrieve transaction details (request moncash directly).
        - moncashId (optional): The Moncash ID to retrieve transaction detail (request moncash directly).
        - transactionId (optional): transaction ID to retrieve transaction details.

    _note: if all parameters provided. `moncashId` is checked first, `moncashOrderId`, `transactionId`._


    - Returns:

        - dict: The response data from the API if the request is successful.
        ```{'path': '/Api/v1/RetrieveTransactionPayment', 'payment': {'reference': 'xxxxxxx', 'transactionId': 'xxxxxx', 'cost': 50, 'message': 'successful', 'payer': '509xxxxxx'}, 'timestamp': 1722538220300, 'status': 200}```

    - Raises:

        - APINotAuthenticated: If the authentication fails (401 status code).
        - APINotAuthorized: If authorization fails (403 status code).
        - LogApayException: For server errors (500-599 status codes).


### Usage Example


```
from logapay.exceptions import *
from logapay.logapay import LogapayAPI

# Initialize the API client with your token
api_client = LogapayAPI(token="your_api_token")

# Create a payment
try:
    payment_response = api_client.payment(amount=100.0, orderId="order123")
    print(payment_response.get_response())
except APINotAuthenticated:
    print("Authentication failed.")
except APINotAuthorized:
    print("Authorization failed.")
except LogApayException as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"General error: {e}")

# Transfer money
try:
    transfer_response = api_client.transfer(amount=50.0, receiver="receiver_id", desc="Payment for services")
    print(transfer_response)
except APINotAuthenticated:
    print("Authentication failed.")
except APINotAuthorized:
    print("Authorization failed.")
except LogApayException as e:
    print(f"API error: {e}")
except Exception as e:
    print(f"General error: {e}")

```



