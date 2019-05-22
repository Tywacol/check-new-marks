import requests
import difflib
import time
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
from notify_run import Notify



#Tres mauvais apparament
#from importlib import reload
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')


USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

LOGIN_URL = "https://portail.polytech-lille.fr/login/"
URL = "http://appliportal.polytech-lille.fr/mypolytech/mesNotes.php"

def send_mail():
        pass

def main():
    session_requests = requests.session()

    # Get login csrf token
    result = session_requests.get(LOGIN_URL)
    tree = html.fromstring(result.text)
    #authenticity_token = list(set(tree.xpath("//input[@name='csrfmiddlewaretoken']/@value")))[0]

    # Create payload
    payload = {
        "login": USERNAME, 
        "password": PASSWORD, 
        #"csrfmiddlewaretoken": authenticity_token
    }

    # Perform login
    result = session_requests.post(LOGIN_URL, data = payload, headers = dict(referer = LOGIN_URL))

    # Scrape url
    result = session_requests.get(URL, headers = dict(referer = URL))
    #print("Result content : ")
    #print(result.content)
    tree = html.fromstring(result.content)
    #print("tree : ")
    #print(tree)
    bucket_names = tree.xpath("//td")
    #print("bucket_names : ")

    #print(bucket_names)
    #print("soup.prettify()")
    soup = BeautifulSoup(result.content, 'html.parser')

    #print(soup.prettify())
    #print()
    pair = True

    lines1 = []

    f_notes = open("notes.txt","r+")
    lines2 = f_notes.readlines()

  
    #print("len lines 2 = " + str(len(lines2)))
    #print()
    #print("lines2 = " + str(lines1))

    #check for emptyness (first run)
    if len(lines2) == 0 :
        #print("len == 0")
        #print("lines2 = " + str(lines1))
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
                 #print(td.contents[0] + " : ", end='')
                #lines1.append(td.contents[0])
        else :
                #print(td.contents[0])
                s += td.contents[0] + '\n'
                lines1.append(s)
                s = ''
        pair = not(pair)

    #could also use set intersection between lines 1 and 2 
    # ex : value = { k : second_dict[k] for k in set(second_dict) - set(first_dict) }

    #diff = difflib.unified_diff(lines2, lines1, fromfile='file1', tofile='file2', lineterm='', n=0)
    #lines = list(diff)[2:]
    #added = [line[1:] for line in lines if line[0] == '+']

    added = list(set(lines1) - set(lines2))
    #print("added_set = " +str(added_set))

    #removed = [line[1:] for line in lines if line[0] == '-']
    #print('additions:')
    print("lines1 : " +str(lines1))
    print("lines2 : " +str(lines1))

    print("added  = " + str(added))

    if len(added) != 0 :
        f_notes = open("notes.txt","a")
        notify = Notify()
        for line in added:
                f_notes.write(str(line))
                print("line = " + str(line))
                notify.send('Note : '+line.split(':')[0]) 
        f_notes.close()

    #print("lines1 = " + str(lines1))
    #print("lines2 = " + str(lines2))

    f_notes.close()



if __name__ == '__main__':
    i = 1
    while True :
        print("Iteration : " + str(i))
        i += 1
        print(datetime.now())
        main()

        time.sleep(60)