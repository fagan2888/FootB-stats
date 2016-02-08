from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import *

#Define the years
y1 = ['{}-{}'.format(i,i+1-1900) for i in range(1929,1999)]
y2 = ['1999-2000']
y3 = ['{}-{:02d}'.format(i,i+1-2000) for i in range(2000,2015)]
years = np.concatenate([y1,y2,y3])

p1 = ['https://en.wikipedia.org/wiki/{}_Serie_A'.format(y) for y in years]
p1.remove('https://en.wikipedia.org/wiki/1943-44_Serie_A')
p1.remove('https://en.wikipedia.org/wiki/1944-45_Serie_A')
p1.remove('https://en.wikipedia.org/wiki/1945-46_Serie_A')
p1.remove('https://en.wikipedia.org/wiki/2005-06_Serie_A')  #Removed because of Calciopoli scandal

p2 = ['https://en.wikipedia.org/wiki/{}_La_Liga'.format(y) for y in years]
p2.remove('https://en.wikipedia.org/wiki/1943-44_Serie_A')

header = {'User-Agent': 'Mozilla/5.0'} # Needed to prevent 403 error on Wikipedia

def FootB(wpages):
	#wpages = 'https://en.wikipedia.org/wiki/2014-15_Serie_A'
	req = urllib2.Request(wpages, headers=header)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page, 'html5lib')
	
	all_tables = soup.find_all("table")
	theone = [u'W', u'Pld']
	
	for j in range(0,len(all_tables)):
		rows = all_tables[j].find_all("tr")
		lencols = len(rows[0].find_all("th")) 
		if lencols > 5:
			columns = [rows[0].find_all("th")[i].get_text().encode('ascii', 'ignore') for i in range(0, lencols)]
			lencols = len(columns)
			if (theone[0] in columns) & (theone[1] in columns):
				lenrows = len(rows) - 1
				break
	
	newcolumns = columns[1:10]
	if '\n' in newcolumns[0]:
		newcolumns[0] = 'Team'

	lencols = len(newcolumns)
	df = pd.DataFrame(columns = newcolumns, index = range(1, lenrows))

	year = wpages.split('/')[-1].split('_')[0]
	df['year'] = year
	
	for i in range(1, lenrows):
		team = rows[i].find_all('td')
		print team[0]
		for j in range(0, lencols):
			if j == 0:
				df[df.columns[j]].ix[i] = team[j + 1].a.get_text().encode('ascii', 'ignore')
			elif j == 8:
				df[df.columns[j]].ix[i] = team[j + 1].b.get_text().encode('ascii', 'ignore')
			else:
				df[df.columns[j]].ix[i] = team[j + 1].get_text().encode('ascii', 'ignore')

	mask = df.GD.apply(lambda x: ('+' in x) | ('-' in x) )
	df.GD[~mask] = '-' + df.GD[~mask]
	
	df['Pos'] = df.index
	
	# Transform to integers
	coltmp = ['Pos', 'Pld', 'W', 'D', 'L', 'GF', 'GA','GD','Pts']
	df[coltmp] = df[coltmp].astype(float).astype(int)
	df.Pts = df.W * 3. + df.D

	#mask = df['Squadra'] == 'Genova 1893'
	#df.loc[mask, 'Squadra'] = 'Genoa'

	#mask = df['Squadra'] == 'L.R. Vicenza'
	#df.loc[mask, 'Squadra'] = 'Vicenza'

	#mask = ((df['Squadra'] == 'Ambrosiana') | (df['Squadra'] == 'Ambrosiana-Inter'))
	#df.loc[mask, 'Squadra'] = 'Inter'

	return df

if __name__ == '__main__':

dff = pd.DataFrame()
for page in tqdm(p1[:-1]):
	print page
	dff = dff.append(FootB(page), ignore_index = True)

grouped = dff.groupby('Team')

