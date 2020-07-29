from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


class VoteForm(FlaskForm):
    vote = RadioField('Your Vote?', choices=[('Cats', 'Cats'), ('Dogs', 'Dogs')],
                      validators=[DataRequired()])
    submit = SubmitField('Vote Now')


class UpdateImage(FlaskForm):
    picture = FileField('Update Profile Picture', validators=[FileRequired(),
                                                              FileAllowed(['jpg', 'png', 'jpeg'])])

    submit = SubmitField('Sent Picture')

