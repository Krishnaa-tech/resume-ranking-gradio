from fastapi import FastAPI
import gradio as gr

from main import interface

app = FastAPI()

@app.get("/")
async def root():
    return 'Gradio app is running at /resume', 200

# Mount the Gradio app
app = gr.mount_gradio_app(app, interface, path="/resume")

