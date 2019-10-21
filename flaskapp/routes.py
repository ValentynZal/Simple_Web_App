import os
import csv
import paralleldots
from math import floor
from datetime import datetime
from flask import (
    Blueprint, g, redirect, render_template, request, url_for, flash, current_app
)
from werkzeug.utils import secure_filename
from flaskapp.db import get_db
from flaskapp.form import ChoiceForm


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
            return f'{k}: {floor(v*100)}%'

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
            sex = line['sex']
            city = line['city']
            emotion = text_to_emotion(line['text'])
            month, time = timestamp_converter(int(line['timestamp']))
            yield sex, city, emotion, month, time
 

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
        gen = csv_extracter(file.filename)
        db = get_db()
        for row in gen:
            print(row)
            db.execute(
                '''INSERT INTO poll (sex, city, emotion, month, poll_time)
                VALUES (?, ?, ?, ?, ?)''',
                (row) # row[0], row[1], row[2], row[3], row[4]
            )
            db.commit()
        db.close()
        print("saved")
        return redirect(url_for('routes.process'))
    return render_template('index.html')

@bp.route('/poll-process', methods=['POST', 'GET'])
def process():
    form =  ChoiceForm(request.form)
    if request.method == 'POST':
        sel1 = request.form.get('sel')
        db = get_db()
        res = db.execute(
            'SELECT * FROM poll WHERE sex = ?',
            (sel1, )
        ).fetchall()
        print(res)                                    
        # rad = request.form["radio"]   
        # if rad == 'csv':
        #     print(6) 
        # if rad == 'html':
        #     print(7)                             
    return render_template('process.html', form=form)




