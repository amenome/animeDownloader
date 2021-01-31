import os
from os import listdir
from os.path import isfile, join
from os import walk

import time
import requests
import urllib.request

try:
    import readline
except ImportError:
    print("Module readline not available.")
else:
    import rlcompleter
    readline.parse_and_bind("tab: complete")

from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from pyvirtualdisplay import Display

#====================================================================================================#

display = Display(visible=0, size=(800, 800))  
display.start()

options = Options()
options.add_argument("--headless")
options.add_argument('--no-sandbox')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("disable-infobars")
options.add_argument("start-maximized")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

#====================================================================================================#

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# os.system('cls' if os.name == 'nt' else 'clear')	
print ("Headless Chrome Initialized")

params = {'behavior': 'allow', 'downloadPath': r''}
driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

download_dir = '/Downloads'

#====================================================================================================#

def enable_download(driver):
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd':'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_dir}}
    driver.execute("send_command", params)

def setting_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('--no-sandbox')
    return chrome_options;
def isFileDownloaded():
    file_path = download_dir+"\python_samples-master.zip"
    while not os.path.exists(file_path):
        time.sleep(1)
    if os.path.isfile(file_path):
        print("File Downloaded successfully..")

#=======================================================================#

myAnimeDir = "/home/myAnime.txt"
myAnime = open(myAnimeDir, "a+")
print(myAnime.read())

#=======================================================================#

def download(link, entire, first, last, title, season, loc, subOrDub):
	# print('Link: ' + link)
	# print('Entire: ' + entire)
	# print('First: ' + first)
	# print('Last: ' + last)
	# print('Title: ' + title)
	# print('Season: ' + season)
	# print('loc: ' + loc)
	# print('Sub or Dub: ' + subOrDub)
	#=======================================================================#

	with open(myAnimeDir) as f:
		if link not in f.read():
			myAnime.write(title + ', ' + link + ', ' + season + ', ' + subOrDub + '\n')
		print(myAnime.read())

	#=======================================================================#

	if(subOrDub == 's'):
		title += ' (Sub)'
		# print("ADDING SUB TO TITLE")
	if(subOrDub == 'd'):
		title += ' (Dub)'
		# print("ADDING DUB TO TITLE")

	#=======================================================================#

	loc = loc + "/" + title
	loc = Path(loc)
	if not os.path.exists(loc):
		os.mkdir(loc)

	numlessLink = link[:-1]

	#=======================================================================#

	if(entire == 'y'):
		first = 1
		driver.get(link);
		elem = driver.find_element_by_xpath("//a[contains(text(), '0-')]")
		tempString = str(elem.get_attribute('innerHTML')).split("-",1)[1]
		last = int(tempString)

	#=======================================================================#
	# ADD FUNCTIONALITY FOR EPISODES THAT ARE WEIRD FORMATS LIKE 24.5 OR 24.9
	print('Downloading Episodes ' + str(first) + '-' + str(last) + ' of ' + title)
	for i in range(int(first), int(last) + 1):
		# os.system('cls' if os.name == 'nt' else 'clear')
		print("\n===============================================================\n")

		if(i < 10):
			if(int(season) < 10):
				fileName = title + ' ' + 'S0' + season + 'E' + '0' + str(i) + '.mp4'
			else:
				fileName = title + ' ' + 'S' + season + 'E' + '0' + str(i) + '.mp4'
		else:
			if(int(season) < 10):
				fileName = title + ' ' + 'S0' + season + 'E' + str(i) + '.mp4'
			else:
				fileName = title + ' ' + 'S' + season + 'E' + str(i) + '.mp4'

		fileToOpen = loc / fileName

		if(not os.path.exists(fileToOpen)):		# Checks to see if the file is already downloaded.
			link = numlessLink + str(i)
			driver.get(link);

			elems = driver.find_elements_by_xpath("//a[@href]")
			for elem in elems:
				if(elem.get_attribute("href").find('gogo-play') != -1):
					print('Found Season ' + season + " Episode " + str(i) + " of " + title + " on gogoanime.so")
					link = elem.get_attribute("href")

			driver.get(link)

			elems = driver.find_elements_by_xpath("//a[@href]")
			for elem in elems:
				if(elem.get_attribute("href").find('gogo-play') == -1):
					print('Found download link for Season ' + season + " Episode " + str(i) + " of " + title)
					link = elem.get_attribute("href")
					file = elem
					break	# default to picking first one

			urllib.request.urlretrieve(link, fileToOpen)
		else:
			print(fileName + ' was already downloaded.')
		print("\n===============================================================\n")
#=======================================================================#

shouldQuit = False
while(not shouldQuit):
	shouldUpdate = input('Update your anime [1] \nAdd a new anime [2]\nQuit [3]\nInput: ')

	if(shouldUpdate == '1'):
		with open(myAnimeDir) as file:
			for myline in file:
				array = myline.split(', ')
				title = array[0]
				link = array[1]
				season = array[2]
				subOrDub = array[3].rstrip()
				entire = 'y'
				loc = '/home'
				download(link, entire, '-1', '-1', title, season, loc, subOrDub)
				# os.system('cls' if os.name == 'nt' else 'clear')
	if(shouldUpdate == '2'):
		link = input('Enter the gogoanime.so URL of the first episode: ')
		entire = input('Download entire anime (y/n): ')
		if(entire == 'n'):
			first = input('Enter the first episode number you want to download: ')
			last = input('Enter the last episode number you want to download: ')
		title = input('Enter the title you want: ')
		season = input('Enter the season of this anime: ')
		loc = '/home'
		subOrDub = input('Subbed or Dubbed (s/d): ')
		download(link, entire, first, last, title, season, loc, subOrDub)
	if(shouldUpdate == '3'):
		shouldQuit = True

driver.quit()
print("Headless Chrome Instance Ended.")

#====================================================================================================#