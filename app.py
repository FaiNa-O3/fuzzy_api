from flask import Flask, request, jsonify


import skfuzzy as fuzz
from skfuzzy import control as ctrl


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl
import skfuzzy as fuzz


app = Flask(__name__)


@app.route('/processjson', methods=['POST'])
def processjson():

    #===============================================================================================================================================#

    # INPUT
    # soil_tension from 0 to 100
    soil_tension = ctrl.Antecedent(np.arange(0, 100, 1), 'soil_tension')

    # sun_radiation from 0 to 12
    sunshine_hour = ctrl.Antecedent(np.arange(0, 12, 1), 'sunshine_hour')

    # delta_evaporation from 0 to 6 mm
    delta_evaporation = ctrl.Antecedent(
        np.arange(0, 6, 1), 'delta_evaporation')

    # last_watering from 0 to 14 days
    last_watering = ctrl.Antecedent(np.arange(0, 14, 1), 'last_watering')

    # OUTPUT
    # Water amount a plant needs
    watering_time = ctrl.Consequent(np.arange(0, 120, 1), 'watering_time')

    #===============================================================================================================================================#

    # soil_tension
    soil_tension['dry'] = fuzz.trapmf(soil_tension.universe, [0, 0, 25, 50])
    soil_tension['moist'] = fuzz.trimf(soil_tension.universe, [25, 50, 75])
    soil_tension['wet'] = fuzz.trapmf(
        soil_tension.universe, [50, 75, 100, 100])

    # sunshine_hour
    sunshine_hour['short'] = fuzz.trapmf(sunshine_hour.universe, [0, 0, 2, 6])
    sunshine_hour['medium'] = fuzz.trimf(sunshine_hour.universe, [2, 6, 10])
    sunshine_hour['long'] = fuzz.trapmf(
        sunshine_hour.universe, [6, 10, 12, 12])

    delta_evaporation['small'] = fuzz.trapmf(
        delta_evaporation.universe, [0, 0, 1, 3])
    delta_evaporation['medium'] = fuzz.trimf(
        delta_evaporation.universe, [1, 3, 5])
    delta_evaporation['large'] = fuzz.trapmf(
        delta_evaporation.universe, [3, 5, 6, 6])

    last_watering['short'] = fuzz.trapmf(last_watering.universe, [0, 0, 4, 7])
    last_watering['medium'] = fuzz.trimf(last_watering.universe, [4, 7, 10])
    last_watering['long'] = fuzz.trapmf(
        last_watering.universe, [7, 10, 14, 14])

    # watering_time.automf(5)
    # output ==== membership value
    watering_time['poor'] = fuzz.trapmf(watering_time.universe, [0, 0, 5, 10])
    watering_time['mediocre'] = fuzz.trimf(
        watering_time.universe, [10, 20, 30])
    watering_time['average'] = fuzz.trimf(watering_time.universe, [20, 40, 60])
    watering_time['decent'] = fuzz.trimf(watering_time.universe, [50, 60, 70])
    watering_time['good'] = fuzz.trapmf(
        watering_time.universe, [70, 80, 90, 90])

    #===============================================================================================================================================#

    # We define set of rules

    rule1 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])
    rule2 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])
    rule3 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])

    rule4 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['mediocre'])
    rule5 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])
    rule6 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])

    rule7 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['mediocre'])
    rule8 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])
    rule9 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                      & delta_evaporation['small'] & last_watering['short'], watering_time['poor'])

    rule10 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['mediocre'])
    rule11 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['poor'])
    rule12 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['poor'])

    rule13 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['mediocre'])
    rule14 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['mediocre'])
    rule15 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['poor'])

    rule16 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['mediocre'])
    rule17 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['mediocre'])
    rule18 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['short'], watering_time['poor'])

    rule19 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])
    rule20 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])
    rule21 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])

    rule22 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['average'])
    rule23 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])
    rule24 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])

    rule25 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['average'])
    rule26 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])
    rule27 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['short'], watering_time['mediocre'])

    rule28 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])
    rule29 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])
    rule30 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])

    rule31 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['average'])
    rule32 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])
    rule33 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])

    rule34 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['average'])
    rule35 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['average'])
    rule36 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['medium'], watering_time['mediocre'])

    rule37 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['average'])
    rule38 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['mediocre'])
    rule39 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['mediocre'])

    rule40 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['decent'])
    rule41 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['average'])
    rule42 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['mediocre'])

    rule43 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['decent'])
    rule44 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['average'])
    rule45 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['medium'], watering_time['mediocre'])

    rule46 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['average'])
    rule47 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['average'])
    rule48 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['mediocre'])

    rule49 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['decent'])
    rule50 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['decent'])
    rule51 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['average'])

    rule52 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['decent'])
    rule53 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['decent'])
    rule54 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['medium'], watering_time['average'])

    rule55 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['decent'])
    rule56 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['average'])
    rule57 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['mediocre'])

    rule58 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['decent'])
    rule59 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['decent'])
    rule60 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['average'])

    rule61 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['good'])
    rule62 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['decent'])
    rule63 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['small'] & last_watering['long'], watering_time['average'])

    rule64 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['good'])
    rule65 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['decent'])
    rule66 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['average'])

    rule67 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['good'])
    rule68 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['decent'])
    rule69 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['average'])

    rule70 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['good'])
    rule71 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['decent'])
    rule72 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['medium'] & last_watering['long'], watering_time['average'])

    rule73 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['good'])
    rule74 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['decent'])
    rule75 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['short']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['decent'])

    rule76 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['good'])
    rule77 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['decent'])
    rule78 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['medium']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['average'])

    rule79 = ctrl.Rule(soil_tension['dry'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['good'])
    rule80 = ctrl.Rule(soil_tension['moist'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['good'])
    rule81 = ctrl.Rule(soil_tension['wet'] & sunshine_hour['long']
                       & delta_evaporation['large'] & last_watering['long'], watering_time['average'])

    #===============================================================================================================================================#

    # Set rules needed to operate the fuzzy logic
    water_ctrl1 = ctrl.ControlSystem(
        [rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9,
         rule10, rule11, rule12, rule13, rule14, rule15, rule16, rule17, rule18,
         rule19, rule20, rule21, rule22, rule23, rule24, rule25, rule26, rule27,
         rule28, rule29, rule30, rule31, rule32, rule33, rule34, rule35, rule36,
         rule37, rule38, rule39, rule40, rule41, rule42, rule43, rule44, rule45,
         rule46, rule47, rule48, rule49, rule50, rule51, rule52, rule53, rule54,
         rule55, rule56, rule57, rule58, rule59, rule60, rule61, rule62, rule63,
         rule64, rule65, rule66, rule67, rule68, rule69, rule70, rule71, rule72,
         rule73, rule74, rule75, rule76, rule77, rule78, rule79, rule80, rule81
         ])

    # Add the simulation to control system
    water = ctrl.ControlSystemSimulation(water_ctrl1)

    #===============================================================================================================================================#

    #req_data = request.get_json()
    soil_tension_in = request.json['soil_tension']
    sunshine_hour_in = request.json['sunshine']
    delta_evaporation_in = request.json['evaporation']
    last_watering_in = request.json['last_water']

    soil_tension = int(soil_tension_in)
    sunshine_hour = int(sunshine_hour_in)
    delta_evaporation = int(delta_evaporation_in)
    last_watering = int(last_watering_in)

    # return '{}'.format(soil_tension+sunshine_hour)

    water.input['soil_tension'] = soil_tension
    water.input['sunshine_hour'] = sunshine_hour
    water.input['delta_evaporation'] = delta_evaporation
    water.input['last_watering'] = last_watering

    water.compute()

    return jsonify(water.output['watering_time'])


if __name__ == '__main__':
    app.run(debug=True, port=5000)

