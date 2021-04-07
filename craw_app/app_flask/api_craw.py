from flask import Flask, request, render_template, jsonify
from craw_app.craw.craw import crawler
from craw_app.process_data.transform import transform_data
from craw_app.database.db_send_data import insert_rows
from craw_app.database.db_consult import consult_big_query
from craw_app.machinelearning.ml import machineleaning_actions
import os

def call_crawler(url, number_pages):
    dict_return = crawler(url, number_pages)
    transform_dict = transform_data().alter(dict_return)
    insert_rows(transform_dict)
    return 'crawler'

# def do_something(text1,text2, text3):
#    text1 = text1.upper()
#    text2 = text2.upper()
#    text3 = text3.upper()
#    combine = text1 + text2 + text3
#    return combine

def call_machine_training(machine):

    machine.training_model()
    return 'Model Trained'

def call_machine_predict(houses, machine):
    pred = machine.predicts(houses)
    return pred

def call_database(consult_query):
    consult_big_query(consult_query)
    return 'database'

def create():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG'))
    machine = machineleaning_actions()

    @app.route("/",endpoint='end0')
    def routes_api0():
        return render_template('index.html')

    # Fix it to put a simple frontend
    # @app.route('/join', methods=['GET','POST']) 
    # def my_form_post():
    #     text1 = request.form['text1']
    #     text2 = request.form['text2']
    #     text3 = request.form['text3']
    #     combine = do_something(text1,text2,text3)
    #     result = {
    #         "output": combine
    #     }
    #     result = {str(key): value for key, value in result.items()}
    #     return jsonify(result=result)

    @app.route("/craw",endpoint='end1', methods=(['POST']))
    def routes_api1():
        url = request.get_json()['url']
        number_pages = request.get_json()['number_pages']
        return call_crawler(url, number_pages)
    
    @app.route("/ml",endpoint='end2', methods=(['POST']))
    def routes_api2():
        return call_machine_training(machine)
    
    @app.route("/pred",endpoint='end3', methods=(['POST']))
    def routes_api3():
        prediction = request.get_json()['predict']
        return call_machine_predict(prediction, machine)

    @app.route("/cons",endpoint='end4', methods=(['POST']))
    def routes_api4():
        consult_query = request.get_json()['consult_query']
        return call_database(consult_query)
    
    return app


