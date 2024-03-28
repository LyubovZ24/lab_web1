import os.path

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, IntegerField, ColorField

from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired

from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from werkzeug.utils import secure_filename
from image_processing import perform_image_processing

SECRET_KEY = "secret"
RECAPTCHA_PUBLIC_KEY = '6Lci-6cpAAAAAF1dLO8oz3cIdMsXQAtIiuWv-1fd'
RECAPTCHA_PRIVATE_KEY = '6Lci-6cpAAAAAMyCf1g2nwp7_22ID8CbesFxF1s_'


class ImageForm(FlaskForm):
    frame_width = IntegerField('Ширина рамки', validators=[DataRequired()])
    upload = FileField(validators=[FileRequired('Выберите файл')])
    color = ColorField('Выберите цвет рамки', validators=[DataRequired()])
    recaptcha = RecaptchaField()


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = SECRET_KEY
app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY


@app.route("/")
def index(form=None, new_image="", table_of_colors=""):
    if form is None:
        form = ImageForm()
    return render_template("index.html", form=form, filepath=new_image, table=table_of_colors)


@app.route("/add", methods=["POST"])
def add():
    form = ImageForm()
    if form.validate_on_submit():
        f = form.upload.data
        filename = secure_filename(f.filename)
        f.save(os.path.join('static/photos', filename))

        new_filename, graphic_name = perform_image_processing(os.path.join('static/photos', filename), form.frame_width.data,
                                                              form.color.data)

        return index(form, new_filename, graphic_name)

    return index(form)


if __name__ == "__main__":
    app.run()
