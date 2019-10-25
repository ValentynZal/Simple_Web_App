
import os
from flask import (
    Blueprint, g, redirect, render_template, request, url_for, flash, current_app, send_file
)
from werkzeug.utils import secure_filename
from flaskapp.db import get_db
from flaskapp.form import ChoiceForm
from flaskapp.utils import text_to_emotion, timestamp_converter, csv_extracter 


bp = Blueprint('routes', __name__)


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
        dict_list = csv_extracter(file.filename)
        db = get_db()
        for dic in dict_list:
            print(dic)
            db.execute(
                '''INSERT INTO author (username, sex)
                VALUES (?, ?)''',
                (dic['name'], dic['sex']) 
            )
            db.commit()
            db.execute(
                '''INSERT INTO poll (city, emotion, month, poll_time)
                VALUES (?, ?, ?, ?)''',
                (dic['city'], dic['emotion'], dic['month'], dic['poll_time']) 
            )
            db.commit()
        db.close()
        print("saved")
        # return redirect(url_for('routes.process'))
    return render_template('index.html')

