import json

def test_crawapp(
    create_app 
    ):
    url = 'https://www.fundsexplorer.com.br/ranking'    
    data_test = {
        "consult_query" : "test_rows"
    }

    response = create_app[1].post('/cons', json= data_test)
    print(response.data)
    assert False