# mood analysis
Across 2020 and 2021, I categorized my mood daily into 6 categories and set out to discover what I could learn about myself.

## the data
Each day was categorized into one of the following mood buckets:
1. **happy**: happy, positive
2. **relaxed**: relaxed, content
3. **neutral**: neutral, uneventful
4. **sad**: sad, lonely, depressed
5. **anxious**: stressed, anxious
6. **upset**: angry, frustrated, upset

#### sentiment
Taking into account personal understanding/weight of the mood categories, I designed a mapping to quantify the moods with the following sentiment/emotional values:
`{"happy": 2, "relaxed": 1, "neutral": 0, "anxious": -1, "sad": -1.5, "upset": -2}
`

## results & trends

#### annual overview

Below is a bar chart representation of the percentage of each year I spent in each mood. Logically, neutral is the general majority, with individual percentages of the following:
- `2020: happy: 5%, relaxed: 24%, neutral: 42%, sad: 7%, anxious: 19%, upset: 2%`
- `2021: happy: 4%, relaxed: 28%, neutral: 43%, sad: 7%, anxious: 28%, upset: 1%`.

![](/plots/annual_bar_chart.png)

##### time series

Below is a time series of mood sentiment over the two years, conveying a metric of positive vs. negative mood over time. Sentiment takes a value in range `[-2.0, 2.0]` inclusive. I take the rolling mean of sentiment value over 7-day and 30-day windows.

![](/plots/annual_time_series.png)

Mood over the two years is relatively volatile, unsurprising for a time as turbulent as this one. The mean sentiment value is ` -0.1166`, with a standard deviation of `1.0479` for range `[-2.0, 2.0]`.

##### weekly trends [2020 only, 2021 pending]
Positive moods like happy or relaxed are most common on weekends, with the highest frequency of an anxious mood during the week.
![](/plots/weekly_mood_counts.png)

If we collapse this further, and group moods by ***positive*** (happy, relaxed) and ***negative*** (sad, anxious, upset), ignoring neutral as the baseline, we see can see the following distribution:

Relative to the overall mean of `0.0127`, sentiment averages by day of the week are the following: `sunday: 0.13, monday: -0.06, tuesday: -0.17, wednesday: -0.1471, thursday: -0.1667, friday: 0.1373, saturday: 0.19`.
