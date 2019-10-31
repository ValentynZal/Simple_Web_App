from wtforms import Form, SelectField, SelectMultipleField, RadioField, SubmitField, validators


sel_choice = [ 
    ('username', 'interviewed person`s name'), 
    ('sex', 'interviewed person`s sex'),
    ('city', 'interviewed person`s city'),
    ('emotion', 'interviewed person`s comment charateristic'),    
    ('month', 'poll month'),
    ('poll_time', 'poll time'),
]

class ChoiceForm(Form):
    sel = SelectField(u'Criteria', choices=sel_choice)
    radio = RadioField(choices=[('csv', 'csv'), ('html', 'html')])
    submit = SubmitField(label='apply')
