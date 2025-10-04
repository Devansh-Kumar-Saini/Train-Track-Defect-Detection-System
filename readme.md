## Project Structure

yolo_app/
├── static/                     # Static files (CSS, JS, images, etc.)
├── templates/                  # HTML templates for rendering views
├── venvAIML/                   # Python virtual environment
├── .DS_Store                   # macOS system file (can be ignored or deleted)
├── .gitignore                  # Git ignore rules
├── app.py                      # Main application script
├── best.pt                    # YOLO model file
├── readme.md                   # Project documentation
└── requirements.txt            # Python dependencies

## Features

- **Object Detection**: Upload images and detect objects using YOLO.
- **Interactive Frontend**: Built with HTML, CSS, and JavaScript.
- **Pre-trained Models**: Includes pre-trained YOLO models for object detection.

## Requirements

- Python 3.9 or later
- Virtual environment (`venv`) with required dependencies installed

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/Devansh-Kumar-Saini/Train-Track-Defect-Detection-System.git
   cd Train-Track-Defect-Detection-System
   ```

# Optional (Virtual Environment)
source venvAIML/Scripts/activate  # On Windows
source venvAIML/bin/activate      # On macOS/Linux


2. Installing Libraries 
pip install -r requirements.txt

3. Run the Application
python app.py
