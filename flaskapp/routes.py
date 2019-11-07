
import os
from flask import (
    Blueprint, g, redirect, render_template, request, url_for, 
    flash, current_app, send_file
)
from werkzeug.utils import secure_filename
from flaskapp.db import get_db
from flaskapp.form import ChoiceForm
from flaskapp.utils import (
    text_to_emotion, timestamp_converter, csv_extracter, 
    add_author_id 
)

bp = Blueprint('routes', __name__)
n = 0

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
            # print(dic)
            db.execute(
                '''INSERT INTO author (username, sex)
                VALUES (?, ?)''',
                (dic['name'], dic['sex']) 
            )
        poll_id = db.execute(
                '''SELECT id FROM author''',
        ).fetchall()
        # print(poll_id)
        global n
        add_author_id(dict_list, poll_id, n)
        n += len(dict_list)
        for dic in dict_list:
            db.execute(
                '''INSERT INTO poll (city, emotion, month, poll_time, author_id)
                VALUES (?, ?, ?, ?, ?)''',
                (dic['city'], dic['emotion'], dic['month'], dic['poll_time'], dic['author_id']) 
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
        select = request.form.get('sel')  
        if select:
            print(select)
            db = get_db()
            res = db.execute(
            '''SELECT username, sex, city, emotion, month, poll_time
                FROM poll
                JOIN author
                    ON poll.author_id = author.id
                ORDER BY %s''' % (select,)                  
            ).fetchall()
            print(res) 
            db.close
    return render_template('process.html', form=form)