#!/usr/bin/python

import pandas as pd
import numpy as np
import json

# read in data
def read_input():
    # build mood categories
    mood_categories = []
    with open("mood_categories.txt") as f:
        for line in f:
            mood_categories.append(line.split(":")[0])
    print("moods: ", mood_categories, end="\n\n")

    # read in mood tracked data
    df = pd.read_csv("mood.csv")
    df_counts = df.apply(pd.value_counts)
    print("original mood data:\n", df_counts, end="\n\n")

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

# calculate and print monthly stats
def monthly_stats():
    for (month, month_data) in df.iteritems():
        print('month: ', month)
        get_frequencies(month_data.values)

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
    df_seasonal =df_counts.groupby(season_mapping, axis=1).sum()
    df_seasonal.reset_index(level=0)
    print(df_seasonal)

def main():
        df, df_counts, mood_categories = read_input()

        # print stats
        year_stats(df, df_counts, mood_categories)
        season_stats(df, df_counts, mood_categories)

if __name__ == '__main__':
        main()
