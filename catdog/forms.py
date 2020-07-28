from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    vote = RadioField('Your Vote?', choices=[('Cats', 'Cats'), ('Dogs', 'Dogs')],
                      validators=[DataRequired()])
    submit = SubmitField('Vote Now')

