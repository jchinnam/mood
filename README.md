# mood

Analytics out of my own mood data from 2020.

### Setup
```bash
git clone <repo>
cd mood/
```

### Data
In 2020, I categorized my mood daily to the following 6 categories:
1. happy, positive
2. relaxed, content
3. neutral, uneventful
4. sad, lonely, depressed
5. stressed, anxious
6. angry, frustrated, upset

### Files
- `mood_categories.txt` for details on the 6 moods
- `mood.csv` is a csv with 12 cols (months) where elements are `{happy, relaxed, neutral, sad, anxious, upset, x}` to represent the 6 moods, with `x` for trailing days (example: 2 at the end of feb)

### Analytics
- Mood frequency & percentages for the year
- Monthly frequency tables
