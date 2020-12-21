#!/usr/bin/python

from scipy.interpolate import spline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
import calendar
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

# print frequencies of each mood in data
def get_frequencies(data):
    unique, counts = np.unique(data, return_counts=True)
    frequencies = dict(zip(unique, counts))
    if 'x' in frequencies.keys(): del frequencies['x'] # ignore trailing days
    print("frequencies:", frequencies)

# calculate and print year stats
def year_stats(df, df_counts, mood_categories, mood_colors):
    total_days = df.shape[0] * df.shape[1] - (df.values == "x").sum()
    print("you tracked your mood for", total_days, "days this year!\n")

    print("year breakdown:")
    days = []
    percentages = []
    percentages_vals = []
    for m in mood_categories:
        num_days = (df.values == m).sum()
        days.append(num_days)
        percentages.append(str(int(round(num_days/total_days, 2) * 100)) + "%")
        percentages_vals.append(int(round(num_days/total_days, 2) * 100))

    df_year_stats = pd.DataFrame([mood_categories,days,percentages]).T
    df_year_stats.columns = ['mood','days','percentage']
    print(df_year_stats.to_string(index=False), end="\n\n")

    # plot
    fig, ax = plt.subplots()
    ax.bar(mood_categories, percentages_vals, color=mood_colors.values())
    plt.xlabel('mood')
    plt.ylabel('percentage')
    plt.show()

    # most/least common moods
    max_mood = str(df_year_stats.mood[df_year_stats.days.idxmax()])
    min_mood = str(df_year_stats.mood[df_year_stats.days.idxmin()])
    print("you felt most frequently", max_mood, "this year, and least frequently", min_mood, end="\n\n")

# calculate and print season stats
def season_stats(df, df_counts, mood_categories):
    print("\nnow lets break it down by season...\n")
    season_mapping = {"january": "winter", "february": "winter", "march": "spring", "april": "spring", "may": "spring", "june": "summer", "july": "summer", "august": "summer", "september": "fall", "october": "fall", "november": "fall", "december": "winter"}
    df_seasonal = df_counts.groupby(season_mapping, axis=1).sum()
    df_seasonal.reset_index(level=0)
    print(df_seasonal)

# build time series data
def build_time_series_raw(df, mood_categories, sentiment_mapping):
    # flatten + convert data to sentiment val
    print("\nconverting data to sentiment time series...")
    time_series_data = []
    for month, row in df.T.iterrows():
        for day, el in enumerate(row):
            if el != 'x': # ignore trailing days
                # print(month, day+1, el, ":", sentiment_mapping[el])
                time_series_data.append(sentiment_mapping[el]) # append sentiment val

    # create date range
    base = datetime.date(2020, 1, 1)
    dates = [base + datetime.timedelta(days=x) for x in range(len(time_series_data))]

    # create df out of dates and sentiment data
    df_time_series = pd.DataFrame({'date': dates, 'sentiment': time_series_data})
    return df_time_series

# plot time series
def plot_time_series(df_time_series):
    # calculate rolling means
    print("\ncalculating rolling means...")
    df_time_series['seven day rolling mean'] = df_time_series.sentiment.rolling(7).mean()
    df_time_series['thirty day rolling mean'] = df_time_series.sentiment.rolling(30).mean()

    # print(df_time_series)
    print("overall mean:", df_time_series["sentiment"].mean())
    print("standard deviation:", df_time_series["sentiment"].std())

    # plot
    time_series_colors = ["#E1C8FB", "#AB69EF", "#3B0279"]
    ax = df_time_series.plot(x='date', y=['sentiment', 'seven day rolling mean', 'thirty day rolling mean'], figsize=(11, 4), linewidth=0.8, color=time_series_colors)

    # customize axes
    ax.set_ylabel("sentiment")
    ax.xaxis.get_label().set_visible(False)

    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b %Y"))

    plt.show()

# ret weekday name from day, month, year input
def what_weekday(year, month, day):
    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    date = datetime.date(year, month, day)
    return weekdays[date.weekday()]

# build weekly aggregated data
def build_weekly_data(df, mood_categories, mood_colors):
    year = 2020
    month_mapping = {month.lower(): index for index, month in enumerate(calendar.month_name) if month}

    # build mood counts by weekday
    print("\ncalculating weekly mood counts...")
    df_weekly = pd.DataFrame(0, index=["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"], columns=["happy", "relaxed", "neutral", "sad", "anxious", "upset"])
    for month, row in df.T.iterrows():
        for day, mood in enumerate(row):
            if mood != 'x': # ignore trailing days
                weekday = what_weekday(year, month_mapping[month], int(day+1))
                df_weekly.at[weekday, mood] += 1
    return df_weekly

# print weekly stats
def weekly_stats(df_weekly, sentiment_mapping):
    # print weekly mean sentiment values
    print(df_weekly)
    print("\ncalculating mean sentiement by weekday...")
    for day_of_week, row in df_weekly.iterrows():
        day_sentiment_total = row["happy"]*sentiment_mapping["happy"] + row["relaxed"]*sentiment_mapping["relaxed"] + row["neutral"]*sentiment_mapping["neutral"] + row["sad"]*sentiment_mapping["sad"] + row["anxious"]*sentiment_mapping["anxious"] + row["upset"]*sentiment_mapping["upset"]
        num_days = row["happy"] + row["relaxed"] + row["neutral"] + row["sad"] + row["anxious"] + row["upset"]
        day_sentiment_mean = day_sentiment_total / num_days
        print(day_of_week, ":", day_sentiment_mean)

# plot weekly mood counts in vertically stacked subplots
def plot_weekly_trends_stacked(df_weekly, mood_categories, mood_colors):
    # plot w vertically stacked subplots
    fig, axes = plt.subplots(6, sharex=True, sharey=True, figsize=(6, 9))
    fig.suptitle('weekly mood counts')

    # 6 axes, for 6 mood line plots
    for index, ax in enumerate(axes):
        mood = mood_categories[index]

        x = list(range(0, 7)) # has to be numeric because to interpolate for smooth lines
        y = df_weekly[mood].tolist()

        # smooth lines
        x_sm = np.array(x)
        y_sm = np.array(y)
        x_smooth = np.linspace(x_sm.min(), x_sm.max(), 200)
        y_smooth = spline(x, y, x_smooth)

        # correcting x labels
        ax.set_xticks(x)
        ax.set_xticklabels(["sun", "mon", "tue", "wed", "thur", "fri", "sat"]) # same order as df_weekly index

        ax.plot(x_smooth, y_smooth, color=list(mood_colors.values())[index], label=mood)
        ax.legend(loc="upper right")

    plt.show()

# plot weekly mood counts in one plot
def plot_weekly_trends(df_weekly, mood_categories, mood_colors):
     weekly_trends_colors = mood_colors.values()

     # plot
     ax = df_weekly.plot(figsize=(11, 4), linewidth=1.1, color=weekly_trends_colors)
     ax.set_ylabel("count")
     plt.show()

# ret df with mood strings replaced w sentiment values
def build_sentiment_df(df, sentiment_mapping):
    df_sentiment = df
    df_sentiment.replace(sentiment_mapping, inplace=True)
    return df_sentiment

def main():
    # read input
    df, df_counts, mood_categories = read_input()
    print("moods: ", mood_categories, end="\n\n")
    print("original mood data:\n", df_counts, end="\n\n")

    # set seaborn/color themes for plots
    sns.set()
    sns.set_palette("Paired")
    mood_colors = {'happy': "#FDE517", 'relaxed': "#ABD006", 'neutral': "#04D0E5", 'sad': "#0497E5", 'anxious': "#B684FA", 'upset': "#FA84AA"}

    # print long-run stats
    # year_stats(df, df_counts, mood_categories, mood_colors)
    # season_stats(df, df_counts, mood_categories)

    # assign sentiments to moods
    sentiment_mapping = {"happy": 2, "relaxed": 1, "neutral": 0, "sad": -1.5, "anxious": -1, "upset": -2}

    # build and plot time series
    df_time_series = build_time_series_raw(df, mood_categories, sentiment_mapping)
    # plot_time_series(df_time_series)

    # build and plot weekly trends
    df_weekly = build_weekly_data(df, mood_categories, mood_colors)
    # plot_weekly_trends_stacked(df_weekly, mood_categories, mood_colors)
    weekly_stats(df_weekly, sentiment_mapping)

    # day_of_interest = "friday"
    # mood_of_interest = "anxious"

if __name__ == '__main__':
        main()
