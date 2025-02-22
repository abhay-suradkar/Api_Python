from fastapi import FastAPI
from routers import users, address, orders, order_item
from database import init_db

app = FastAPI()

# Initialize the database
init_db()

# Include routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(address.router, prefix="/address", tags=["Address"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(order_item.router, prefix="/order_item", tags=["Order_Item"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
