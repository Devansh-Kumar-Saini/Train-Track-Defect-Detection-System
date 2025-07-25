from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from ultralytics import YOLO
from PIL import Image
import numpy as np
import gradio as gr
import uvicorn
import cv2
import base64
from fastapi.responses import JSONResponse

# Load YOLOv8 model
model = YOLO("best.pt", task='detect')  # Using the correct .pt model file with explicit task

# Gradio function
def detect_defect(image):
    results = model.predict(image, conf=0.5, verbose=False)
    result = results[0]
    # Get the original image
    img = result.orig_img.copy()
    
    # Draw only boxes with confidence scores
    for box, conf in zip(result.boxes.xyxy, result.boxes.conf):
        x1, y1, x2, y2 = box.tolist()
        
        # Draw rectangle with no labels
        cv2.rectangle(img, 
                     (int(x1), int(y1)), 
                     (int(x2), int(y2)), 
                     (0, 255, 0), 2)
        
        # Add only confidence percentage
        conf_text = f'{int(conf * 100)}%'
        # Position confidence score inside the box at the top
        text_x = int(x1) + 5
        text_y = int(y1) + 20
        cv2.putText(img, 
                   conf_text,
                   (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, 
                   (255, 255, 255), 
                   2)  # White text with outline
        cv2.putText(img, 
                   conf_text,
                   (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 
                   0.6, 
                   (0, 255, 0), 
                   1)  # Green text
    
    return Image.fromarray(img)

# FastAPI app setup
app = FastAPI()

# Mount static and template folders
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes for all frontend pages
@app.get("/", response_class=HTMLResponse)
async def serve_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/demo", response_class=HTMLResponse)
async def serve_demo(request: Request):
    return templates.TemplateResponse("demo.html", {"request": request})

@app.get("/about", response_class=HTMLResponse)
async def serve_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get("/technical", response_class=HTMLResponse)
async def serve_technical(request: Request):
    return templates.TemplateResponse("technical.html", {"request": request})

# API endpoint for predictions
@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    import io

    img = Image.open(file.file).convert("RGB")
    results = model.predict(img, conf=0.5, verbose=False)
    result = results[0]
    img_np = result.orig_img.copy()

    confidences = []
    for box, conf in zip(result.boxes.xyxy, result.boxes.conf):
        x1, y1, x2, y2 = box.tolist()
        cv2.rectangle(img_np, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        conf_text = f'{int(conf * 100)}%'
        text_x = int(x1) + 5
        text_y = int(y1) + 20
        cv2.putText(img_np, conf_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)
        cv2.putText(img_np, conf_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 1)
        confidences.append(float(conf))

    # Convert image to base64
    pil_img = Image.fromarray(img_np)
    buf = io.BytesIO()
    pil_img.save(buf, format='PNG')
    img_bytes = buf.getvalue()
    img_base64 = base64.b64encode(img_bytes).decode('utf-8')

    # Prepare response
    if confidences:
        max_conf = max(confidences)
        found = True
    else:
        max_conf = 0
        found = False

    return JSONResponse(content={
        "image": img_base64,
        "defect_found": found,
        "confidence": round(max_conf * 100, 2)
    })

# Mount Gradio app separately
gradio_interface = gr.Interface(
    fn=detect_defect,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="Railway Track Defect Detection",
    description="Upload an image to detect defective and non-defective tracks using YOLOv8."
)

app = gr.mount_gradio_app(app, gradio_interface, path="/gradio")

# Run with Uvicorn
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7860)