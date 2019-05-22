
import requests
import difflib
import time
from lxml import html
from bs4 import BeautifulSoup
from notify_run import Notify


USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

LOGIN_URL = "https://portail.polytech-lille.fr/login/"
URL = "http://appliportal.polytech-lille.fr/mypolytech/mesNotes.php"

def send_mail():
	#TODO
    pass


def main():
    session_requests = requests.session()

    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)

    # Create payload
    payload = {
        "login": USERNAME, 
        "password": PASSWORD, 
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    tree = html.fromstring(result.content)
    bucket_names = tree.xpath("//td")

    soup = BeautifulSoup(result.content, 'html.parser')

    pair = True

    lines1 = []
    f_notes = open("notes.txt","r+")
    lines2 = f_notes.readlines()

    #check for emptyness (first run)
    if len(lines2) == 0 :
    	for td in soup.find_all('td'):
	    	if pair:
	    		f_notes.write(td.contents[0] + " : ")
	    	else :
	    		f_notes.write(td.contents[0] +'\n')
	    	pair = not(pair)

    s = ''    	
    for td in soup.find_all('td'):
    	if pair:
    		s += str(td.contents[0]) + " : " 
    	else :
    		s += td.contents[0] + '\n'
    		lines1.append(s)
    		s = ''
    	pair = not(pair)

    #could also use set intersection between lines 1 and 2 
    # ex : value = { k : second_dict[k] for k in set(second_dict) - set(first_dict) }

    diff = difflib.unified_diff(lines2, lines1, fromfile='file1', tofile='file2', lineterm='', n=0)
    lines = list(diff)[2:]
    added = [line[1:] for line in lines if line[0] == '+']

    if len(added) != 0 :
    	f_notes = open("notes.txt","a")
    	notify = Notify()
    	for line in added:
    		f_notes.write(str(line))
    		notify.send(line.split(':')[0]) 
    	f_notes.close()

    f_notes.close()



if __name__ == '__main__':
    while True :
        main()
        time.sleep(60)