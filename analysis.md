# mood analysis
In 2020, I categorized my mood daily into 6 categories and set out to discover what I could learn about myself.

### Data
Each day was categorized into one of the following mood sets:
1. **happy**: happy, positive
2. **relaxed**: relaxed, content
3. **neutral**: neutral, uneventful
4. **sad**: sad, lonely, depressed
5. **anxious**: stressed, anxious
6. **upset**: angry, frustrated, upset

### Results & Trends

##### Year Statistics

Below is a bar chart representation of the percentage of the year I spent in each mood. Logically, neutral is the clear majority, with individual percentages of the following: `happy: 5%, relaxed: 4%, neutral: 43%, sad: 7%, anxious: 19%, upset: 3%`.

![](/plots/year_percentages.png)

##### Sentiment Values
Taking into account personal understanding/weight of the mood categories, I designed a mapping to quantify the moods with the following sentiment/emotional values:
`{"happy": 2, "relaxed": 1, "neutral": 0, "anxious": -1, "sad": -1.5, "upset": -2}
`

##### Time Series

Below is a time series of mood sentiment over the entire year, conveying a metric of positive vs. negative mood over time. Sentiment takes a value in range `[-2.0, 2.0]` inclusive. I take the rolling mean of sentiment value over 7-day and 30-day windows.

![](/plots/time_series_rolling_means.png)

Mood over the year is relatively volatile, unsurprising for a year as turbulent as 2020. The mean sentiment value is `0.0127`, with a standard deviation of `0.9402` for range `[-2.0, 2.0]`.

A few observations:
- visible dip in average sentiment from March to June, coinciding with the onset of the COVID-19 pandemic
- subsequent rise in average sentiment from June to August, simultaneous with the summer months (a relief from previously mostly-indoor quarantine)
- another drop in average mood in the early fall as the pandemic rides in a second wave and daylight becomes scarce
- general upward trend of sentiment in the second half of the year as pandemic-inflicted stress subsides
