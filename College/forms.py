from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, BooleanField, IntegerField, DateField
from wtforms.validators import DataRequired, Length, Email, InputRequired, Regexp, EqualTo, ValidationError
from College.models import User

class FeedbackForm(FlaskForm):
    name = StringField('Your Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Your Email',
                        validators=[DataRequired(), Email()])
    phone = StringField(
        'Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    feedback = TextAreaField(
        'Feedback',
        validators=[DataRequired(),
                    Length(max=500, message="Message must be 500 characters or fewer")]
    )
    submit = SubmitField('Submit')



class SearchForm(FlaskForm):
    admission_number= StringField('Admission Number', validators=[DataRequired()])
    submit = SubmitField('Search')





class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is taken try different one")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is taken try different one")



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')





class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is taken try different one")
        
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email is taken try different one")
            


class AdmissionForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=50)])
    f_name = StringField("Father's Name", validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Your Email',
                        validators=[DataRequired(), Email()])
    phone = StringField(
        'Phone Number', validators=[DataRequired(), Length(min=10, max=15)])
    dob = DateField('DOB', validators=[DataRequired()])
    photo = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    signature = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Submit')