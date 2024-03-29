from fastapi import FastAPI

from address_book.api.endpoints import addresses

from address_book.database import engine, Base

import uvicorn


# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include router
app.include_router(addresses.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
