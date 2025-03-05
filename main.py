from fastapi import FastAPI
from routers import orders, order_item
from utils.database import init_db
from Users.api import router as UserAPI 
from Address.api import router as AddressAPI
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

init_db()

app.include_router(UserAPI)
app.include_router(AddressAPI)

PORT = int(os.getenv("PORT", 14565))  

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=PORT, reload=True)
