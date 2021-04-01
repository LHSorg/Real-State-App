from google.cloud import bigquery
from flask import current_app as app

def call_query(item):
    table_id = app.config['BIGQUERY_TABLE']
    querys = {
        'all_rows': (f"""
                    SELECT *
                    FROM {table_id}
                    LIMIT 1000 """),
        'count_rows': (f"""
                    SELECT COUNT(*)
                    FROM {table_id}
                    LIMIT 1000 """),
        'test_rows': (f"""
                    SELECT *
                    FROM {table_id}
                    WHERE preco_atual > 14
                    LIMIT 1000 """)           
    }
    return (querys.get(item, "Invalid Item"))

def consult_big_query(consult_query):
    bigquery_client = bigquery.Client(project=app.config['GCP_PROJECT'])
    query_return = call_query(consult_query)
    query_job = bigquery_client.query(query_return)
    results = query_job.result() 
    for row in results:
        print(f'{dict(row)}\n')
    