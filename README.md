# Fantasy-Baseball-Stuff

`query` assumes projection CSV format from [Auction Calculator via fangraphs]('http://www.fangraphs.com/auctiontool.aspx').

`query.py` - Useful for quickly querying CSV data.

```python
# top 10 players priced at $30 or below
query(max_val=30)

# top 10 at shortstop
query_by_pos('SS')

# Mike Trout
query_by_name('Trout')
```

`scrape.py` - Scrapes ESPN for most picked up players.
