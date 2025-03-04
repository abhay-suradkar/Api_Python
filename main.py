from fastapi import FastAPI
from routers import orders, order_item
from utils.database import init_db
from Users.api import router as UserAPI 
from Address.api import router as AddressAPI

app = FastAPI()
 
init_db()
app.include_router(UserAPI)
app.include_router(AddressAPI)
# app.include_router(address.router, prefix="/address", tags=["Address"])
# app.include_router(orders.router, prefix="/orders", tags=["Orders"])
# app.include_router(order_item.router, prefix="/order_item", tags=["Order_Item"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
