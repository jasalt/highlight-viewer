import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

from kindle import read_clippings

from flask.ext.autoindex import AutoIndex

CLIPPINGS = ""

DATA_FILE = 'highlights.txt'
UPLOAD_FOLDER = './output/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

AutoIndex(app, browse_root=UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

# TODO set some nice index page
# @app.route("/")
# def home():
#     f = open(UPLOAD_FOLDER + DATA_FILE, 'r')
#     text = f.read()
    
#     return str(CLIPPINGS)

@app.route("/upload", methods=['POST'])
def upload():
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], DATA_FILE))
        print("Uploaded")
    else:
        return 500
    
    print("Processing")
    CLIPPINGS = read_clippings(UPLOAD_FOLDER + DATA_FILE)

    return "Upload OK"

if __name__ == "__main__":
    app.run()
