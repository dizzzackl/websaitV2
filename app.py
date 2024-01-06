import os
import pickle
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'downloads'
FILE_PATH = 'mydatabase.txt'

class File:
    def __init__(self, name, webaddress):
        self.name = name
        self.webaddress = webaddress

@app.route('/')
def index():
    files = get_files_from_file()
    return render_template("index.html", files=files)

@app.route('/files', methods=['GET', 'POST'])
def get_files():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = file.filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            address = f"http://gera228.pythonanywhere.com/download/{filename}"
            file_obj = File(name=filename, webaddress=address)
            save_file_to_file(file_obj)
            return redirect(url_for("index"))

    return render_template("files.html")

def save_file_to_file(file_obj):
    files = get_files_from_file()
    files.append(file_obj)
    with open(FILE_PATH, 'wb') as f:
        pickle.dump(files, f)

def get_files_from_file():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, 'rb') as f:
            files = pickle.load(f)
        return files
    return []

if __name__ == '__main__':
    app.run(debug=True)
