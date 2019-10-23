import csv
import os
import paralleldots
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
        for line in csv_reader:
            sex = line['sex']
            city = line['city']
            emotion = text_to_emotion(line['text'])
            month, time = timestamp_converter(int(line['timestamp']))
            yield sex, city, emotion, month, time


def converter(nested_list):
    ''' converts list of tuples into list of strings'''
    lines = []
    for tupl in nested_list:
        line = ''
        for id, item in enumerate(tupl):
            if id == 0:
                continue
            elif id < len(tupl)-1:
                line += str(item) + ','
            else:
                line += str(item)
        lines.append(line)
    # print(lines)
    return lines 


def save_as_csv(response):
    ''' build csv file from response data '''
    with open('statistics.csv', 'w') as new_file:
        lines = converter(response)
        print(lines)
        for line in lines:
            new_file.write(line)
            new_file.write('\n')
    pass

# os.path.join(current_app.config['DOWNLOAD_FOLDER'],
response = [
    (24, 'w', 'Kharkiv', 'Fear: 60%', '10', '15:2:51'), 
    (29, 'w', 'Kiev', 'Happy: 23%', '10', '18:53:4')
]

save_as_csv(response)

