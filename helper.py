from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()



def fetch_stats(selected_user, df):

    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]
    #1. Number of messages
    num_messages  = df.shape[0]

    #2. Number of Words
    words = []
    for message in df['Message']:
        words.extend(message.split())

    #3. Number of Media shared
    num_media = df[df['Message'] == '<Media omitted>\n'].shape[0]

    #4. Number of links shared
    links = []
    for message in df['Message']:
        links.extend(extract.find_urls(message))
    num_links = len(links)

    return num_messages, len(words), num_media, num_links

def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    timeline = df.groupby(['Year', 'month_num', 'Month']).count()['Message'].reset_index()
    time = []

    for i in range(timeline.shape[0]):
        time.append(timeline['Month'][i] + "-" + str(timeline['Year'][i]))
    timeline['Time'] = time

    return timeline

def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['Message'].reset_index()

    return daily_timeline

def weekly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    busy_day = df['day_name'].value_counts()

    return busy_day

def monthly_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    busy_month = df['Month'].value_counts()

    return busy_month

def daily_activity(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    activity = df.pivot_table(index = 'day_name', columns = 'period', values = 'Message', aggfunc = 'count').fillna(0)

    return activity

def most_busy_users(df):
    num_busy = df['User_Name'].value_counts().head()
    pct_busy = round(
        ((df['User_Name'].value_counts()/df.shape[0])*100).reset_index().rename(columns = {
        'index': 'User_Name', 'User_Name': 'Percentage of messages'}),
        2)
    return num_busy, pct_busy

def create_wordcloud(selected_user, df):
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    temp = df[df['User_Name'] != 'Group_Notificaion']
    temp = temp[(temp['Message'] != '<Media omitted>\n') & (temp['Message'] != 'This message was deleted\n')]

    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)

        return " ".join(y)

    wc = WordCloud(width = 500, height = 500, min_font_size = 8, background_color = 'white')
    temp['Message'] = temp['Message'].apply(remove_stop_words)
    wc_df = wc.generate(temp['Message'].str.cat(sep = " "))

    return  wc_df

def most_common_words(selected_user, df):

    f = open('stop_hinglish.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['User_Name'] == selected_user]

    temp = df[df['User_Name'] != 'Group_Notificaion']
    temp = temp[(temp['Message'] != '<Media omitted>\n') & (temp['Message'] != 'This message was deleted\n')]

    words = []

    for message in temp['Message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df

def num_emoji(selected_user,df):

    if selected_user !='Overall':
        df = df[df['User_Name'] == selected_user]

    emojis = []
    for message in df['Message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return emoji_df
