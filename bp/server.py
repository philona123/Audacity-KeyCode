import os
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploads')
MODEL_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'downloads')
app = Flask(__name__, static_folder="uploads")
app.config['SECRET_KEY'] = '@@SECRET@@!!'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MODEL_FOLDER'] = MODEL_FOLDER
@app.route('/', methods=['GET', 'POST'])
def get_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            abort(400, 'No File')
        else:
            file = request.files['file']
            print(secure_filename(file.filename))
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            flash('Image successfully uploaded')
            return 'Success', 201
    elif request.method == 'GET':
        return return_pdf()
@app.route("/file")
def return_pdf():
    return send_file(os.path.join(app.config['MODEL_FOLDER'], 'scene.obj'))
if __name__ == '__main__':
    app.run(host="0.0.0.0")