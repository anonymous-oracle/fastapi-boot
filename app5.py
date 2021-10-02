from fastapi import FastAPI, Query
from typing import List, Optional

app = FastAPI()

items_db = {"items": []}

# performing additional validation for query parameters
#  the min_length and the max_length parameters further validate the query data passed to the route, works only on strings
# the regex filters out the characters 'fixedquery' and nothing else contained in the query
@app.get("/items")
async def read_items(
    q: Optional[str] = Query(None, max_length=50, min_length=3, regex=r"^fixedquery$")
):
    if q != None:
        list_ = items_db.get("items")
        list_.append({"item_id": q})
        items_db.update({"items": list_})
    return items_db


# default values
@app.get("/items2")
async def read_items2(
    q: Optional[str] = Query(
        "default", max_length=50, min_length=3, regex=r"^fixedquery$"
    )
):
    if q != None:
        list_ = items_db.get("items")
        list_.append({"item_id": q})
        items_db.update({"items": list_})
    return items_db


# required parameter
@app.get("/items3")
async def read_items(q: Optional[str] = Query(..., max_length=50)):
    if q != None:
        list_ = items_db.get("items")
        list_.append({"item_id": q})
        items_db.update({"items": list_})
    return items_db


# query parameter list with multiple values
# Example request: http://127.0.0.1:8000/items4?q=new_item&q=new_item2&q=new_item3
@app.get("/items4")
async def read_items(q: Optional[List[str]] = Query(None)):
    query_items = {"q": q}
    return query_items

# query parameter list with multiple values - another way
# Example request: http://127.0.0.1:8000/items4?q=new_item&q=new_item2&q=new_item3
@app.get("/items4")
async def read_items(q: Optional[List] = Query([])):
    query_items = {"q": q}
    return query_items

# query parameter list with default values
# Example request: http://127.0.0.1:8000/items4?q=new_item&q=new_item2&q=new_item3
@app.get("/items4")
async def read_items(q: Optional[List[str]] = Query(["foo", "bar"])):
    query_items = {"q": q}
    return query_items
