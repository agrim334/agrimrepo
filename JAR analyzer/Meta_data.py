from bs4 import BeautifulSoup
import lxml
import requests
import time
import random
import openpyxl
#import xlsxwriter

workbook = openpyxl.load_workbook("Category_info.xlsx") 
wb2 = openpyxl.Workbook()
# credits for user agent rotation method to https://www.scrapehero.com/how-to-fake-and-rotate-user-agents-using-python-3/
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
sheet_obj = workbook.active 
sheet_obj2 = wb2.active
#workbook2 = xlsxwriter.Workbook('Meta_data.xlsx')
#worksheet1 = workbook2.add_worksheet()
row = 1

for j in range(1,151):
	URL = sheet_obj.cell(row = j, column = 3) 
	for i in range(1,11):    
		time.sleep(2)                                          #add delay to request
		url = URL.value + '?p='
		url = url + str(i)
		user_agent = random.choice(user_agent_list)
		page = requests.get(url,headers = {'User-Agent': user_agent})
		
		soup = BeautifulSoup(page.content,'lxml')           #parsing the html doc
		lib_url = soup.select('body > div[id = "page"] > div[id = "maincontent"] > div[class = "im"] > a[href ^= "/artifact/"]')  #structure of the website determined the tags to be used
		
		for temp in lib_url:
			new_url = "https://mvnrepository.com/"+temp['href']
			user_agent = random.choice(user_agent_list)
			time.sleep(2)                                          #add delay to request
			newpage = requests.get(new_url,headers = {'User-Agent': user_agent})
			newsoup = BeautifulSoup(newpage.content,'lxml')
			lib_name = newsoup.select('body > div[id = "page"] > div[id = "maincontent"] > div[class = "im"] > div[class = "im-header"] > h2[class = "im-title"] > a[href]')
			metainfo_value = newsoup.select('body > div[id = "page"] > div[id = "maincontent"] > table[class = "grid"] > tr > td')  #structure of the website determined the tags to be used
			n=0
			col = 2
			for val in metainfo_value:
				cell = sheet_obj2.cell(row=row,column=col)
				if col == 4:
					temp = val.text
					cell.value = temp
				elif col == 5:
					try:
						numval = val.text.split()[:-1]
						numval = int(numval[0].replace(',',''))
						cell.value = numval
					except:
						cell.value = ''
				else:
					cell.value = val.text
				col = col + 1
				print(cell.value)
				print(col)
				wb2.save("Meta_data.xlsx")
				if col == 6:
					cell = sheet_obj2.cell(row=row,column=1)
					cell.value = lib_name[n].text
					n = n + 1
					col = 2
					row = row + 1
wb2.close()
workbook.close()