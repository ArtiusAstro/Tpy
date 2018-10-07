"""
2018/21/5

@author: astro

This script searches for a keyword and downloads the item, avoiding any annoying popup ads.
The script aims to create a search results url then parses the html to proceed to download.
"""

#import sys #if you would rather state search query in args than input()
import os #start client
import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup

def encodeQuery(q):

	return '+'.join(q.split())

def getSoup(link):

	from urllib.request import Request, urlopen

	request = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
	try:
		page = urlopen(request).read()
	except:
		print("invalid URL")
	return BeautifulSoup(page,"html.parser")

site = "https://duckingproxy.eu" #Choose a site here
postQueryText = "&page=0&orderby=99" #Text after the search keyword in url
preQueryText = "/s/?q=" #Text before the search keyword in url but after site

#rawData = ' '.join(sys.argv[1:])
rawData = (input(">>> "))
print(rawData)
q = encodeQuery(rawData) #Query
url = site+preQueryText+q+postQueryText

# Here a google search attempts to correct any spelling errors
print("Spell checker...")

goog = "https://www.google.com/search?q="+q

soup = getSoup(goog)
correction = ""
spell = soup.findAll("a",{"class":["spell"]})

for sp in spell[:1]:
	correction=sp.text

if(len(correction)>0):
	print("I got a suggestion: %s"%(correction))
	q = encodeQuery(correction)
	url = site+preQueryText+q+postQueryText

else:
	print("%s looks OK"%(rawData))

print("Please wait as this may take some time...")

soup = getSoup(url)

#Adjust according to the class you seek
allLinks = soup.findAll("div", {"class":["detName"]})

links = []
numWanted = 10

for link in allLinks[:numWanted]:
	new_url=site+(link.find('a')['href'])
	links.append(new_url)

if(len(links)==0):
	print("No links found. Manual search.")
else:
	print("Please choose num from the following links, any other input will exit")
	i = 0
	for link in links:
		print("\n%d)  %s" % (i,link[40:]))
		i+=1
	try:
		soup = getSoup(links[int(input("\n>>> "))])
		link = soup.find("div",{"class":["download"]}) #Check the class you seek
		magnet = (link.a['href'])
		print("File obtained, starting client.")
		os.startfile(magnet)
	except:
		print("Terminating")
