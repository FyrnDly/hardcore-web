import os
from datetime import datetime
from flask import Flask, render_template, request, session, redirect, url_for
from module.imageProcessing import ImageProcessing
from module.db import ConnectionSQLite
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

db = ConnectionSQLite(os.getenv("DATABASE", 'database.sqlite'))

def allowed_file(filename):
    return filename.rsplit('.', 1)[-1].lower() in IMAGE_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/auth', methods=['GET', 'POST'])
@app.route('/auth/<check>', methods=['GET','POST'])
def auth(check=None):
    if request.method == "GET":
        if session.get('user'):
            return redirect('/')
        return render_template('auth.html')
    else:
        if check == 'login':
            # Get Request
            username = request.form['username']
            password = request.form['password']
            
            # Get User data
            user = db.selectTable('users', '*', f'username = "{username}"')
            if user:
                user_username = user[0][0]
                user_name = user[0][1]
                user_password = user[0][2]
                if user_password == password:
                    # Create Session
                    session['user'] = {
                        'username' : user_username,
                        'name' : user_name
                    }

                    return redirect('/') 
                else:
                    return render_template('auth.html', error="Kata Sandi Tidak Cocok")
                    
            else:
                return render_template('auth.html', error="Username Belum Terdaftar")
            
        elif check == 'register':
            # Get Request
            name = request.form['name']
            username = request.form['username']
            password = request.form['password']
            
            # Check Username
            username_status = len(db.selectTable('users', '*', f'username = "{username}"'))
            if username_status:
                return render_template('auth.html', error="Username Telah Terdaftar")
            
            # Create User DB
            db.insertTable("users", username, name, password)
            # Create Session
            session['user'] = {
                'username' : username,
                'name' : name
            }

            return redirect('/')
        
        elif check == 'logout':
            session.clear()
            return redirect('/auth')  
                  
        else:
            return redirect('/')

@app.route('/forest',methods=['GET','POST'])
@app.route('/forest/<forest_id>', methods=['GET','POST'])
def forest(forest_id=None):
    if not session.get('user'):
        return render_template('auth.html', error="Masuk Terlebih dahulu agar dapat Mengolah Citra")
    if request.method == "POST":
        # Rule Upload File
        if 'file' not in request.files:
            error = "File Belum Diupload"
            return render_template('forest.html', error=error)
        # Get file Image
        file_input = request.files['file']
        if not(allowed_file(file_input.filename)):
            error = "Pastikan File Merupakan Gambar berformat .png, .jpg, atau .jpeg"
            return render_template('forest.html', error=error)
        
        # Get Name Forest
        name_forest = request.form['name']
        
        # Save Image
        file_extension = file_input.filename.rsplit('.', 1)[-1].lower()
        date = datetime.now().strftime(f"%d-%m-%Y")
        file_name = secure_filename(f"{name_forest}-{date}.{file_extension}")
        file_input.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))
        file_path = f"image_forest/{file_name}"
        
        # Image Processing
        img_proc = ImageProcessing(f"public/{file_path}")
        ndvi = img_proc.get_ndvi()
        reflectance = img_proc.get_reflectance()
        output, status = img_proc.get_fuzzy()
        
        # Insert to DB
        db.insertTable("forests", name=name_forest, ndvi=round(ndvi, 2), reflectance=round(reflectance, 2), status=status, path_forest=file_path, quality=round(output, 2))
        forests = db.selectTable("forests")
        return render_template('forest.html', status=status, output=round(output, 2), forests=forests)
    else:
        if forest_id != None:
            file_path = db.selectTable("forests", 'path_forest', f'id = {forest_id}')[0][0]
            try:
                os.remove(f"public/{file_path}")
            except FileNotFoundError:
                print(f"File {file_path} tidak ditemukan.")
            except Exception as e:
                print(f"Terjadi kesalahan saat menghapus file: {e}")
            db.dropRecord("forests", forest_id)
        forests = db.selectTable("forests")
        return render_template('forest.html', forests=forests)

if __name__ == "__main__":
    app.run(debug=True)