from wtforms import Form, SelectField, SelectMultipleField, RadioField, SubmitField, validators


sel_choice1 = [ 
    ('m', 'man'), 
    ('w', 'woman'),
]

sel_choice2 = [ 
    ('Kiev', 'Kiev'), 
    ('Kharkiv', 'Kharkiv'),
]

sel_choice3 = [ 
    ('Happy', 'Happy'), 
    ('Angry', 'Angry'),
    ('Excited', 'Excited'), 
    ('Sad', 'Sad'),
    ('Fear', 'Fear'), 
    ('Bored', 'Bored'),
]

sel_choice4 = [ 
    (1, 'Jan'), 
    (2, 'Feb'), 
    (3, 'March'), 
    (4, 'Apr'),     
    (5, 'May'),     
    (6, 'June'), 
    (7, 'July'),     
    (8, 'Aug'), 
    (9, 'Sep'), 
    (10, 'Oct'), 
    (11, 'Nov'), 
    (12, 'Dec'), 
]

class ChoiceForm(Form):
    sel_sex = SelectField(u'Criteria', choices=sel_choice1)
    sel_city = SelectField(u'Criteria', choices=sel_choice2)
    sel_emotion = SelectField(u'Criteria', choices=sel_choice3)
    sel_month = SelectField(u'Criteria', choices=sel_choice4)
    radio = RadioField(choices=[('csv', 'csv'), ('html', 'html')])
    submit = SubmitField(label='apply')
