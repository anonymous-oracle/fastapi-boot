from fastapi import FastAPI

app = FastAPI()

# the file_path datatype specified for the path variable automatically parses the filepath
@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
