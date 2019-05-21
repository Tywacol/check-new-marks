
import requests
from lxml import html
from bs4 import BeautifulSoup

USERNAME = "USERNAME"
PASSWORD = "PASSWORD"

LOGIN_URL = "https://portail.polytech-lille.fr/login/"
URL = "http://appliportal.polytech-lille.fr/mypolytech/mesNotes.php"

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
    print(result.content)
    tree = html.fromstring(result.content)
    print(tree)
    bucket_names = tree.xpath("//td")
    print()

    print(bucket_names)
    print()
    soup = BeautifulSoup(result.content, 'html.parser')

    print(soup.prettify())
    print()
    pair = True

    for td in soup.find_all('td'):
    	#if pair:
    	print(td.contents[0])


if __name__ == '__main__':
    main()