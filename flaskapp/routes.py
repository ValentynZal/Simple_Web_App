import os
import csv
import paralleldots
from datetime import datetime
from flask import (
    Blueprint, g, redirect, render_template, request, url_for, flash, current_app
)
from werkzeug.utils import secure_filename
from flaskapp.db import get_db


bp = Blueprint('routes', __name__)


def text_to_emotion(text):
    paralleldots.set_api_key("OlMPavfQZZ02uGla2Goa1UzxDJm2RhkjEVJfhAb6MVY")
    paralleldots.get_api_key()
    lang_code = "en"    
    dictionary = paralleldots.emotion(text)  
    arr =  dictionary['emotion'].values()
    prior = max(arr)
    for k, v in dictionary['emotion'].items():
        if v == prior:
            return k

def timestamp_converter(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    month = dt.month
    time =str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)    
    return month, time

def csv_extracter(filename):
    with open(os.path.join(current_app.config['UPLOAD_FOLDER'], filename), 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # next(csv_file)
        for line in csv_reader:
            sex = line[' sex']
            city = line[' city']
            emotion = text_to_emotion(line[' text'])
            month, time = timestamp_converter(int(line[' timestamp']))
        return sex, city, emotion, month, time
 

@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], file.filename))        
        sex, city, emotion, month, poll_time = csv_extracter(file.filename)
        db = get_db()
        db.execute(
                'INSERT INTO poll (sex, city, emotion, month, poll_time)\
                 VALUES (?, ?, ?, ?, ?)',
                (sex, city, emotion, month, poll_time)
        )
        db.commit()
        print("saved")
        # return redirect(url_for('page'))
    return render_template('page.html')




