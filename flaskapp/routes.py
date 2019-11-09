
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
    add_author_id , save_as_csv, save_to_html
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


@bp.route('/poll-filters', methods=['POST', 'GET'])
def process():
    form =  ChoiceForm(request.form)
    if request.method == 'POST':

        select = request.form.get('sel')  
        if select:
            print(select)
            db = get_db()
            res = db.execute(
            '''SELECT username, sex, city, emotion, month, poll_time
                FROM poll p
                JOIN author a
                    ON p.author_id = a.id
                ORDER BY %s''' % (select,)                  
            ).fetchall()
            # print(res) 
            db.close
                  
        rad = request.form["radio"] 
        if rad == 'csv':
            # print('csv function call') 
            save_as_csv(res)
            return redirect(url_for('routes.download_csv'))
        if rad == 'html':
            print('html function call') 
            save_to_html(res, select)
            return redirect(url_for('routes.download_html'))
    return render_template('process.html', form=form)


@bp.route('/download-csv',methods=['GET'])
def download_csv():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'downloads/statistics.csv')   
    return send_file(filename, as_attachment=True, attachment_filename='statistics.csv')

@bp.route('/download-html',methods=['GET'])
def download_html():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'downloads/test.html')   
    return send_file(filename, as_attachment=True, attachment_filename='statistics.html')