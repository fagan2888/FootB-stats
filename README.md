# FootB-stats
A python web-scraping code to get football championship statistics.

The code scraps data from the wikipedia pages of European tournaments (Serie A, Premier League, La Liga, Ligue 1, Bundesliga) and gets some interesting statistics out of it. 

 - `FootB.py` contains the functions necessary for the web-scraping bit;

 - `stats.py` uses the functions in `FootB.py` to create the stacked table (pandas dataframe) with the data;

 - This [python notebook ](notebook/FootB.ipynb) contains a tutorial and some usage examples.  

The code relies on BeautifulSoup, Pandas, numpy and seaborn (for some plots only).

<img src="https://github.com/vincepota/FootB-stats/blob/master/notebook/W.png" width="600">

