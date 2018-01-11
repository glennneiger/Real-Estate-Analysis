import requests
import pandas as pd
from bs4 import BeautifulSoup
import mechanicalsoup
from datetime import datetime
from utilities.utility import HTMLTableToDF, HTMLtoDF, URLDetails

url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9'
detailed_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=361762545'
url2 = 'https://salesweb.civilview.com/Sales/SalesSearch'
baseUrl = 'https://salesweb.civilview.com'
##

CountyURLs = {}
RealEstateData = pd.DataFrame()
listingDetails = ['Sales Date :', 'Sheriff # :', 'Priors :', 'Defendant :', 'Plaintiff :', 'Court Case # :', 'Address :',                  'Approx. Judgment* :', 'Attorney :', 'Description :', 'Approx. Upset* :']
statusTypes = ['Pending Bankruptcy', 'Adjourned - Defendant', 'Adjourned - Court', 'Scheduled', 'Adjourned - Plaintiff',                'Cancelled/Settled', 'Adjourned - Other', 'Purchased - 3rd Party', 'Purchased - Plaintiff', 'Cancelled',                'Indefinite Bankruptcy', 'Vacated', 'Canceled', 'Adjournment Plaintiff', 'Adjournment Defendant',                'Purchased - Buy Back', 'Purchased - Third Party', 'Settled', 'Bankrupt', 'Reinstated', 'Redeemed',                'Vacate ', 'ADJOURNED DUE TO BANKRUPTCY', 'Defendant Adjournment', 'Plaintiff Adjournment', 'Bankruptcy',                'Bankuptcy', 'Adjourned per Court Order', 'Buy Back', 'Purchased', 'Sheriff Adjournment', 'On Hold',                'Hold In Abeyance', 'Adjourned - Bankruptcy', 'Adjourned - Statuatory', 'Rescheduled', 'Re-Scheduled']
purchaseTypes = ['Purchased - 3rd Party', 'Purchased - Plaintiff', 'Purchased - Buy Back', 'Purchased - Third Party',                 'Purchased']


##


r = requests.get(baseUrl)
RealEstateSoup = BeautifulSoup(r.text, 'lxml')

for county in RealEstateSoup.findAll('a'):
    CountyURLs[county.text] = baseUrl + county.get('href')


##

# In[587]:


RealEstateData = pd.DataFrame()

HTMLtoDF(url).to_excel('C:\\Users\\matth\\Desktop\\Real Estate Analysis Ouput.xlsx','Sheet1')


# In[486]:


RealEstateData = pd.DataFrame()
for url in ['https://salesweb.civilview.com/Sales/SalesSearch?countyId=25',             'https://salesweb.civilview.com/Sales/SalesSearch?countyId=8']:
    HTMLtoDF(url)
    
RealEstateData.to_excel('C:\\Users\\matth\\Desktop\\Real Estate Analysis Ouput.xlsx','Sheet1')


# In[482]:


browser.open(url)
stuff = browser.find_link()
browser.follow_link(stuff)
stuff2 = browser.get_current_page()
stuff3 = stuff2.find('table')
add = 0
for x in stuff3.findAll('td'):
    if add == 1:
        tag_str = str(x)
        tag_str = tag_str.replace('<td>','')
        tag_str = tag_str.replace('</td>', '')
        tag_str_spl = tag_str.split('<br/>')
        print(tag_str_spl)
        #print('Street: ' + tag_str[0])
        #print('City, ZIP: ' + tag_str[1])
        add = 0
    if x.text == 'Address :':
        add = 1

