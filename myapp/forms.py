from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from myapp.models import User


class RegistrationForm(FlaskForm):
    username = StringField("ユーザー名", validators=[DataRequired(), Length(min=2, max=20)])
    # email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("パスワード", validators=[DataRequired()])
    confirm_password = PasswordField(
        "パスワードの確認", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("そのユーザー名はすでに使用されています 別の名前を入力してください")

    # def validate_email(self, email):
    #     email = User.query.filter_by(email=email.data).first()
    #     if email:
    #         raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    # email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("ユーザー名", validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField("パスワード", validators=[DataRequired()])
    # remember = BooleanField("Remember me")
    submit = SubmitField("Login")


class PageForm(FlaskForm):
    page_title = StringField("page_title", validators=[DataRequired()])
    page_url = StringField("page_url", validators=[DataRequired()])
    page_domain = StringField("page_domain", validators=[DataRequired()])
    submit = SubmitField("Page")
