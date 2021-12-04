# mood

analytics out of my own mood data across 2020-2021. See analysis [here](/analysis.md).

### usage
```bash
$ git clone <repo>
$ cd mood/
$ python ./mood.py # after populating mood.csv
```

### files
- `moods_info.json`: details on the 6 moods
- `mood.csv`: raw mood data, columns represent months and each element is a character in the set `{a, b, c, d, e, f, x}` to represent the 6 moods (see `moods_info.json` for which mood corresponds to which character), with `x` for trailing days (example: 2 at the end of feb)

### analytics
- total mood frequencies & percentages
- monthly frequency tables
- annual mood frequency bar plots
- time series (via sentiment assignment) with 7 and 30 day rolling means
