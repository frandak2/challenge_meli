from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)

def test_no_atraso_prediction():
    response = client.post('/v1/prediction', json = {
                                                    'DIA': 1,
                                                    'MES': 1,
                                                    'HORA': 0,
                                                    'MIN': 15,
                                                    'SEG': 15,
                                                    'DIANOM': 'Domingo',
                                                    'MESNOM': 'Ene'
                                                })
    assert response.status_code == 200
    assert response.json()['your_y_variable'] == 0 

def test_atraso_prediction():
    response = client.post('/v1/prediction', json = {
                                                    'DIA': 1,
                                                    'MES': 1,
                                                    'HORA': 0,
                                                    'MIN': 15,
                                                    'SEG': 15,
                                                    'DIANOM': 'Domingo',
                                                    'MESNOM': 'Ene'
                                                })
    assert response.status_code == 200
    assert response.json()['your_y_variable'] == 1




