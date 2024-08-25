import re
import pandas as pd

def preprocess(data):
    # Pattern to match the date and time format in WhatsApp exported chat
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s?[APMapm]{2}\s-\s'

    # Extract messages and dates using regex
    messages = re.split(pattern, data)[1:]  # Skip the first element which is empty before the first message
    dates = re.findall(pattern, data)

    # Create DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    # Convert message_date to datetime format
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p - ')

    # Rename the column
    df.rename(columns={'message_date': 'date'}, inplace=True)

    # Splitting user and message
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if len(entry) > 1:  # If the message has a user
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    # Adding more datetime-related columns
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df
