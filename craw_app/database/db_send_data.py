from google.cloud import bigquery
from flask import current_app as app

def insert_rows(data):
    bigquery_client = bigquery.Client(project=app.config['GCP_PROJECT'])
    table_id = app.config['BIGQUERY_TABLE']
    table = bigquery_client.get_table(table_id)
    for iter in list(data.keys()):
        data_to_bigquery = {
            'Page': iter,
            'Quarto': data[iter]['Quartos'],
            'Banheiro': data[iter]['Banheiros'],
            'Cozinha': data[iter]['Cozinha'],
            'Quintal': data[iter]['Quintal'],
            'Salas': data[iter]['Salas'],
            'VagadeGaragem': data[iter]['VagasdeGaragem'],
            'AreadeServico': data[iter]['ÁreadeServiço'],
            'Area': data[iter]['m²deÁrea'],
            'Aceitapet': data[iter]['Aceitapet'],
            'MetroProximo': data[iter]['Metrôpróximo'],
            'Price': data[iter]['Price']
        }
        print(data_to_bigquery)
        errors = bigquery_client.insert_rows(table, [data_to_bigquery])
