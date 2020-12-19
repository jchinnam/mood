# mood

Analytics out of my own mood data from 2020. See analysis [here](/analysis.md).

### Setup
```bash
$ git clone <repo>
$ cd mood/
```

### Files
- `mood_categories.txt` for details on the 6 moods
- `mood.csv` is a csv with 12 cols (months) where elements are `{happy, relaxed, neutral, sad, anxious, upset, x}` to represent the 6 moods, with `x` for trailing days (example: 2 at the end of feb)

### Analytics
- Mood frequency & percentages for the year
- Monthly and seasonal frequency tables
- Time series (via sentiment assignment)
  - with 7-day rolling mean
  - with 30-day rolling mean
