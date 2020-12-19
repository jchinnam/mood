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

### Methodology

##### Sentiment Values
Taking into account personal understanding/weight of the mood categories, I designed a mapping to quantify the moods with the following sentiment/emotional values:
`{"happy": 2, "relaxed": 1, "neutral": 0, "sad": -1.5, "anxious": -1, "upset": -2}
`

### Trends

##### Time Series

Below is a time series of mood sentiment over the entire year, conveying a metric of positive vs. negative mood over time. Sentiment takes a value in range `[-2.0, 2.0]` inclusive. I take the rolling mean of sentiment value over 7-day and 30-day windows.

![](/plots/time_series_rolling_means.png)

Mood over the year is relatively volatile, unsurprising for a year as turbulent as 2020. A few observations:
- a visible dip in average sentiment from March to June, coinciding with the onset of the COVID-19 pandemic
- subsequent rise in average sentiment from June to August, simultaneous with the summer months (a relief from previously mostly-indoor quarantine)
- another drop in average mood in the early fall as the pandemic rides in a second wave and daylight becomes scarce
- general upward trend of sentiment in the second half of the year as volatility subsides
