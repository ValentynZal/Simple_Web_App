from wtforms import Form, SelectField, SelectMultipleField, RadioField, SubmitField, validators


sel_choice1 = [ 
    ('m', 'man'), 
    ('w', 'woman'),
]

class ChoiceForm(Form):
    sel_sex = SelectField(u'Criteria', choices=sel_choice1)
    radio = RadioField(choices=[('csv', 'csv'), ('html', 'html')])
    submit = SubmitField(label='apply')
