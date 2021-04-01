from flask import Flask, request
from craw_app.craw.craw import crawler
from craw_app.process_data.transform import transform_data
from craw_app.database.db_send_data import insert_rows
from craw_app.database.db_consult import consult_big_query
import os

def call_crawler(url, number_pages):
    dict_return = crawler(url, number_pages)
    transform_dict = transform_data().alter(dict_return)
    insert_rows(transform_dict)
    return 'crawler'

def call_database(consult_query):
    consult_big_query(consult_query)
    return 'database'

def create():
    app = Flask(__name__)
    app.config.from_object(os.getenv('APP_CONFIG'))


    @app.route("/craw",endpoint='end1', methods=(['POST']))
    def routes_api():
        url = request.get_json()['url']
        number_pages = request.get_json()['number_pages']
        return call_crawler(url, number_pages)
    
    @app.route("/cons",endpoint='end2', methods=(['POST']))
    def routes_api2():
        consult_query = request.get_json()['consult_query']
        return call_database(consult_query)

    return app


