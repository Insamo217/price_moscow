from geopy import distance
import pickle
import pandas as pd
import joblib
import csv
from flask import (
    Flask, 
    render_template, 
    redirect,
    request, 
    jsonify
)
from webapp.forms import ParametersFlat
from webapp.tools import (
    age_of_house,
    distance_to_metro,
    change_of_repair,
    change_of_typehome,
    place_value
)

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    
    @app.route('/', methods=["GET", "POST"])
    def predict():
        title = "Оценка недвижимости"
        title_predict = "Стоимость квартиры"
        form = ParametersFlat()
        if form.validate_on_submit():
            # Собираем данные из формы в переменные
            try:
                time_metro = request.form['time_to_metro']
                flat_area = request.form['flat_area']
                floor = request.form['floor']
                num_of_floors = request.form['num_of_floors']
                dist_to_metro = distance_to_metro(form.metro)
                cos = (change_of_repair(form.type_of_repair)[0])
                euro = (change_of_repair(form.type_of_repair)[1])
                design = (change_of_repair(form.type_of_repair)[2])
                brick_ch = (change_of_typehome(form.type_of_house)[0])
                panel_ch = (change_of_typehome(form.type_of_house)[1])
                modular_ch = (change_of_typehome(form.type_of_house)[2])
                monolithic_ch = (change_of_typehome(form.type_of_house)[3])
                age = age_of_house(form.year_of_constr)
                # Собираем словарь из данных формы
                data = {'Время до метро, мин.': time_metro,
                        'Площадь квартиры': flat_area,
                        'Этаж': floor,
                        'Количество этажей': num_of_floors,
                        'Расстояние до центра': dist_to_metro,
                        'Блочный': modular_ch,
                        'Кирпичный': brick_ch,
                        'Монолитный': monolithic_ch,
                        'Панельный': panel_ch,
                        'Возраст дома': age,
                        'Дизайнерский': design,
                        'Евроремонт': euro,
                        'Косметический': cos}
                df = pd.DataFrame(data, index=[1]) # Переводим словарь c данными пользователя в DataFrame
                model = joblib.load('model_cian.pkl') # Загружаем модель GradientBoostingRegressor
                price = model.predict(df) # Передаем в модель данные пользователя
                price_int = int(price)
                price_finish=place_value(price_int)
                return render_template('result.html', price=price_finish, title=title_predict)
            except(ValueError):
                return('Станция метро не была найдена, повторите ввод')
        return render_template('parameters_flat.html', page_title=title,form=form)

    return app

