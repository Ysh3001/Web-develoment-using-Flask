from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired, URL
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = StringField('Location', validators=[URL(message="Enter a valid URL!")])
    open = StringField('Open', validators=[DataRequired()])
    close = StringField('Close', validators=[DataRequired()])
    rating = SelectField('Coffee Rating', choices=['☕️', '☕️☕️', '☕️☕️☕️', '☕️☕️☕️☕️', '☕️☕️☕️☕️☕️'],
                         validators=[DataRequired()])
    wifi = SelectField('WIFI rating', choices=['✘', '💪', '💪💪', '💪💪💪', '💪💪💪💪', '💪💪💪💪💪'], validators=[DataRequired()])
    outlet = SelectField('Outlet rating', choices=['✘', '🔌', '🔌🔌', '🔌🔌🔌', '🔌🔌🔌🔌', '🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.route("/")
def home():
    return render_template("index.html")


cafe_list = []


@app.route('/add', methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    if request.method == "POST" and form.validate_on_submit():
        print("True")
        cafe_list.append(request.form["cafe"])
        cafe_list.append(request.form["location"])
        cafe_list.append(request.form["open"])
        cafe_list.append(request.form["close"])
        cafe_list.append(request.form["rating"])
        cafe_list.append(request.form["wifi"])
        cafe_list.append(request.form["outlet"])

        with open('cafe-data.csv', 'a', newline='',  encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(cafe_list)
            cafe_list.clear()
        form = CafeForm(formdata=None)

        return render_template('add.html', form=form, req=True)
    else:
        return render_template('add.html', form=form, req=False)

@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', newline='', encoding='utf-8') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
    return render_template('cafes.html', cafes=list_of_rows)


if __name__ == '__main__':
    app.run(debug=True)
