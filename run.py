from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import FileResponse
import gradio as gr
import os
from main import generate_response

app = FastAPI()

# Define the directory where flagged files are saved
FLAGGED_FOLDER = "flagged"

# Ensure that the flagged folder exists
os.makedirs(FLAGGED_FOLDER, exist_ok=True)

@app.get("/")
async def root():
    return 'Hello, World!', 200

# Endpoint to upload resume files
@app.post("/resume/")
async def resume(resume: UploadFile = File(...)):
    file_path = os.path.join(FLAGGED_FOLDER, resume.filename)
    with open(file_path, "wb") as f:
        f.write(await resume.read())
    return {"filename": resume.filename}

# Endpoint to upload job description text
@app.post("/jd/")
async def jd(job_description: str):
    with open(os.path.join(FLAGGED_FOLDER, "job_description.txt"), "w") as f:
        f.write(job_description)
    return {"status": "Job description saved successfully"}

# Endpoint to serve flagged files
@app.post("/flagged_files/{file_name}")
async def get_flagged_file(file_name: str):
    file_path = os.path.join(FLAGGED_FOLDER, file_name)
    if os.path.isfile(file_path):
        return FileResponse(file_path)
    else:
        return {"error": "File not found"}

# Mount the Gradio app
app = gr.mount_gradio_app(app, generate_response, path="/evaluate_resume")

