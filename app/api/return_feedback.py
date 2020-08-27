"""Returns feedback to the user based on other successful kickstarters"""
import pandas as pd


def feedback(df):
    """Cleaning data from the csv"""
    df_cat = pd.read_csv('app/api/data/kickstarter_data_with_features.csv')
    # These are the only columns we can use as input
    df_cat = df_cat[['name', 'goal', 'blurb', 'launched_at', 'deadline',
                     'category', 'state', 'country']]
    # filter out all countries not english-speaking
    english_countries = ['US', 'IE', 'GB', 'AU', 'CA', 'NZ', ]
    df_cat = df_cat[df_cat['country'].isin(english_countries)]
    # Convert fail or success to 0 or 1
    df_cat['state'] = df_cat['state'].replace({'failed': 0, 'successful': 1})
    # separate dataframe created below,
    # one of only success and another with both
    df_cat_losers = df_cat.copy()
    df_cat = df_cat[df_cat['state'] == 1]

    # Using cleaned data to retrieve numbers to be used based on category
    def retrieve_input(df_cat, df_cat_losers):

        # Title length
        def length(df):
            return len(df)

        df_cat['name_len'] = df_cat['name'].apply(length)
        title_length = df_cat['name_len'].mean()

        # Description length
        df_cat['blurb_len'] = df_cat['blurb'].apply(length)
        blurb_length = df_cat['blurb_len'].median()

        # Campaign Length avg
        def campaign_len(df):
            df['deadline'] = df['deadline'].str[:10]
            df['launched_at'] = df['launched_at'].str[:10]
            df['deadline'] = pd.to_datetime(df['deadline'],
                                            format="%Y/%m/%d")
            df['launched_at'] = pd.to_datetime(df['launched_at'],
                                               format="%Y/%m/%d")
            # create new column
            df['cam_length'] = df['deadline'] - df['launched_at']
            return df

        campaign_len_days = campaign_len(df_cat)['cam_length'].mean().days

        # Monetary goal median
        monetary_goal_median = df_cat['goal'].median()

        # Month of release avg
        df_cat["month_launched"] = df_cat['launched_at']
        df_cat["month_launched"] = pd.to_datetime(df_cat["month_launched"],
                                                  format="%Y/%m/%d")
        df_cat_losers["month_launched"] = df_cat_losers['launched_at']
        df_cat_losers["month_launched"] = pd.to_datetime(df_cat_losers
                                                         ["month_launched"],
                                                         format="%Y/%m/%d")

        def extract_month(df):
            return df.month

        df_cat['month_launched'] = df_cat['month_launched'] \
            .apply(extract_month)
        df_cat_losers['month_launched'] = df_cat_losers['month_launched'] \
            .apply(extract_month)

        def separate(df):
            df = df.reset_index(drop=True)
            dic = {}
            for row in range(df['month_launched'].value_counts().sum()):
                if df.loc[row, 'month_launched'] in dic.keys():
                    dic[df.loc[row, 'month_launched']] += 1
                else:
                    dic[df.loc[row, 'month_launched']] = 1
            return dic

        successful_dict = separate(df_cat)
        total_dict = separate(df_cat_losers)
        month_proba_dic = ({k: successful_dict[k] / total_dict[k] for k in
                            total_dict.keys() & successful_dict})

        return title_length, blurb_length, campaign_len_days, \
               monetary_goal_median, month_proba_dic

    # If the category has less than 150 rows it will use the
    # numbers from all categories instead
    if len(df_cat[df_cat['category'] == df.loc[0, 'category']]) > 150:
        df_cat_losers = df_cat_losers[df_cat_losers['category'] ==
                                      df.loc[0, 'category']]
        df_cat = df_cat[df_cat['category'] == df.loc[0, 'category']]
        title_length, blurb_length, campaign_len_days, monetary_goal_median, \
        month_proba_dic = retrieve_input(df_cat, df_cat_losers)
    else:
        title_length, blurb_length, campaign_len_days, monetary_goal_median, \
        month_proba_dic = retrieve_input(df_cat, df_cat_losers)

    # Now that we have the numbers based on category
    # we can feed them into conditionals
    # Title feedback
    if (title_length - 6) <= len(df.loc[0, 'title']) <= (title_length + 6):
        title_feedback = "Your title looks great!"
    elif len(df.loc[0, 'title']) > (title_length + 5):
        title_feedback = "Hmm. You should remove about " + \
                         str(int(len(df.loc[0, 'title']) - (title_length + 5))) \
                         + " characters from the title to be in the length " \
                           "range of most winning campaigns in the " + \
                         df.loc[0, 'category'] + " category."
    elif len(df.loc[0, 'title']) < (title_length - 5):
        title_feedback = "Your title is shorter than the average successful" \
                         " campaign in the " + df.loc[0, 'category'] + \
                         " category, you should try adding " + \
                         str(int((title_length - 5) - len(df.loc[0, 'title']))) \
                         + " characters to it!"

    # Description feedback
    if len(df.loc[0, 'description']) > (blurb_length + 20):
        description_feedback = "Uh oh. Your description is longer than the " \
                               "average successful Kickstarter in the " + \
                               df.loc[0, 'category'] + " category. Try " \
                                                       "removing about "\
                               + str(int(len(df.loc[0, 'description'])
                                         - (blurb_length + 20))) + \
                               " characters. We found that your campaign's" \
                               " description can be the most important " \
                               "section to your success!"
    elif len(df.loc[0, 'description']) < (blurb_length - 15):
        description_feedback = "Can you say a bit more? Most winning " \
                               "Kickstarter's in the " + \
                               df.loc[0, 'category'] + " category have a" \
                               " longer description. Try adding about " \
                               + str(int((blurb_length - 15) -
                                         len(df.loc[0, 'description'])))\
                               + " characters. We found that your " \
                                 "campaign's description can be the most" \
                                 " important section to your success!"
    else:
        description_feedback = "Perfect description!"

    # Campaign length feedback
    def campaign_len(df):
        df['finish_date'] = df['finish_date']
        df['launch_date'] = df['launch_date']
        df['finish_date'] = pd.to_datetime(df['finish_date'],
                                           format="%Y/%m/%d")
        df['launch_date'] = pd.to_datetime(df['launch_date'],
                                           format="%Y/%m/%d")
        # create new column
        df['cam_length'] = df['finish_date'] - df['launch_date']
        return df

    if campaign_len(df)['cam_length'].mean().days > (campaign_len_days + 5):
        campaign_len_feedback = "Your campaign lasts quite longer than " \
                                "most winning campaigns in the " + \
                                df.loc[0, 'category'] + " category. Try" \
                                " decreasing your campaign time by " + \
                                str(int(campaign_len(df)['cam_length']
                                        .mean().days -
                                        (campaign_len_days + 5))) + \
                                " days. Believe it or not a shorter " \
                                "campaign can actually increase " \
                                "your funding!"
    elif campaign_len(df)['cam_length'].mean().days < (campaign_len_days - 5):
        campaign_len_feedback = "Some more time perhaps? your campaign" \
                                " is quite shorter than most successful" \
                                " campaigns in the " + \
                                df.loc[0, 'category'] + " category. You " \
                                "should consider giving people about " \
                                + str(int((campaign_len_days - 5) -
                                          campaign_len(df)['cam_length']
                                          .mean().days)) + \
                                " more days to fund!"
    else:
        campaign_len_feedback = "Your campaign length is right in line " \
                                "with the most successful Kickstarters!"

    # Monetary goal feedback
    if df.loc[0, 'monetary_goal'] > (monetary_goal_median + 3000):
        monetary_feedback = "Your monetary goal is higher than most " \
                            "successful campaigns in the " + \
                            df.loc[0, 'category'] + " category. You " \
                            "should consider lowering it by $" + \
                            str(int(df.loc[0, 'monetary_goal'] -
                                    (monetary_goal_median + 3000))) + \
                            " for more chances of success. (keep in mind" \
                            " this is just a suggestion and there are a" \
                            " lot of other variables, like the nature " \
                            "of your product)"
    elif df.loc[0, 'monetary_goal'] < (monetary_goal_median - 3000):
        monetary_feedback = "Your goal is lower than average for " \
                            "successful campaigns in the " + \
                            df.loc[0, 'category'] + " category. Why " \
                            "not bump it up a bit? just about $" + \
                            str(int((monetary_goal_median - 3000) -
                                    df.loc[0, 'monetary_goal'])) + \
                            " more would be perfect (keep in mind " \
                            "this is just a suggestion and there are" \
                            " a lot of other variables, like the " \
                            "nature of your product)"
    else:
        monetary_feedback = "Your goal is right in line with successful " \
                            "campaigns like yours! (keep in mind this is " \
                            "just a suggestion and there are a lot of other" \
                            " variables, like the nature of your product)"

    # Release month feedback
    if month_proba_dic[df.loc[0, "launch_date"].month] < \
            month_proba_dic[(df.loc[0, "launch_date"].month + 1) % 12]:
        month_launched_feedback = "By looking at other posts in the " + \
                                  df.loc[0, 'category'] + " category, we" \
                                  " detected that the chances of your " \
                                  "Kickstarter success might increase " \
                                  "by " + str(round(((month_proba_dic
                                  [(df.loc[0, "launch_date"].month + 1)
                                  % 12] - month_proba_dic[df.loc
                                  [0, "launch_date"].month])*100), 2)) + \
                                  "% if you wait to post next month. " \
                                  "Something to think about!"
    else:
        month_launched_feedback = "You picked a great time to post! This " \
                                  "month gives you the greatest chances of" \
                                  " success when compared to next month," \
                                  " so get posting!"

    return monetary_feedback, title_feedback, description_feedback, \
           campaign_len_feedback, month_launched_feedback
