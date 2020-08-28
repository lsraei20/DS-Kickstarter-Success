API Which can make a prediction of kickstarter success or fail using a xgboost multi-model and returning tailored feedback based on category of kickstarter and the properties of it.

You can access and send a request through this website:

https://kickstarter-success-rate.herokuapp.com/

or using this command with default dummy input which you can change:

curl -X POST "https://kickstarter-success-rate.herokuapp.com/predict" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"title\":\"Water bike\",\"description\":\"A bike that floats\",\"monetary_goal\":5000,\"launch_date\":\"2020/08/06\",\"finish_date\":\"2020/10/20\",\"category\":\"sports\"}"


Request Body

'title': 'string (title of campaign)',
'description': 'string (Description of campaign)',
'monetary_goal': 'int (monetary goal)',
'launch_date': 'string (date in yyyy/mm/dd format)',
'finish_date': 'string (date in yyyy/mm/dd format)',
'category': 'string (category of campaign)'


Response

'prediction': boolean, pass or fail, representing the predicted class's probability
'probability_of_success': int, percentage probability of having a successful campaign
'monetary_feedback': string, feedback about monetary goal of the campaign
'Title_feedback': string, feedback about the length of your campaign's title
'description_feedback': string, feedback about the length of your campaign's description
'campaign_time_feedback': string, feedback about the duration of your campaign
'month_feedback': string, feedback about when it's the best time to launch your campaign
