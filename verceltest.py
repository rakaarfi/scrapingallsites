from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from io import StringIO
import pandas as pd

# Dummy dictionary
dummy_data = [{
    "name": "John Doe",
    "age": 29,
    "occupation": "Software Developer",
    "email": "johndoe@example.com",
}]

app = FastAPI()

@app.get("/")
def testing():
  dummy_df = pd.DataFrame(dummy_data)
  
  csv_buffer = StringIO()
  dummy_df.to_csv(csv_buffer)
  csv_buffer.seek(0)

  csv_data = "dummy.csv"
  
  return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_data}"}
    )