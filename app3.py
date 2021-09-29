from typing import Optional
from fastapi import FastAPI

app = FastAPI()

# the file_path datatype specified for the path variable automatically parses the filepath
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


# When creating path operations, you can find situations where you have a fixed path.

# Like /users/me, let's say that it's to get data about the current user.

# And then you can also have a path /users/{user_id} to get data about a specific user by some user ID.

# Because path operations are evaluated in order, you need to make sure that the path for /users/me is declared before the one for /users/{user_id}:


@app.get("/users/me")
async def read_user_me():

    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# Otherwise, the path for /users/{user_id} would match also for /users/me, "thinking" that it's receiving a parameter user_id with a value of "me"

# QUERY PARAMS - predefined params, know what is allowed to be passed; Optional is a param which can be given a default value and not be passed
@app.get("/query_params")
async def get_params(param1: int, param2: int, opt: Optional[str] = None):
    return {"param1": param1, "param2": param2, "opt": opt}
