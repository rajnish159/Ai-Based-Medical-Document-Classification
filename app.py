from flask import Flask, render_template, request
import os
import pytesseract
from PIL import Image

app = Flask(__name__)

# Specify the Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/login')
def login():
    return render_template('login.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'uploadedFile' not in request.files:
        return render_template('upload.html', error='No file part')

    file = request.files['uploadedFile']

    if file.filename == '':
        return render_template('upload.html', error='No selected file')

    try:
        # Save the uploaded file
        file_path = 'static/uploads/' + file.filename
        file.save(file_path)

        # Perform OCR
        text, document_type = perform_ocr(file_path)

        return render_template('upload.html', text=text, document_type=document_type, image_path=file_path)

    except Exception as e:
        return render_template('upload.html', error=str(e))

def perform_ocr(image_path):
    # Load the image
    img = Image.open(image_path)

    # Perform OCR
    text = pytesseract.image_to_string(img)

    # Identify document type
    document_type = identify_document_type(text)

    return text, document_type

def identify_document_type(document_text):
    common_medical_words = [
        'patient', 'diagnosis', 'treatment', 'medical history',
        'x-ray chest', 'radiologic', 'mri', 'ct scan',
        'laboratory results', 'blood test', 'prescription',
        'medical examination', 'patient history', 'electrocardiogram',
        'ultrasound', 'pathology report', 'clinical findings',
        'physical examination', 'vital signs', 'surgical procedure',
        'discharge summary', 'patient information', 'health record','diabetes','ABO Grouping'
    ]

    if any(word in document_text.lower() for word in common_medical_words):
        if 'x-ray' in document_text.lower():
            return "X-Ray Chest"
        elif 'mri' in document_text.lower():
            return "MRI scan"
        elif 'ct scan' in document_text.lower():
            return "CT scan"
        elif 'abo grouping' in document_text.lower():
            return "A Positive"
        elif 'blood test' in document_text.lower() or 'laboratory results' in document_text.lower():
            return "Blood Test Report"
        elif 'diabetes' in document_text.lower() or 'glucose levels' in document_text.lower():
            return "Diabetes Report"
        # Add more conditions for additional report types as needed
        else:
            return "Generic medical document"
    else:
        return "Not a medical document"

if __name__ == '__main__':
    app.run(debug=True)
