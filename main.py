from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    name = StringField(label='Cafe name', validators=[DataRequired()])
    location = StringField(label='Location on Google Maps (URL)', validators=[DataRequired(), URL()])
    opening = StringField(label='Opening time', validators=[DataRequired()])
    closing = StringField(label='Closing time', validators=[DataRequired()])
    coffee = SelectField(u'Coffee Rating', choices=[('✘', '✘'), ('☕️', '☕️'), ('☕️☕️', '☕️☕️'), ('☕️☕☕️️', '☕️☕️☕️'), ('☕️☕️☕️☕️', '☕️☕☕️️☕️'), ('☕️☕️☕️☕️☕️', '☕️☕️☕️☕️☕️')])
    wifi = SelectField(u'WiFi Rating', choices=[('✘', '✘'), ('💪', '💪'), ('💪💪', '💪💪'), ('💪💪💪', '💪💪💪'), ('💪💪💪💪', '💪💪💪💪️'), ('💪💪💪💪💪', '💪💪💪💪💪️')])
    power = SelectField(u'Power socket availability', choices=[('✘', '✘'), ('🔌', '🔌'), ('🔌🔌', '🔌🔌'), ('🔌🔌🔌', '🔌🔌🔌️'), ('🔌🔌🔌🔌', '🔌🔌🔌🔌'), ('🔌🔌🔌🔌🔌', '🔌🔌🔌🔌🔌')])
    submit = SubmitField(label="Submit")


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open("cafe-data.csv", mode="a") as file:
            file.write(f"\n{form.name.data},{form.location.data},{form.opening.data.upper()},{form.closing.data.upper()},{form.coffee.data},{form.wifi.data},{form.power.data}")

    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
            print(row)
        print(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, length=len(list_of_rows))


if __name__ == '__main__':
    app.run(debug=True)
