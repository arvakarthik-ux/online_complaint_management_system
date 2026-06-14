from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class AdminCreateForm(FlaskForm):
    full_name = StringField("Full Name", validators=[DataRequired(), Length(min=2, max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8, max=128)])
    role = SelectField("Role", choices=[("admin", "Admin"), ("superadmin", "Super Admin")], validators=[DataRequired()])
    category_id = SelectField("Category", coerce=int)
    submit = SubmitField("Create Admin")
