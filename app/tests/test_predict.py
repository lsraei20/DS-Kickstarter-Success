from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success when input is valid."""
    response = client.post(
        '/predict',
        json={
            'title': 'Water bike',
            'blurb': 'A bike that floats',
            'goal': '5000',
            'launch_date': '08/06/2020',
            'deadline': '10/20/2020',
            'category': 'sports'
        }
    )
    body = response.json()


def test_invalid_input():
    """Return 422 Validation Error when x1 is negative."""
    response = client.post(
        '/predict',
        json={
             'title': 'Water bike',
             'blurb': 'A bike that floats',
             'goal': '5000',
             'launch_date': '08/06/2020',
             'deadline': '10/20/2020',
             'category': 'sports'
        }
    )
    body = response.json()

