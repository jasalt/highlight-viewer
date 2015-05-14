import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename

DATA_FILE = 'highlight.txt'
UPLOAD_FOLDER = './data/'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
    
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/")
def home():
    f = open(UPLOAD_FOLDER + DATA_FILE, 'r')
    text = f.read()
    
    return text

@app.route("/upload", methods=['POST'])
def upload():
    import ipdb; ipdb.set_trace()
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], DATA_FILE))
        return "Upload complete"
    else:
        return 500

if __name__ == "__main__":
    app.run(debug=True)
