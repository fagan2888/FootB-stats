from bs4 import BeautifulSoup
import urllib2
import pandas as pd
import numpy as np
import httplib2
import re

# Define years

def years(start, end):
	if end < 2000:
		output = ['{}-{}'.format(i,i+1-1900) for i in range(start,end)]
	else:
		y1 = ['{}-{}'.format(i,i+1-1900) for i in range(start,1999)]
		y2 = ['1999-2000']
		y3 = ['{}-{:02d}'.format(i,i+1-2000) for i in range(2000,end)]
		output = y1 + y2 + y3
	return output

header = {'User-Agent': 'Mozilla/5.0'} # Needed to prevent 403 error on Wikipedia

def league_name(wpage):
	a = wpage.split('_')[1:][0]
	b = wpage.split('_')[1:][1]
	return a + ' ' + b

def FootB(wpage, league_name):

	req = urllib2.Request(wpage, headers = header)
	page = urllib2.urlopen(req)
	soup = BeautifulSoup(page, 'html5lib')

	all_tables = soup.find_all('table')
	theone = [u'W', u'D']
	
	for table in all_tables:
		all_rows = table.find_all('tr')
		lencols = len(all_rows[0].find_all('th')) 
		cols = np.array([all_rows[0].find_all('th')[i].get_text().encode('ascii', 'ignore') for i in range(0, lencols)])
		
		if (theone[0] in cols) & (theone[1] in cols):

			if len(cols[1]) > 10:
				cols[1] = cols[1].strip('\n\n\nv\nt\ne\n\n\n\n')
			cols[cols == 'Club'] = 'Team'	
			cols[cols == 'Played'] = 'Pld'
			cols[cols == 'Points'] = 'Pts'	
			cols[cols == 'Wins'] = 'W'	
			cols[cols == 'Draws'] = 'D'	
			cols[cols == 'Losses'] = 'L'	
			cols[cols == 'Goals for'] = 'GF'
			cols[cols == 'Goals against'] = 'GA'	
			cols[cols == 'F'] = 'GF'
			cols[cols == 'A'] = 'GA'	
			# Masks rows which are not related to Team information 
			rows = []
			for r in all_rows:
   				 if len(r) > 5:
   				 	rows.append(r)
			lenrows = len(rows)
			break

	year = wpage.split('/')[-1].split('_')[0]

	columns = ['Team', 'Pld', 'W', 'D', 'L', 'GF', 'GA', 'GD']
	# Create empty pandas dataframe
	df = pd.DataFrame(columns = columns, index = range(1, lenrows))

	# Fill the dataframe
	for i in range(1, lenrows):
		team = rows[i].find_all('td')
		df.Team.ix[i] = team[np.where(cols == 'Team')[0][0]].a.get_text().encode('ascii', 'ignore')
		df.Pld.ix[i] = team[np.where(cols == 'Pld')[0][0]].get_text().encode('ascii', 'ignore')
		
		for colnames in ['W', 'D', 'L', 'GF', 'GA']:
			mask = np.where(cols == colnames)[0]
			x0 = 0 
			if len(mask) > 1:
				for m in [0,1]: 
					x0 += int(team[mask[m]].get_text().encode('ascii', 'ignore'))
					df[colnames].ix[i] = x0
			else: 
				df[colnames].ix[i] = int(team[mask[0]].get_text().encode('ascii', 'ignore'))

			mask = np.where(cols == 'GD')[0]
	
		if 'GD' in cols:
			# strip() is needed to strip whitespaces in some seasons
			df['GD'].ix[i] = team[mask[0]].get_text().encode('ascii', 'ignore').strip() 
	
	# Add year and league name 
	df['year'] = pd.Period(year.split('-')[0]) + 1
	if league_name == 'Football League':
		league_name = 'Premier League'

	if league_name == 'French Division':
		league_name = 'Ligue 1'

	df['league'] = league_name

	# Replace Unicode minus sign with '-'
	if ' ' in df.GD.values.any():
		df.GD = df.GD.map(lambda x: re.sub('[\s+]', '', x))
	mask = df.GD.apply(lambda x: ('+' in x) | ('-' in x))
	df.GD[~mask] = '-' + df.GD[~mask]
	
	# Add ladder position from the index
	df['Pos'] = df.index

	df['Pld'] = df.Pld.map(lambda x: x[0:2])
	# Transform to integers
	coltmp = ['Pos', 'Pld', 'W', 'D', 'L', 'GF', 'GA','GD']
	df[coltmp] = df[coltmp].astype(float).astype(int)

	# Redefine Pts using Italian standard scoring system
	df['Pts'] = df.W * 3. + df.D

	return df
