from bs4 import BeautifulSoup
import lxml
import requests
import csv
import time
import random
import xlsxwriter	#can replace this with openpyxl

category_dict = {}				#set for storage of categories

# credit for user agent rotation method to https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
user_agent_list = [
   #Chrome
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
	'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
	#Firefox
	'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
	'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
	'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)',
	'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)',
	'Mozilla/5.0 (Windows NT 6.1; Win64; x64; Trident/7.0; rv:11.0) like Gecko',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)',
	'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
	'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)'
]

for i in range(1,16):								#the website had 15 pages for total categories. may need to update this to handle changes in website
	
	time.sleep(2)											#add delay to request

	URL = "https://mvnrepository.com/open-source?p="+str(i)
	
	user_agent = random.choice(user_agent_list)
	
	page = requests.get(URL,headers = {'User-Agent': user_agent})

	soup = BeautifulSoup(page.content,'lxml')			#parsing the html doc
														#structure of the website determined the tags to be used

	category = soup.select('body > div[id = "page"] > div[id = "maincontent"] > div > h4')		#this obtains the category name alongwith library count in form of a list

	category_url = soup.select('body > div[id = "page"] > div[id = "maincontent"] > div > h4 > a[href]')	#this obtains the url for main page of each category in form of a list

	for (cat,url) in zip(category,category_url): 
		category_dict[cat.text]="https://mvnrepository.com/"+url['href']			#cat.text contains category+library count string which is the key and value is the url for it

workbook = xlsxwriter.Workbook('Path to xlsx file')		#create new workbook
worksheet1 = workbook.add_worksheet() 
row = 0
col = 0

for k,v in category_dict.items():		#obtaining values from the category set
	
	val = k.split()[-1]						#splitting the category name and library count
	val = int(val[1:-1])					#this gives the library count in integer form 
	cat = ', '.join(k.split()[:-1])
	cat = cat.replace(",","")				#category name cleaned up 
	worksheet1.write(row,col,cat)
	worksheet1.write(row,col+1,val)			#writing category name, count and url to xlsx file
	worksheet1.write(row,col+2,v)
	row += 1

workbook.close()					#storing category info with urls in a xlsx file
