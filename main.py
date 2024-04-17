import os
from PyPDF2 import PdfReader
import gradio as gr

# Import the Python SDK
import google.generativeai as genai

# Define API key
API_KEY = "AIzaSyBeKXOpP1-_Uuxl8BseTdR19uvlAnIbGlo"

# Configure the Generative AI model
genai.configure(api_key=API_KEY)

# Function to open file from given file path
def open_file(file_path):
    return open(file_path, 'rb')

# Function to extract text from a PDF file
def extract_text_from_pdf(file_path):
    file_obj = open_file(file_path)
    reader = PdfReader(file_obj)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    file_obj.close()
    return text

# Initialize the Generative Model
model = genai.GenerativeModel('gemini-pro')

# Define a function to generate response
def generate_response(resume, job_description):
    # Dictionary to store extracted text with file names
    extracted_texts = {}
    extracted_text = extract_text_from_pdf(resume.name)
    extracted_texts[resume.name] = extracted_text
    
    # Dictionary to store model responses
    model_responses = {}
    
    # Iterate through each file and pass its text to the model
    for filename, text in extracted_texts.items():
        response = model.generate_content(prompt + f"Resume: {filename}\n\n{text}\n\nJob Description:\n{job_description}")
        model_responses[filename] = response.text
    
    return model_responses[resume.name]

# Define the prompt
prompt = """Dear HR Professional,

As an expert in resume evaluation, your task is to assess the alignment between each resume and the job description provided below. Please consider the following key aspects while evaluating each resume:

Skills: Review the skills mentioned in the resumes and compare them with the required skills outlined in the job description.
Experience: Evaluate the candidate's experience level and see if it matches the experience requirements specified in the job description.
Qualifications: Assess the candidate's qualifications and qualifications required for the job role.
After considering these aspects, provide a match percentage indicating how closely each resume matches the job description. This match percentage will help in identifying the most suitable candidates for the role.

Thank you for your expertise and attention to detail in this evaluation process."""

# Create Gradio Interface
resume_input = gr.File(label="Upload Resume")
job_description_input = gr.Textbox(label="Job Description", type="text")
interface = gr.Interface(fn=generate_response, inputs=[resume_input, job_description_input], outputs="text", title="Resume Matcher", description="Assess the alignment between a resume and a job description.")

# Launch Gradio Interface
interface.launch()
