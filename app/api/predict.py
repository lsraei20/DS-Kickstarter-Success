import logging
from fastapi import APIRouter
import pandas as pd
from pydantic import BaseModel, Field, validator

log = logging.getLogger(__name__)
router = APIRouter()


class Success(BaseModel):
    """Use this data model to parse the request body JSON."""
    title: str = Field(..., example='Water bike')
    blurb: str = Field(..., example='A bike that floats')
    goal: int = Field(..., example=5000)
    launch_date: str = Field(..., example='08/06/2020')
    deadline: str = Field(..., example='10/20/2020')
    category: str = Field(..., example='sports')

    def prep_data(self):
        """Prepare the data to be sent to the machine learning model"""
        df = pd.DataFrame([dict(self)])
        df['title_desc'] = df['title'] + " " + df['description']
        df2 = df['title_desc']
        print(df2)
        df['launch_date'] = pd.to_datetime(
            df['launch_date'], format='%Y/%m/%d')
        df['finish_date'] = pd.to_datetime(
            df['finish_date'], format='%Y/%m/%d')
        df['monetary_goal'] = pd.to_numeric(df['monetary_goal'])
        return df2

    @validator('title')
    def title_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'{value} == title, title value must be a string'
        return value,

    @validator('blurb')
    def blurb_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'blurb == {value}, blurb value must be a string'
        return value

    @validator('goal')
    def goal_must_be_positive(cls, value):
        assert value > 0, f'goal == {value}, goal value must be > 0'
        return value

    @validator('launch_date')
    def launch_date_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'launch_date == {value}, launch_date value must be a string'
        return value

    @validator('deadline')
    def deadline_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'deadline == {value}, deadline value must be a string'
        return value

    @validator('category')
    def category_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'category == {value}, category value must be a string'
        return value


@router.post('/predict')
async def predict(success: Success):
    """
    Make a prediction of kickstarter success or fail

    # Request Body
     - 'title': 'string (title of campaign)',
     - 'blurb': 'string (Description of campaign)',
     - 'goal': 'int (monetary goal)',
     - 'launch_date': 'string (date in dd/mm/yyyy format)',
     - 'deadline': 'string (date in dd/mm/yyyy format)',
     - 'category': 'string (category of campaign)'

    # Response
    - `campaign id`: unique campaign identifier
    - `prediction`: boolean, pass or fail,
    representing the predicted class's probability

    """

    response = {
        "title": "Water bike",
        "blurb": "A bike that floats",
        "goal": 5000,
        "launch_date": "08/06/2020",
        "deadline": "10/20/2020",
        "category": "sports"
    }

    if len(response.get('title')) > 15:
        Title_feedback = 'too long'
    elif len(response.get('title')) < 5:
        Title_feedback = 'too short'
    else:
        Title_feedback = 'good'

    if len(response.get('blurb')) > 300:
        description_feedback = 'too long'
    elif len(response.get('blurb')) < 50:
        description_feedback = 'too short'
    else:
        description_feedback = 'good'

    prediction = 0
    probability_of_success = 75
    monetary_feedback = 'too long'
    campaign_time_feedback = 'to long'
    month_feedback = 'wait a month'

    return {
        'prediction': prediction,
        'probability_of_success': probability_of_success,
        'monetary_feedback': monetary_feedback,
        'Title_feedback': Title_feedback,
        'description_feedback': description_feedback,
        'campaign_time_feedback': campaign_time_feedback,
        'month_feedback': month_feedback
    }
