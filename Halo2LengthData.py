import requests
import bs4
import re

# create lists and counters to store data, set first url and base
matches = []
lengths = []
minutes = []
seconds = []
purged_counter = 0
base = "http://halo.bungie.net"
url = "http://halo.bungie.net/stats/playerstatshalo2.aspx?player=nolls&ctl00_mainContent_bnetpgl_recentgamesChangePage="

# grab every link of every game on all 278 pages of game history, and append to matches list
for x in range(1, 278):
    link = requests.get(url + str(x))
    soup = bs4.BeautifulSoup(link.text)
    
    for game in soup.find_all('tr', {'class':'rgRow'}):
        matches.append(base + game.a['href'])
    for game in soup.find_all('tr', {'class':'rgAltRow'}):
        matches.append(base + game.a['href'])

# go through every link and find length of game, store data where its appropriate 
for i in range(len(matches)):
    link = requests.get(matches[i])
    soup = bs4.BeautifulSoup(link.text)
    length = soup.find_all('li', text=re.compile('Length'))
	
	# if game length isn't displayed
    if (length[0].string == u'Length: \xa0'):
        purged_counter += 1
        print "None"
		
	# strange outlier I found, had to bypass
    elif (length[0].string.encode('ascii', 'ignore') == "Length: 49710.06:27:22"):
		print "Error"	
		
    else:
        lengths.append(length[0].string.encode('ascii', 'ignore')[11:17])
    	print length[0].string.encode('ascii', 'ignore')[11:17]
        minutes.append(int(length[0].string.encode('ascii', 'ignore')[11:13]))
        seconds.append(int(length[0].string.encode('ascii', 'ignore')[14:17]))

print "Total purged games are: " + str(purged_counter)
print "Total Minutes are: " + str(sum(minutes))
print "Total Seconds are: " + str(sum(seconds))
