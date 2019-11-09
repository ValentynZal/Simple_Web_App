import csv
import os
import paralleldots
from collections import defaultdict
from datetime import datetime
from math import floor
from flask import current_app


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
        res = []
        for line in csv_reader:
            name = line['name']
            sex = line['sex']
            city = line['city']
            emotion = text_to_emotion(line['text'])
            month, poll_time = timestamp_converter(int(line['timestamp']))
            l = [('name',name),('sex',sex),('city',city),('emotion',emotion),('month',month),('poll_time',poll_time)]
            res.append(dict(l))
        return res

def add_author_id(dict_list, poll_id, n):
    poll_id = poll_id[n:]
    get_list = [i[0] for i in poll_id]
    for i, dic in zip(get_list, dict_list):
        dic.update({'author_id': i}) 
    return dict_list


def save_as_csv(lines):
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'downloads/statistics.csv') 
    with open(filename, 'w') as new_csv:
        fieldnames = ['username', 'sex', 'city', 'emotion', 'month', 'poll_time']
        csv_writer = csv.DictWriter(new_csv, fieldnames=fieldnames)
        csv_writer.writeheader()
        for line in lines:
            # print(line[0],line[1],line[2],line[3],line[4])
            csv_writer.writerow({'username': line[0], 'sex': line[1], 'city': line[2], 'emotion': line[3], 'month': line[4], 'poll_time': line[5]})