import matplotlib.pyplot as plt
from FootB import *
matplotlib.style.use('ggplot')

list_La_Liga = ['https://en.wikipedia.org/wiki/{}_La_Liga'.format(y) for y in years(1930,2014)]

list_Bunder = ['https://en.wikipedia.org/wiki/{}_Bundesliga'.format(y) for y in years(1963,2014)]


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
			 list_Premier_League + list_French_Division + list_Ligue_1 + list_Bunder)

# Construct a dataframe with the data

df = pd.DataFrame()

for page in final_list:
	h = httplib2.Http()
	resp = h.request(page, 'HEAD')
	if int(resp[0]['status']) < 400:	
		print page
		tmp = FootB(page, league_name(page))
		df = df.append(tmp, ignore_index = True)

df.to_csv('results.csv', index = False )

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

for i in [0,1,2,3,4]:
    ax[i].set_ylim(10,24)
    ax[i].set_ylabel('Teams')
    ax[i].set_title(labs[i])
    #ax[i].legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)
plt.tight_layout()
plt.savefig('figures/pos.png', dpi=300)

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

pd.rolling_mean(grouped['GFn'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Average number of victories')
plt.ylabel('')
plt.tight_layout()
plt.savefig('figures/W.png', dpi=300)

#####################################
# Number of draws
pd.rolling_mean(grouped['Dn'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Average number of draws divided by the number of teams')
plt.ylabel('')
plt.savefig('figures/Dn.png', dpi=300)

#####################################
# Number of GF

pd.rolling_mean(grouped['GF'], 5).plot(lw = 1.5)
plt.legend(loc='left')
plt.title('Average number of goals-for divided by the number of teams')
plt.savefig('figures/GFn.png', dpi=300)

#####################################
# Maximum Wn
grouped = df.groupby(['year','league']).max().unstack().apply(pd.Series.interpolate)
pd.rolling_mean(grouped['Wn'], 5).plot(lw = 1.5)

plt.legend(loc='left')
plt.title('Maximum number of victories divided by the number of teams')
plt.savefig('figures/M_Wn.png', dpi=300)

#####################################
plt.figure(figsize=(6,5))

grouped = df.groupby('league')
cm = plt.cm.get_cmap('jet')
grouped.plot(x='W', y='D', c = 'GF', s= 60, kind='scatter', cmap=cm, subplots = True)

import seaborn as sns

fig, axes = plt.subplots(nrows=2, ncols=3)
for ax,j in zip(axes.flat, ['Premier League', 'Serie A', 'La Liga', 'Ligue 1', 'Bundesliga']):
	tmp = grouped.get_group(j)
	ax.set_title(j)
	im = sns.kdeplot(tmp.W, tmp.D, gridsize=40, cmap=cm, ax = ax)
	ax.scatter(tmp.W, tmp.D, s=5, c='black', marker = 'x')
	ax.set_xlim(0,35)
	ax.set_ylim(0,30)
	ax.set_xlabel('Won')
	ax.set_ylabel('Drawn')

plt.suptitle('All time Won vs Drawn',size=15)
plt.savefig('figures/W_vs_D.png', dpi=300)

