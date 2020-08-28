from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_valid_input():
    """Return 200 Success when input is valid."""
    response = client.post(
        '/predict',
        json={
            'title': 'Water bike',
            'description': 'A bike that floats',
            'monetary_goal': 5000,
            'launch_date': '2020/08/06',
            'finish_date': '2020/10/20',
            'category': 'sports' 
        }
    )
    assert response.status_code == 200


def test_invalid_input():
    """Return 422 Validation Error when x1 is negative."""
    response = client.post(
        '/predict',
        json={
            'title': 'Water bike',
            'blurb': 'A bike that floats',
            'goal': 'e',
            'launch_date': '08/06/2020',
            'deadline': '10/20/2020',
            'category': 'sports'
        }
    )
    assert response.status_code != 200
