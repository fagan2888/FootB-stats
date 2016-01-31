from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import matplotlib.pyplot as plt
from tqdm import *

wpages = ['https://it.wikipedia.org/wiki/Serie_A_{}-{}'.format(i,i + 1) for i in range(1929,2015)]
wpages.remove('https://it.wikipedia.org/wiki/Serie_A_1943-1944')
wpages.remove('https://it.wikipedia.org/wiki/Serie_A_1944-1945')
wpages.remove('https://it.wikipedia.org/wiki/Serie_A_1945-1946')

header = {'User-Agent': 'Mozilla/5.0'} # Needed to prevent 403 error on Wikipedia

def findpar(s):
	alist = list(s)
	if '(' in alist:
		out = s[s.find("(")+1:s.find(")")]
	else:
		out = s
	return out

def serieA(wpages):
	req = urllib2.Request(wpages, headers=header)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page, 'html5lib')
	
	all_tables = soup.find_all("table", { "class" : "wikitable sortable" })
	theone = [u'Pos.',u'Squadra', u'Pt', u'G']
	
	for j in range(0,len(all_tables)):
		rows = all_tables[j].find_all("tr")
		lencols = len(rows[0].find_all("th")) 
		if lencols > 5:
			columns = [rows[0].find_all("th")[i].get_text().encode('ascii', 'ignore') for i in range(1, lencols)]
			lencols = len(columns)
			if columns[:4] == theone:
				table = all_tables[j]
				lenrows = len(rows) - 1
				break
	
	columns[0] = 'Pos' 

	if columns[5] == 'P': 
		columns[5] = 'N'
	
	if columns[6] == 'S': 
		columns[6] = 'P'
	
	df = pd.DataFrame(columns = columns, index = range(1, lenrows + 1))

	year = wpages.split('_')[-1]
	df['year'] = year
	
	for i in range(1, lenrows + 1):
		team = rows[i].find_all("td")
		for j in range(0, lencols):
			df[df.columns[j]].ix[i] = team[j + 1].get_text().encode('ascii', 'ignore')
	
	# Extract numbers between parenthesis 
	df['Pt'] = df.Pt.apply(lambda x: findpar(x))
	# Transform to integers
	df[['Pos','Pt', 'G', 'V', 'N', 'P', 'GF', 'GS']] = df[['Pos','Pt', 'G', 'V', 'N', 'P', 'GF', 'GS']].astype(float).astype(int)

	# Remove first two unicode characters
	# Remove [n] from some team names
	df['Squadra'] = df['Squadra'].apply(lambda x: x.encode('ascii', 'ignore').split('[')[0]) 

	mask = df['Squadra'] == 'Genova 1893'
	df.loc[mask, 'Squadra'] = 'Genoa'

	mask = df['Squadra'] == 'L.R. Vicenza'
	df.loc[mask, 'Squadra'] = 'Vicenza'

	mask = ((df['Squadra'] == 'Ambrosiana') | (df['Squadra'] == 'Ambrosiana-Inter'))
	df.loc[mask, 'Squadra'] = 'Inter'

	df.Pt = df.V * 3. + df.N 

	if 'QR' in columns:
		df.drop('QR', axis=1, inplace=True)
	if 'DR' in columns:
		df.drop('DR', axis=1, inplace=True)

	df['Squadra'] = df['Squadra'].apply(lambda x: x.split()[0]) 

	return df

if __name__ == '__main__':

dff = pd.DataFrame()
for page in tqdm(wpages):
	dff = dff.append(serieA(page), ignore_index = True)


grouped = dff.groupby('Squadra')

