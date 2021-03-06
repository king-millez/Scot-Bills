from requests import post, get
from bs4 import BeautifulSoup
import json

old_base = 'https://www.parliament.scot'
old_site_base = 'https://www.parliament.scot/parliamentarybusiness/Bills/29732.aspx'
beta_url = 'https://beta.parliament.scot/api/sitecore/BillListing/SearchBills' # POST URL
beta_strip = 'https://beta.parliament.scot'
headers = {'User-Agent': 'Hello from https://github.com/king-millez/Scot-Bills !'}

TITLE = 'title'
URL = 'url'
BILL_TYPE = 'bill_type'
STATUS = 'status'
SESSION = 'session'

class All_Bills(object):
    _bills_data = []

    def __init__(self):
        try:
            self._scrape_old_site()
            self._scrape_beta_site()
        except Exception as e:
            raise Exception('Don\'t worry, the errors don\'t have an accent.\n' + e)
        
    def _scrape_beta_site(self):
        test_soup = BeautifulSoup(post(beta_url, params={
            'X-Requested-With': 'XMLHttpRequest'
        }, headers=headers).text, 'lxml')
        p = test_soup.find_all('p', {'class': 'pagination__title'})[-1]
        page_total = int(p.text.replace('Page: ', '').split(' of ')[-1])
        for page_num in range(page_total):
            soup = BeautifulSoup(post(beta_url + '?class=pagination__link-wrapper&tab1sort=billfullname|asc&tab2sort=billfullname|asc&allpage=' + str(page_num) + '&currentpage=1&currentTab=1&isPaging=True', headers=headers, params={
                'X-Requested-With': 'XMLHttpRequest'
            }).text, 'lxml')
            table = soup.find('div', {'id': 'paneltab2'})
            rows = table.find_all('div', {'class': 'bill-panel u--shadow'})
            for row in rows:
                _bill_title = row.find('a').text.replace('\u2019', '\'')
                _bill_url = beta_strip + row.find('a')['href']
                _bill_type = row.find('p').text
                _bill_status = self.get_status(row.find('text', {'class': 'box__text'}).text)
                bill_dict = {URL: _bill_url, TITLE: _bill_title, SESSION: 5, BILL_TYPE: _bill_type, STATUS: _bill_status}
                self._bills_data.append(bill_dict)
    
    def get_status(self, _input):
        if(isinstance(_input, str)):
            if(_input == 'L'):
                return('Assented')
            elif(_input == '3'):
                return('Stage 3')
            elif(_input == '2'):
                return('Stage 2')
            elif(_input == '1'):
                return('Stage 1')
            elif(_input == 'In'):
                return('Introduced')
            else:
                return('')
        else:
            raise ValueError('Use a str for the bill status...\n' + str(_input))

    def _scrape_old_site(self):
        soup = BeautifulSoup(get(old_site_base, headers=headers).text, 'lxml')
        div = soup.find('div', {'class': 'secondaryContent'})
        for session in div.find_all('div', {'class': 'podHalf'})[1:]:
            session_num = int(session.text[10:][0])
            soup = BeautifulSoup(get(old_base + session.find('a')['href'], headers=headers).text, 'lxml')
            row = soup.find('div', {'class': 'secondaryContent'})
            table = row.find_all('div', {'class': 'podHalf'})
            for row in table:
                _bill_title = row.text.strip()
                _bill_url = old_base + row.find('a')['href']
                bill_dict = {URL: _bill_url, TITLE: _bill_title, SESSION: session_num}
                self._bills_data.append(bill_dict)

    @property
    def data(self):
        return(self._bills_data)

all_bills = All_Bills().data
open('ScotParl.json', 'w').write(json.dumps(all_bills, indent=2))