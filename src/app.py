from flask import Flask, render_template, request

from utils.geo_search_api import get_coordinates
from utils.weather_api import get_forecast


app = Flask(__name__)

@app.route('/')
def show_page():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def get_weather():
    city = request.args.get('city')
    cords = get_coordinates(city)
    forecast = get_forecast(cords)
    return render_template("forecast.html", forecast=forecast)


if __name__=="__main__":
    app.run(debug=True, port=5000)
