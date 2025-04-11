from fastapi import FastAPI
from utils.database import init_db
from Users.api import router as UserAPI 
from Address.api import router as AddressAPI
from Order_Item.api import router as OrderItemAPI
from Payment.api import router as PaymentAPI  # ✅ Add this line

import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

init_db()

# Include all routers
app.include_router(UserAPI)
app.include_router(AddressAPI)
app.include_router(OrderItemAPI)
app.include_router(PaymentAPI)  # ✅ Include the payment route

PORT = int(os.getenv("PORT", 14565))  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)
