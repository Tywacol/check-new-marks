import requests
import difflib
import time
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
from notify_run import Notify

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

LOGIN_URL = "https://portail.polytech-lille.fr/login/"
URL = "http://appliportal.polytech-lille.fr/mypolytech/mesNotes.php"

def send_mail():
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

    added = list(set(lines1) - set(lines2))

    if len(added) != 0 :
        f_notes = open("notes.txt","a")
        notify = Notify()
        for line in added:
                f_notes.write(str(line))
                notify.send('Note : '+line.split(':')[0]) 
        f_notes.close()

    f_notes.close()

if __name__ == '__main__':
    while True :
        main()

        time.sleep(60)