import logging
import pandas as pd
from fastapi import APIRouter
from pydantic import BaseModel, Field, validator
import joblib
from app.api.return_feedback import feedback
import numpy as np

# Connecting to fast API
log = logging.getLogger(__name__)
router = APIRouter()


# Retrieves and stores data from the API
class Success(BaseModel):
    """Use this data model to parse the request body JSON."""
    title: str = Field(..., example='Water bike')
    description: str = Field(..., example='A bike that floats')
    monetary_goal: int = Field(..., example=5000)
    launch_date: str = Field(..., example='2020/08/06')
    finish_date: str = Field(..., example='2020/10/20')
    category: str = Field(..., example='sports')

    def prep_data(self):
        """Prepares the data to be sent to the machine learning
        model as a dataframe row"""
        df = pd.DataFrame([dict(self)])
        df['title_desc'] = df['title'] + " " + df['description']
        df['launch_date'] = pd.to_datetime(df['launch_date'],
                                           format='%Y/%m/%d')
        df['finish_date'] = pd.to_datetime(df['finish_date'],
                                           format='%Y/%m/%d')
        df['monetary_goal'] = pd.to_numeric(df['monetary_goal'])
        return df

    @validator('title')
    def title_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'{value} == title, title value must be a string'
        return value

    @validator('description')
    def blurb_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'blurb == {value}, blurb value must be a string'
        return value

    @validator('monetary_goal')
    def goal_must_be_positive(cls, value):
        assert value > 0, f'goal == {value}, goal value must be > 0'
        return value

    @validator('launch_date')
    def launch_date_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'launch_date == {value}, launch_date ' \
                    f'value must be a string'
        return value

    @validator('finish_date')
    def deadline_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'deadline == {value}, deadline value must be a string'
        return value

    @validator('category')
    def category_must_be_str(cls, value):
        assert value.isdigit(
        ) == False, f'{value} == title, title value must be a string'
        return value


# Returns a prediction to anyone making a request to the API
@router.post('/predict')
async def predict(success: Success):
    """
    Make a prediction of kickstarter success or fail

    ### Request Body
     - 'title': 'string (title of campaign)',
     - 'description': 'string (Description of campaign)',
     - 'monetary_goal': 'int (monetary goal)',
     - 'launch_date': 'string (date in yyyy/mm/dd format)',
     - 'finish_date': 'string (date in yyyy/mm/dd format)',
     - 'category': 'string (category of campaign)'

    ### Response
    -  'prediction': boolean, pass or fail,
    representing the predicted class's probability
    -  'probability_of_success': int, percentage
    probability of having a successful campaign
    -  'monetary_feedback': string, feedback
    about monetary goal of the campaign
    -  'Title_feedback': string, feedback about
    the length of your campaign's title
    -  'description_feedback': string, feedback about
    the length of your campaign's description
    -  'campaign_time_feedback': string, feedback about
    the duration of your campaign
    -  'month_feedback': string, feedback about when it's
    the best time to launch your campaign
    """
    # Unpickling machine learning model
    model = joblib.load('app/api/lrm_model.pkl')

    # Feeding user data to the model
    df = success.prep_data()
    df2 = df['title_desc'][0]
    prediction = int((model.predict([df2]))[0])
    probability_of_success = np.round(((model.predict_proba(['title']))[0][1])*100)

    # Returning feedback to the user
    monetary_feedback, title_feedback, description_feedback, \
        campaign_len_feedback, month_launched = feedback(df)
    return {
        'prediction': prediction,
        'probability_of_success': probability_of_success,
        'monetary_feedback': monetary_feedback,
        'Title_feedback': title_feedback,
        'description_feedback': description_feedback,
        'campaign_time_feedback': campaign_len_feedback,
        'month_feedback': month_launched
    }
