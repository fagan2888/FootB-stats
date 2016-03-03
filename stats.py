import matplotlib.pyplot as plt
from FootB import *
matplotlib.style.use('ggplot')

list_La_Liga = ['https://en.wikipedia.org/wiki/{}_La_Liga'.format(y) for y in years(1930,2014)]

list_Serie_A = ['https://en.wikipedia.org/wiki/{}_Serie_A'.format(y) for y in years(1930,2014)]
# Removed because of Calciopoli scandal
list_Serie_A.remove('https://en.wikipedia.org/wiki/2005-06_Serie_A')  

list_Football_League = ['https://en.wikipedia.org/wiki/{}_Football_League'.format(y) for y in years(1926,1992)]
list_Premier_League = ['https://en.wikipedia.org/wiki/{}_Premier_League'.format(y) for y in years(1992,2014)]
# Only three games were played in 1939-40 because of the war
list_Football_League.remove('https://en.wikipedia.org/wiki/1939-40_Football_League')  

list_French_Division = ['https://en.wikipedia.org/wiki/{}_French_Division_1'.format(y) for y in years(1933, 2001)]
list_Ligue_1 = ['https://en.wikipedia.org/wiki/{}_Ligue_1'.format(y) for y in years(2002, 2014)]
list_Ligue_1.remove('https://en.wikipedia.org/wiki/2003-04_Ligue_1')  

final_list = (list_La_Liga + list_Serie_A + list_Football_League + 
			 list_Premier_League + list_French_Division + list_Ligue_1)

# Construct a dataframe with the data

dff = pd.DataFrame()

for page in final_list:
	h = httplib2.Http()
	resp = h.request(page, 'HEAD')
	if int(resp[0]['status']) < 400:	
		print page
		df = FootB(page, league_name(page))
		dff = dff.append(df, ignore_index = True)

# Finally, let's have some fun!

dff['TN'] = dff['Pld']/2. + 1
dff['Wn'] = dff['W']/dff['TN']
dff['Dn'] = dff['D']/dff['TN']
dff['Ln'] = dff['L']/dff['TN']
dff['GFn'] = dff['GF']/dff['TN']
dff['GAn'] = dff['GA']/dff['TN']
dff['GDn'] = dff['GD']/dff['TN']

sfactor = 5
MAX = dff.groupby(['year','league']).max().unstack().apply(pd.Series.interpolate)
pd.rolling_mean(MAX['W'], 5).plot(lw = 1.5)

MEAN = dff.groupby(['year','league']).mean().unstack().apply(pd.Series.interpolate)
pd.rolling_mean(MEAN['Wn'], sfactor).plot(lw = 1.5)



gg.Pld.map(lambda x: np.where(len(x)>2))