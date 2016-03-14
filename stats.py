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

#dff.to_csv('results.csv', index = False )

df = pd.read_csv('results.csv')

# Finally, let's have some fun!
df['TN'] = df['Pld']/2. + 1 # Number of teams
df['Wn'] = df['W']/df['TN']
df['Dn'] = df['D']/df['TN']
df['Ln'] = df['L']/df['TN']
df['GFn'] = df['GF']/df['TN']
df['GAn'] = df['GA']/df['TN']
df['GDn'] = df['GD']/df['TN']
sfactor = 5


max_group = df.groupby(['year','league']).max().unstack().apply(pd.Series.interpolate)
ax = max_group['Pos'].plot(subplots=True,figsize=(6, 6), sharex=True, legend=None)
labs = max_group['GF'].columns.values

for i in [0,1,2,3]:
    ax[i].set_ylim(10,24)
    ax[i].set_ylabel('Teams')
    ax[i].set_title(labs[i])
    #ax[i].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()

#####################################

grouped = df.groupby(['year','league']).mean().unstack().apply(pd.Series.interpolate)

pd.rolling_mean(grouped['Wn'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Average number of victories divided by the number of teams')
plt.ylabel('')
plt.tight_layout()
plt.savefig('figures/Wn.png', dpi=300)

pd.rolling_mean(grouped['W'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Average number of victories')
plt.ylabel('')
plt.tight_layout()
plt.savefig('figures/W.png', dpi=300)

#####################################

pd.rolling_mean(grouped['Dn'], 5).plot(lw = 1.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Average drawn matches')
plt.ylabel('Normalized average of draws per year')

pd.rolling_mean(grouped['GFn'], 5).plot(lw = 1.5)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.title('Average Goals for')
plt.ylabel('Normalized average of GF per year')


grouped = df.groupby(['year','league']).max().unstack().apply(pd.Series.interpolate)

pd.rolling_mean(grouped['Wn'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Maximum number of victories divided by the number of teams')
plt.savefig('figures/M_Wn.png', dpi=300)

