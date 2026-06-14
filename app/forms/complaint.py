from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileField, FileRequired, FileSize

class ComplaintForm(FlaskForm):
    category = SelectField("Category", coerce=int, validators=[DataRequired()])
    title = StringField("Complaint Title", validators=[DataRequired(), Length(min=5, max=200)])
    description = TextAreaField("Complaint Description", validators=[DataRequired(), Length(min=20)])
    incident_date = DateField("Incident Date", validators=[DataRequired()], format="%Y-%m-%d")
    incident_location = StringField("Incident Location", validators=[DataRequired(), Length(min=3, max=200)])
    priority = SelectField("Priority Level", choices=[("Low", "Low"), ("Medium", "Medium"), ("High", "High")], validators=[DataRequired()])
    attachments = FileField("Upload Evidence/Documents", validators=[
        FileAllowed(["png", "jpg", "jpeg", "gif", "pdf", "doc", "docx"], "Allowed: images, pdf, doc, docx"),
        FileSize(max_size=10 * 1024 * 1024, message="Max file size: 10MB")
    ])
    additional_notes = TextAreaField("Additional Notes")
    submit = SubmitField("Submit Complaint")
