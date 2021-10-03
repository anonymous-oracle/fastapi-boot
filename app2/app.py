from fastapi import FastAPI

app = FastAPI()


@app.get("/blog?limit=10&published=true")
async def index(limit, published: bool):  # accept query parameters
    if published:
        return {"data": [f"{limit} published blogs from db"]}
    else:
        return {'data':[f"{limit} blogs from db"]}

@app.get("/blog/unpublished")
async def unpublished():
    return {"data": ["all unpublished blogs"]}


# NOTE: ALWAYS PUT DYNAMIC ROUTING PATHS IN THE END AFTER STATIC ROUTING PATHS
@app.get("/blog/{blog_id}")
async def show(blog_id: int):
    # fetch blog with id = blog_id
    return {"data": blog_id}


@app.get("/blog/{blog_id}/comments")
async def comments(blog_id: int):
    # get comments for blog with id = blog_id
    return {"blog_id": blog_id, "comments": ["comments"]}
