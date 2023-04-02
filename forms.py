from flask_wtf import FlaskForm
from wtforms import StringField,TextAreaField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo,Email,ValidationError
from models import User

class ContactForm(FlaskForm):
    def validate_email(form,field):
        if "@gmail.com" not in field.data:
            raise ValidationError("invalid email")
        
    name = StringField('name', validators = [DataRequired()])
    email = StringField('email', validators= [DataRequired(),Email(),validate_email])
    subject = StringField('subject', validators=[DataRequired()])
    message = TextAreaField('message')


class RegisterForm(FlaskForm):
    def validate_email(form,field):
        user = User.query.filter_by(email=field.data).first()
        if user:
            raise ValidationError("Email already taken.")
        if "@gmail.com" not in field.data:
            raise ValidationError("invalid email")
        
    def validate_confirm_password(form, field):
        if form.password.data != field.data:
            raise ValidationError("Passwords must match")
    name = StringField('name',validators=[DataRequired()])
    email = StringField('email', validators= [DataRequired(),Email(),validate_email])
    password = PasswordField('password', validators=[DataRequired()])
    confirm_password = PasswordField('confirm_password',validators=[DataRequired(), EqualTo('password'),validate_confirm_password])


class LoginForm(FlaskForm):
    def validate_email(form,field):
        if "@gmail.com" not in field.data:
            raise ValidationError("invalid email")
    email = StringField('email', validators= [DataRequired(),Email(),validate_email])
    password = PasswordField('password', validators=[DataRequired()])


class SubscribeForm(FlaskForm):
    def validate_email(form,field):
        if "@gmail.com" not in field.data:
            raise ValidationError("invalid email")
    name = StringField('name',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired(),Email(),validate_email])
   
    submit = SubmitField('Subscribe')


class ReviewForm(FlaskForm):
    message = TextAreaField('message',validators=[DataRequired()])


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])

    