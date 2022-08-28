import os
import cairo
import subprocess
from subprocess import Popen, PIPE
from subprocess import check_output
from flask import Flask, flash, request, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from fill import process_image
import cv2

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
            img = cv2.imread('uploads/screenShot.jpg')
            process_image('uploads/screenShot.jpg')
            flash('Image successfully uploaded')
            length = img.shape[0]
            width = imag.shape[1]
            # creating a SVG surface
            # here geek95 is file name & 700, 700 is dimension
            with cairo.SVGSurface("plane.svg", length, width) as surface:
                # creating a cairo context object for SVG surface
                # using Context method
                context = cairo.Context(surface)
                # setting color of the context
                context.set_source_rgb(0, 0, 0)
                # creating a rectangle
                context.rectangle(0, 0, length, width)
                # Fill the color inside the rectangle
                context.fill()
                # printing message when file is saved
                print("File Saved")
            return 'Success', 201
    elif request.method == 'GET':
        return return_pdf()

@app.route("/file")
def return_pdf():
    return send_file(os.path.join(app.config['MODEL_FOLDER'], 'teapot.obj'))

@app.route('/svg',methods=['GET',])
def getSVG():
    session = Popen([os.path.join(app.config['MODEL_FOLDER'], 'tosvg.sh')], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()
    if stderr:
        raise Exception("Error "+str(stderr))
    return ('downloads/plan.svg')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
