from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def testing():
  return 1