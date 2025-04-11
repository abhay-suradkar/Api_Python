from .schemas import PaymentRequest
from urllib.parse import urlencode

def create_instamojo_payment(data: PaymentRequest):
    base_url = "https://www.instamojo.com/@abhaysuradkar8"
    
    query_params = {
        "data_readonly": "email,phone",
        "email": data.email,
        "phone": data.phone,
        "buyer_name": data.buyer_name,
        "amount": data.amount
    }

    final_url = f"{base_url}?{urlencode(query_params)}"

    return {"payment_url": final_url}
