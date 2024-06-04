import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from module.imageProcessing import ImageProcessing
from module.fuzzy import input_fuzzy
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("APP_SECRET", None)
app.static_url_path = '/public'
app.static_folder = 'public'

UPLOAD_PATH = os.getenv("APP_UPLOAD", 'public')
app.config['UPLOAD_FOLDER'] = UPLOAD_PATH
IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']

def allowed_file(filename):
    return filename.rsplit('.', 1)[-1].lower() in IMAGE_EXTENSIONS

@app.route('/',methods=['GET','POST'])
def index():
    if request.method == "POST":
        # Rule Upload File
        if 'file' not in request.files:
            error = "File Belum Diupload"
            return render_template('index.html', error=error)
        file_input = request.files['file']
        if not(allowed_file(file_input.filename)):
            error = "Pastikan File Merupakan Gambar berformat .png, .jpg, atau .jpeg"
            return render_template('index.html', error=error)
        
        # Save Image
        file_extension = file_input.filename.rsplit('.', 1)[-1].lower()
        file_time = datetime.now().strftime(f"%d-%m-%Y-%H_%M_%S")
        file_name = secure_filename(f"{file_time}.{file_extension}")
        file_input.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        
        # Image Processing
        path = f"{UPLOAD_PATH}/{file_name}"
        img_proc = ImageProcessing(path)
        output, status = img_proc.get_fuzzy()
        
        return render_template('index.html', status=status, output=round(output, 2))
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)