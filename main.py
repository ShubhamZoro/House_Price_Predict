from flask import Flask,  jsonify,render_template,redirect,url_for
import util
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,SelectField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"
Bootstrap(app)
class Predict(FlaskForm):
    Area = StringField('Area(Square Feet)', validators=[DataRequired()])
    Bhk= SelectField("BHK", choices=["1", "2", "3", "4", "5"],
                                validators=[DataRequired()])
    Bath= SelectField("Bath", choices=["1", "2", "3", "4", "5"],
                              validators=[DataRequired()])
    Location= StringField("Location",
                               validators=[DataRequired()])
    submit = SubmitField('Estimate Price')

@app.route("/",methods=['GET','POST'])
def home():
    form=Predict()
    res=0
    tru=False
    if form.validate_on_submit():
        total_sqft = float(form.Area.data)
        location = form.Location.data
        bhk = int(form.Bhk.data)
        bath = int(form.Bath.data)

        response = jsonify({
        'estimated_price': util.get_estimated_price(location,total_sqft,bhk,bath)
        })
        response.headers.add('Access-Control-Allow-Origin', '*')
        res=util.get_estimated_price(location,total_sqft,bhk,bath)
        print(res)
        tru=True
        return render_template("app.html",form=form,res=res,tru=tru,price=res)
    return  render_template("app.html",form=form,tru=tru,price=res)

@app.route('/get_location_names', methods=['GET'])
def get_location_names():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response


    

if __name__ == "__main__":
    print("Starting Python Flask Server For Home Price Prediction...")
    util.load_saved_artifacts()
    app.run(debug=True)
