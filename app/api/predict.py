import logging
import random

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

    def to_df(self):
        """Convert pydantic object to pandas dataframe with 1 row."""
        return pd.DataFrame([dict(self)])


@router.post('/predict')
async def predict(success: Success):
    """
    Make a prediction of kickstarter success or fail

    ### Request Body
     - 'title': 'string (title of campaign)',
     - 'blurb': 'string (Description of campaign)',
     - 'goal': 'int (monetary goal)',
     - 'launch_date': 'string (date in dd/mm/yyyy format)',
     - 'deadline': 'string (date in dd/mm/yyyy format)',
     - 'category': 'string (category of campaign)'

    ### Response
    - `campaign id`: unique campaign identifier
    - `prediction`: boolean, pass or fail,
    representing the predicted class's probability

    """

    campaign_id = 23548
    result = 'pass'
    return {
        'campaign id': campaign_id,
        'prediction': result
    }

