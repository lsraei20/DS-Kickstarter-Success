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
    assert response.json() == {
        "prediction": 0,
        "probability_of_success": 5,
        "monetary_feedback": "Your goal is right in line with successful campaigns like yours! (keep in mind this is just a suggestion and there are a lot of other variables, like the nature of your product)",
        "Title_feedback": "Your title is shorter than the average successful campaign in the sports category, you should try adding 25 characters to it!",
        "description_feedback": "Can you say a bit more? Most winning Kickstarter's in the sports category have a longer description. Try adding about 93 characters. We found that your campaign's description can be the most important section to your success!",
        "campaign_time_feedback": "Your campaign lasts quite longer than most winning campaigns in the sports category. Try decreasing your campaign time by 38 days. Believe it or not a shorter campaign can actually increase your funding!",
        "month_feedback": "By looking at other posts in the sports category, we detected that the chances of your Kickstarter success might increase by 0.01% if you wait to post next month. Something to think about!"
    }


# def test_invalid_input():
#     """Return 422 Validation Error when x1 is negative."""
#     response = client.post(
#         '/predict',
#         json={
#             'title': 'Water bike',
#             'blurb': 'A bike that floats',
#             'goal': '5000',
#             'launch_date': '08/06/2020',
#             'deadline': '10/20/2020',
#             'category': 'sports'
#         }
#     )
#     body = response.json()
