import csv
from flask import request
from spellchecker import SpellChecker


def distance_to_metro(metro):
    # Функция определение расстояние от центра до станции метро пользователя
    metro = str(request.form['metro'])
    spell = SpellChecker()
    spell.word_frequency.load_text_file("metro_station.txt")
    metro_correct = spell.correction(metro)
    metro_correct_up = metro_correct.capitalize()
    print(metro_correct_up)
    with open('Dist_to_center.csv',encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if metro_correct_up in row:
                return row[2]


def age_of_house(year_of_constr):
    # Вычисление возраста дома
    age_constr = request.form['year_of_constr']
    age = (2020 - int(age_constr))
    return age


def change_of_repair(type_of_repair):
    # Функция работы выпадающего списка выбора типа ремонта
    global cos
    type_of_rep = request.form['type_of_repair']
    if type_of_rep == "cosmetic": # Если выбран тип ремонта Косметический
        cos = 1
        euro = 0
        design = 0
    elif type_of_rep == "eurorepair": # Если выбран тип ремонта Евроремонт
        cos = 0
        euro = 1
        design = 0
    elif type_of_rep == "designer": # Если выбран тип ремонта Дизайнерский
        cos = 0
        euro = 0
        design = 1
    return cos, euro, design


def change_of_typehome(type_of_house):
    # Функция работы вырадающего списка выбора типа дома
    global brick_ch
    type_of_hous = request.form['type_of_house']
    if type_of_hous == "brick": # Если выбран тип дома Кирпичный
        brick_ch = 1
        panel_ch = 0
        modular_ch = 0
        monolithic_ch = 0
    elif type_of_hous == "panel": # Если выбран тип дома Панельный
        brick_ch = 0
        panel_ch = 1
        modular_ch = 0
        monolithic_ch = 0
    elif type_of_hous == "modular": # Если выбран тип дома Блочный
        brick_ch = 0
        panel_ch = 0
        modular_ch = 1
        monolithic_ch = 0
    elif type_of_hous == "monolithic": # Если выбран тип дома Монолитный
        brick_ch = 0
        panel_ch = 0
        modular_ch = 0
        monolithic_ch = 1
    return brick_ch, panel_ch, modular_ch, monolithic_ch


def place_value(number):
    return ("{:,}".format(number))

