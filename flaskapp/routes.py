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
    return paralleldots.emotion(text)

def timestamp_converter(timestamp):
    dt = datetime.utcfromtimestamp(timestamp)
    month = dt.month
    time =str(dt.hour) + ':' + str(dt.minute) + ':' + str(dt.second)    
    return month, time

def csv_extracter(file):
    with open(file, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        next(csv_file)
        for line in csv_reader:
            sex = line['name']
            city = line['city']
            emotion = text_to_emotion(line['text'])
            month, time = timestamp_converter(line['timestamp'])
        return sex, city, emotion, month, time


@bp.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        sex, city, emotion, month, time = csv_extracter(file)
        # query
        db = get_db()
        db.execute(
                'INSERT INTO user (sex, city, emotion, month, time)\
                 VALUES (?, ?, ?, ?, ?)',
                (sex, city, emotion, month, time)
        )
        db.commit()
        print("saved")
        # return redirect(url_for('page'))
    return render_template('page.html')




