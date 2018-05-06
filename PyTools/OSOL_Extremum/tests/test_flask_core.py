import pytest
import json

from OSOL_Extremum.computational_core.flask_core import create_app
from OSOL_Extremum.computational_core.core_tuner import core_tuner
from OSOL_Extremum.arithmetics.interval import Interval


@pytest.fixture
def app():
    app = create_app()
    try:
        core_tuner(app, core_path='../../Tasks/Dummy/Dummy_3.json')
    except FileNotFoundError:
        core_tuner(app, core_path='../../../Tasks/Dummy/Dummy_3.json')
    return app

@pytest.fixture
def client():
    return app().test_client()


def test_real_f(client):
    data = {
        'x': 1,
        'y': 2,
        'z': 3
    }
    url = '/process_request?field=f'
    for k, v in data.items():
        url += '&{0}={1}'.format(k, json.dumps(v))

    response = client.get(url)
    output = json.loads(response.data)

    assert response.status_code == 200
    assert output == 36.0


def test_real_df(client):
    data = {
        'x': 3,
        'y': -2,
        'z': 11
    }
    url = '/process_request?field=df_grad'
    for k, v in data.items():
        url += '&{0}={1}'.format(k, json.dumps(v))

    response = client.get(url)
    output = json.loads(response.data)

    assert response.status_code == 200
    assert output[0] == 6.0
    assert output[1] == -8.0
    assert output[2] == 66.0


def test_interval_f(client):
    data = {
        'x': Interval(1, 2),
        'y': Interval(2, 3),
        'z': Interval(3, 4)
    }
    url = '/process_request?field=f&scope=interval'
    for k, v in data.items():
        url += '&{0}={1}'.format(k, json.dumps(v))

    response = client.get(url)
    output = Interval.from_dict(json.loads(response.data))

    assert response.status_code == 200
    assert output == Interval(36.0, 70.0)


def test_interval_df(client):
    data = {
        'x': Interval(3, 4),
        'y': Interval(-2, 1),
        'z': Interval.from_value(11)
    }
    url = '/process_request?field=df_grad&scope=interval'
    for k, v in data.items():
        url += '&{0}={1}'.format(k, json.dumps(v))

    response = client.get(url)
    output = list(map(Interval.from_dict, json.loads(response.data)))

    assert response.status_code == 200
    assert output[0] == Interval(6, 8)
    assert output[1] == Interval(-8, 4)
    assert output[2] == Interval.from_value(66.0)
