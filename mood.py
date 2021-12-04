#!/usr/bin/python

# columns axis=0 (the default)
# rows axis=1

from scipy.interpolate import spline
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
import seaborn as sns
import datetime
import calendar
import json

MOOD_INFO_FILE = "moods_info.json"
MOOD_DATA_FILE = "mood.csv"

# lists of column titles that belong to each year in (2020, 2021)
MONTHS_2020 = ["1-20","2-20","3-20","4-20","5-20","6-20","7-20","8-20","9-20","10-20","11-20","12-20"]
MONTHS_2021 = ["1-21","2-21","3-21","4-21","5-21","6-21","7-21","8-21","9-21","10-21","11-21","12-21"]

BASE_DATE = datetime.date(2020, 1, 1)

# maps characters from csv to moods
char_mood_mapping = {
    "a": "happy",
    "b": "relaxed",
    "c": "neutral",
    "d": "anxious",
    "e": "sad",
    "f": "upset"
    }



def read_input():
    '''Read in, parse, and print input data.'''
    with open(MOOD_INFO_FILE) as file:
        mood_info = json.load(file)

    df = pd.read_csv(MOOD_DATA_FILE)

    print("raw data...\n")
    counts(df)

    return mood_info, df


def counts(df):
    '''Collapse original df into monthly counts to summarize data.'''
    df_monthly_counts = df.apply(pd.value_counts)
    df_monthly_counts.drop(["x"], inplace=True)
    df_monthly_counts.rename(index=char_mood_mapping, inplace=True)

    print(df_monthly_counts)


def get_days_and_percentages(df, mood_info):
    '''Calculate day counts and percentages by mood.'''
    total_days = df.shape[0] * df.shape[1] - (df.values == "x").sum()

    days = []
    percents = []
    for m in mood_info.keys():
        num_days = (df.values == mood_info[m]["char"]).sum()
        days.append(num_days)
        percent = int(round(num_days/total_days, 2) * 100)
        percents.append(percent)

    return days, percents


def total(df, mood_info):
    days, percents = get_days_and_percentages(df, mood_info)
    percents_str = [str(p) + "%" for p in percents]

    df_total = pd.DataFrame({'days':days,'%':percents_str}, index=list(mood_info.keys()))
    print("in total...\n\n", df_total.to_string(), end="\n\n")


def annual(df, mood_info):
    '''Plot bar chart of annual mood percentages.'''

    # 2020
    days2020, percents2020 = get_days_and_percentages(df[MONTHS_2020], mood_info)
    ser2020 = pd.Series(percents2020, index=list(mood_info.keys()))

    # 2021
    days2021, percents2021 = get_days_and_percentages(df[MONTHS_2021], mood_info)
    ser2021 = pd.Series(percents2021, index=list(mood_info.keys()))

    # plot double bar: https://stackoverflow.com/questions/53228762/matplotlib-double-bar-graph-with-pandas-series
    annual_df = pd.DataFrame({"2020":ser2020, "2021":ser2021})
    ax = annual_df.plot.bar(rot=0)
    ax.set_xlabel("moods")
    ax.set_ylabel("%")

    # add bar annotations
    # for p in ax.patches:
    #     ax.annotate(str(p.get_height()), (p.get_x() * 1.02, p.get_height() * 1.02), fontsize=8)

    plt.show()


def time_series(df, mood_info):
    '''Build and plot time series sentiment data.'''
    time_series_data = []
    for month, row in df.T.iterrows():
        for day, el in enumerate(row):
            if el != 'x': # ignore trailing days
                mood = char_mood_mapping[el] # get mood from char element
                time_series_data.append(mood_info[mood]["sentiment"]) # append sentiment val

    # create date range
    dates = [BASE_DATE + datetime.timedelta(days=x) for x in range(len(time_series_data))]

    # create df out of dates and sentiment data
    df_time_series = pd.DataFrame({'date': dates, 'sentiment': time_series_data})

    # calculate rolling means
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



def main():
    mood_info, df = read_input()

    days = df.shape[0] * df.shape[1] - (df.values == "x").sum()
    print("you have tracked your mood for", days, "days!")

    # set seaborn/color themes
    sns.set()
    sns.set_palette("Paired")

    total(df, mood_info)
    annual(df, mood_info)

    time_series(df, mood_info)



if __name__ == '__main__':
        main()
