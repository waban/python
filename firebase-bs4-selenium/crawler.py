import re
import requests
from bs4 import BeautifulSoup

import selenium
from selenium import webdriver
import selenium.webdriver.chrome.service as service
from selenium.webdriver.chrome.options import Options

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use a service account
cred = credentials.Certificate("#locate-this-file/AccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

url = requests.get("http://livescore-spbo.com/")

data = {}
def triggerCrawl():
    options = Options()
    options.add_argument('--headless')

    chromeDriver = "#locate-this-file/chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=options,executable_path=chromeDriver)
        
    try:
        driver.get("http://livescore-spbo.com/")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        table1 = soup.select('table')[0]
        table2 = soup.select('table')[1]
        table3 = soup.select('table')[2]
        id_counter = 0
        for items in table1.findAll('tr', style=True)[1:]:
            id_counter += 1     
            updateFirebase(data, items, id_counter)
        for items in table2.findAll('tr', style=True):
            id_counter += 1     
            updateFirebase(data, items, id_counter)
        for items in table3.findAll('tr', style=True):
            id_counter += 1     
            updateFirebase(data, items, id_counter)
            
        db.collection(u'livescore').document(u'spbo').set(data, merge=True)  
        print("PASS")
        
    finally:
        driver.close()
        pass

def updateFirebase(data, items , id_counter):
    td_result = [a.text for a in items.findAll('td')] 
    # FOR 2nd Data of KickOff Time
    kickoff_b = td_result[3] 
    if kickoff_b == "" :
        d3 = "empty"
    else:
        d3 = td_result[3] 
    # FOR SCORE
    score = td_result[5] 
    if score == " - " :

        d5 = "empty"
    else:
        d5 = td_result[5] 

    
    sub_data = {}
    sub_data['id']        = str(id_counter)
    sub_data['league']    = str(td_result[1] )
    sub_data['kickoff_a'] = str(td_result[2] )
    sub_data['kickoff_b'] = str(d3)
    sub_data['team_a']    = str(td_result[4])
    sub_data['score']     = str(d5)
    sub_data['team_b']    = str(td_result[6])
    data[str(id_counter)] = sub_data
    
if __name__ == "__main__":
    triggerCrawl()
