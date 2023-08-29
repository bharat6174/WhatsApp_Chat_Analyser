import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{1,2},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    # creating the data frame by combining above lists
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # convert format of date as per pandas
    df['message_date'] = pd.to_datetime(df['message_date'], format='%d/%m/%y, %H:%M - ')

    df.rename(columns={'message_date': 'date'}, inplace=True)

    # seperating username and message and group notification

    users = []
    msgs = []

    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # use name
            users.append(entry[1])
            msgs.append(entry[2])
        else:
            users.append('Group_Notification')
            msgs.append(entry[0])

    df['User_Name'] = users
    df['Message'] = msgs
    df.drop(columns=['user_message'], inplace=True)

    df['Year'] = df['date'].dt.year
    df['Month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['only_date'] = df['date'].dt.date
    df['day_name'] = df['date'].dt.day_name()
    df['Day'] = df['date'].dt.day
    df['Hour'] = df['date'].dt.hour
    df['Minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'Hour']]['Hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period
    return df