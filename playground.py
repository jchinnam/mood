#!/usr/bin/python

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
import json

# read in data
def read_input():
    print("reading input...")
    # build mood categories
    mood_categories = []
    with open("mood_categories.txt") as f:
        for line in f:
            mood_categories.append(line.split(":")[0])

    # read in mood tracked data
    df = pd.read_csv("mood.csv")
    df_counts = df.apply(pd.value_counts)

    return df, df_counts, mood_categories

# ret the most frequent mood in data
def get_max_mood(data):
    print("hi, this will have an implementation soon")

# ret month that had the highest days of that mood
def get_max_month(data, mood):
    print("hi, this will have an implementation soon")

# print frequencies of each mood in data
def get_frequencies(data):
    unique, counts = np.unique(data, return_counts=True)
    frequencies = dict(zip(unique, counts))
    if 'x' in frequencies.keys(): del frequencies['x'] # ignore trailing days
    print("frequencies:", frequencies)

# calculate and print year stats
def year_stats(df, df_counts, mood_categories):
    total_days = df.shape[0] * df.shape[1] - (df.values == "x").sum()
    print("you tracked your mood for", total_days, "days this year!\n")

    print("year breakdown:")
    days = []
    percentages = []
    for m in mood_categories:
        num_days = (df.values == m).sum()
        days.append(num_days)
        percentages.append(str(int(round(num_days/total_days, 2) * 100)) + "%")
    year_stats = [mood_categories,days,percentages]

    df_year_stats = pd.DataFrame(year_stats).T
    df_year_stats.columns = ['mood','days','percentage']
    print(df_year_stats.to_string(index=False), end="\n\n")

    # most/least common moods
    max_mood = str(df_year_stats.mood[df_year_stats.days.idxmax()])
    min_mood = str(df_year_stats.mood[df_year_stats.days.idxmin()])
    print("you felt most frequently", max_mood, "this year, and least frequently", min_mood, end="\n\n")

# calculate and print season stats
def season_stats(df, df_counts, mood_categories):
    print("now lets break it down by season...\n")
    season_mapping = {"january": "winter", "february": "winter", "march": "spring", "april": "spring", "may": "spring", "june": "summer", "july": "summer", "august": "summer", "september": "fall", "october": "fall", "november": "fall", "december": "winter"}
    df_seasonal = df_counts.groupby(season_mapping, axis=1).sum()
    df_seasonal.reset_index(level=0)
    print(df_seasonal)

# ret weekday name from day, month, year input
def what_weekday(day, month, year):
    weekdays = ("monday","tuesday","wednesday","thursday","friday","saturday","sunday")
    date = datetime.date(year, month, day)
    return weekdays[date.weekday()]

# build time series data
def build_time_series_raw(df, mood_categories, sentiment_mapping):
    # flatten + convert data to sentiment val
    print("converting data to sentiment time series...")
    time_series_data = []
    for month, row in df.T.iterrows():
        for day, el in enumerate(row):
            if el != 'x': # ignore trailing days
                # print(month, day+1, el, ":", sentiment_mapping[el])
                time_series_data.append(sentiment_mapping[el]) # append sentiment val

    # create date range
    base = datetime.date(2020, 1, 1)
    dates = [base + datetime.timedelta(days=x) for x in range(len(time_series_data))]

    # plot raw time series
    # plt.figure(figsize=(20,3))
    # plt.plot(dates,time_series_data)
    # plt.show()

    # create df out of dates and sentiment data
    df_time_series = pd.DataFrame({'date': dates, 'sentiment': time_series_data})
    return df_time_series

# plot time series
def plot_time_series(df_time_series):
    # calculate rolling means
    print("calculating rolling means...")
    df_time_series['seven day rolling mean'] = df_time_series.sentiment.rolling(7).mean()
    df_time_series['thirty day rolling mean'] = df_time_series.sentiment.rolling(30).mean()
    # print(df_time_series)

    # plot
    ax = df_time_series.plot(x='date', y=['seven day rolling mean', 'thirty day rolling mean'], figsize=(11, 4), linewidth=0.8);

    # customize axes
    ax.xaxis.get_label().set_visible(False)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))

    plt.show()

def build_sentiment_df(df, sentiment_mapping):
    df_sentiment = df
    df_sentiment.replace(sentiment_mapping, inplace=True)
    return df_sentiment

def main():
    # read input
    df, df_counts, mood_categories = read_input()
    print("moods: ", mood_categories, end="\n\n")
    print("original mood data:\n", df_counts, end="\n\n")

    # set seaborn theme for plots
    sns.set()
    sns.set_palette("Paired")

    # print stats
    # year_stats(df, df_counts, mood_categories)
    # season_stats(df, df_counts, mood_categories)

    # assign sentiments to moods
    sentiment_mapping = {"happy": 2, "relaxed": 1, "neutral": 0, "sad": -2, "anxious": -1, "upset": -2}

    # build and plot time series
    df_time_series = build_time_series_raw(df, mood_categories, sentiment_mapping)
    plot_time_series(df_time_series)

    # df_sentiment = build_sentiment_df(df, sentiment_mapping)

    # day_of_interest = "friday"
    # mood_of_interest = "anxious"

if __name__ == '__main__':
        main()
