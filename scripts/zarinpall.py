import requests
import json


class ZarinPalSandbox:
    _payment_request_url = "https://sandbox.zarinpal.com/pg/v4/payment/request.json"
    _payment_verify_url = "https://sandbox.zarinpal.com/pg/v4/payment/verify.json"
    _payment_page_url = "https://sandbox.zarinpal.com/pg/StartPay/"
    _callback_url = "http://redreseller.com/verify"

    def __init__(self, merchant_id):
        self.merchant_id = merchant_id

    def payment_request(self, amount, description="پرداختی کاربر"):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": str(amount),
            "callback_url": self._callback_url,
            "Description": description,
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(
            self._payment_request_url, headers=headers, data=payload)

        return response.json()

    def payment_verify(self,amount,authority):
        payload = {
            "merchant_id": self.merchant_id,
            "amount": amount,
            "authority": authority
        }
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.post(self._payment_verify_url, headers=headers, data=payload)
        return response.json()

    def generate_payment_url(self,authority):
        return self._payment_page_url + authority



if __name__ == "__main__":
    zarinpal = ZarinPalSandbox(merchant_id="36c2a45d-6ca8-48aa-81ba-def6d628351d")
    response =zarinpal.payment_request(15000)
    
    print(response)
    input("proceed to generating payment url?")
    print(zarinpal.generate_payment_url(response["authority"]))
    
    input("check the payment?")
    
    response = zarinpal.payment_verify(15000,response["authority"])
    print(response)
    