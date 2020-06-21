from flask import Flask, render_template, url_for, redirect, flash, request, jsonify
from werkzeug.utils import secure_filename
import os
from fastai.vision import *
import pickle
import warnings
warnings.filterwarnings('ignore')

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
# 图片的存放路径
app.config['UPLOAD_FLODER'] = UPLOAD_FOLDER
# 限制图片的大小
app.config['MAX_CONTENT_LENGTH'] = 4 * 1024 * 1024
app.secret_key = 'xjw'

path = os.path.realpath('.')

@app.route('/')
def index():
    return render_template('index.html')

def predict(img):
    learner = load_learner(path)
    img = open_image(img).resize(size=128)
    pred_class, pre_idx, outputs = learner.predict(img)
    print(outputs)
    return learner.data.classes[int(pred_class)]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/dataFromAjax', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')

        file = request.files['file']
        # if user does not select file, browser also submit 
        # an empty part without filename
        if file.filename == '':
            flash('No selected file')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FLODER'], filename))
            result = predict(app.config['UPLOAD_FLODER'] + '/'+ filename)
            
            result = 'The bear is '+ result
            return jsonify({"success":200, "msg": "upload successed ", "result":result})
        else:
            return jsonify({"error": 1001, "msg":  "upload failed"})


if __name__ == "__main__":
    app.run(debug=True)
