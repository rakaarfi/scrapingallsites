from fastapi import FastAPI
from fastapi.responses import FileResponse
from io import StringIO
import pandas as pd

# Dummy dictionary
dummy_data = {
    "name": "John Doe",
    "age": 29,
    "occupation": "Software Developer",
    "email": "johndoe@example.com",
    "skills": ["Python", "JavaScript", "React", "Django"],
    "experience": {
        "company_1": {
            "name": "Tech Corp",
            "role": "Frontend Developer",
            "years": 2
        },
        "company_2": {
            "name": "DevSolutions",
            "role": "Full Stack Developer",
            "years": 1
        }
    },
    "hobbies": ["Reading", "Traveling", "Photography"]
}

app = FastAPI()

@app.get("/")
def testing():
  dummy_df = pd.DataFrame(dummy_data)
  csv_buffer = StringIO()
  dummy_df.to_csv(csv_buffer, index=False)
  csv_buffer.seek(0)

  csv_data = "dummy.csv"
  
  return  FileResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={csv_data}"}
    )