from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


# defining request body
class Item(BaseModel):
    id: int
    name: str
    price: float
    tax: Optional[float] = None
    description: Optional[str] = None

    def __str__(self) -> str:
        repr_str = f"\n**************************************************************\nID: {self.id}\tNAME: {self.name}\tPRICE: {self.price}"
        if self.tax != None:
            repr_str += f"\tTAX: {self.tax}"
        if self.description != None:
            repr_str += f"\nDESCRIPTION : {self.description}\n**************************************************************\n"
        return repr_str


class Item2(BaseModel):
    name: str
    price: float
    tax: Optional[float] = None
    description: Optional[str] = None

    def __str__(self) -> str:
        repr_str = f"\n**************************************************************\nNAME: {self.name}\tPRICE: {self.price}"
        if self.tax != None:
            repr_str += f"\tTAX: {self.tax}"
        if self.description != None:
            repr_str += f"\nDESCRIPTION : {self.description}\n**************************************************************\n"
        return repr_str


app = FastAPI()

# notice the post request decorator
@app.post("/items")
async def items(item: Item):
    print(item)
    item_dict = item.dict()
    if item_dict.get("tax") != None:
        price_post_tax = item_dict.get("price") + item_dict.get("tax")
        item_dict.update({"price_post_tax": price_post_tax})
    return {"ITEM": item_dict}


# # request body with path params
# @app.put("/items/{item_id}")
# async def items2(item_id: int, item: Item2):
#     item_dict = item.dict()
#     if item_dict.get("tax") != None:
#         price_post_tax = item_dict.get("price") + item_dict.get("tax")
#         item_dict.update({"price_post_tax": price_post_tax})
#     return {"ITEM": {"id": item_id, **item_dict}}


# request body with path params and query params
@app.post("/items/{item_id}")
async def items3(item_id: int, item: Item2, q: Optional[str] = None):
    item_dict = item.dict()
    if item_dict.get("tax") != None:
        price_post_tax = item_dict.get("price") + item_dict.get("tax")
        item_dict.update({"price_post_tax": price_post_tax})
    result = {"ITEM": {"id": item_id, **item_dict}}
    if q != None:
        result.update({"query": q})
    return result
