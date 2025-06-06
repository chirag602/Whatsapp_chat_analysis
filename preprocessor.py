import re
import pandas as pd

def preprocess(data):
    # Normalize hidden unicode characters (like  )
    data = data.encode('utf-8').decode('utf-8').replace('\u202f', ' ').replace('\u200e', '')

    # Updated regex for [dd/mm/yy, hh:mm:ss AM/PM] format
    pattern = r'^\[(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{2}:\d{2}\s[APMapm]{2})\] (.*?): (.*)'
    messages = []
    dates = []
    times = []
    users = []

    for line in data.splitlines():
        match = re.match(pattern, line.strip())
        if match:
            date, time, user, message = match.groups()
            dates.append(date)
            times.append(time)
            users.append(user)
            messages.append(message)

    df = pd.DataFrame({
        'date': dates,
        'time': times,
        'user': users,
        'message': messages
    })

    # Convert to datetime
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d/%m/%y %I:%M:%S %p')
    df['only_date'] = df['datetime'].dt.date
    df['year'] = df['datetime'].dt.year
    df['month_num'] = df['datetime'].dt.month
    df['month'] = df['datetime'].dt.month_name()
    df['day'] = df['datetime'].dt.day
    df['day_name'] = df['datetime'].dt.day_name()
    df['hour'] = df['datetime'].dt.hour
    df['minute'] = df['datetime'].dt.minute

    df['period'] = df['hour'].apply(lambda x: f"{x}-{(x + 1) % 24}")

    return df