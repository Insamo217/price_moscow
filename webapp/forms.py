from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired, NumberRange


class ParametersFlat(FlaskForm):
    metro = StringField('Станция метро', validators=None, render_kw={"class": "form-control"})
    time_to_metro = IntegerField('Время до метро, мин', validators=[InputRequired(), NumberRange(min=1, max=60, message='Введите корректные данные')], render_kw={"class": "form-control"})
    flat_area = IntegerField('Площадь квартиры, м2', validators=[InputRequired(), NumberRange(min=10, max=500, message='Введите корректные данные')], render_kw={"class": "form-control"})
    floor = IntegerField('Этаж', validators=[InputRequired(), NumberRange(min=1, max=150, message='Введите корректные данные')], render_kw={"class": "form-control"})
    num_of_floors = IntegerField('Количество этажей', validators=[InputRequired(), NumberRange(min=1, max=150, message='Введите корректные данные')], render_kw={"class": "form-control"})
    type_of_repair = SelectField('Тип ремонта',choices = [('cosmetic', 'Косметический'), ('eurorepair', 'Евроремонт'), ('designer', 'Дизайнерский')], validators=[DataRequired()], render_kw={"class": "form-control"})
    year_of_constr = IntegerField('Год постройки', validators=[InputRequired(), NumberRange(min=1840, max=2020, message='Введите корректные данные')], render_kw={"class": "form-control"})
    type_of_house = SelectField('Тип дома', choices = [('brick', 'Кирпичный'), ('panel', 'Панельный'), ('modular', 'Блочный'), ('monolithic', 'Монолитный')], validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Узнать стоимость', validators=None)
