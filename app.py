from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.get("/items/{item_name}")
# async def items(item_name):
#     return {"item_name": item_name, "route": "items"}


@app.get("/items/{item_id}")
async def items(item_id: int):
    return {"item_name": item_id, "route": "items_int"}
