import requests
import pandas as pd
from bs4 import BeautifulSoup
from utilities.utility import HTMLTableToDF, HTMLtoDF, URLDetails

url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9'
detailed_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=361762545'
baseUrl = 'https://salesweb.civilview.com'

##

RealEstateData = pd.DataFrame()
CountyURLs = {}
listingDetails = ['Sales Date :', 'Sheriff # :', 'Priors :', 'Defendant :', 'Plaintiff :', 'Court Case # :', \
                  'Address :', 'Approx. Judgment* :', 'Attorney :', 'Description :', 'Approx. Upset* :']
statusTypes = ['Pending Bankruptcy', 'Adjourned - Defendant', 'Adjourned - Court', 'Scheduled', \
               'Adjourned - Plaintiff', 'Cancelled/Settled', 'Adjourned - Other', 'Purchased - 3rd Party', \
               'Purchased - Plaintiff', 'Cancelled', 'Indefinite Bankruptcy', 'Vacated', 'Canceled', \
               'Adjournment Plaintiff', 'Adjournment Defendant', 'Purchased - Buy Back', 'Purchased - Third Party', \
               'Settled', 'Bankrupt', 'Reinstated', 'Redeemed', 'Vacate ', 'ADJOURNED DUE TO BANKRUPTCY', \
               'Defendant Adjournment', 'Plaintiff Adjournment', 'Bankruptcy', 'Bankuptcy', \
               'Adjourned per Court Order', 'Buy Back', 'Purchased', 'Sheriff Adjournment', 'On Hold', \
               'Hold In Abeyance', 'Adjourned - Bankruptcy', 'Adjourned - Statuatory', 'Rescheduled', 'Re-Scheduled']
purchaseTypes = ['Purchased - 3rd Party', 'Purchased - Plaintiff', 'Purchased - Buy Back', 'Purchased - Third Party', \
                 'Purchased']

##

r = requests.get(baseUrl)
RealEstateSoup = BeautifulSoup(r.text, 'lxml')

for county in RealEstateSoup.findAll('a'):
    CountyURLs[county.text] = baseUrl + county.get('href')

##

HTMLtoDF(url).to_excel('C:\\Users\\matth\\Desktop\\Real Estate Analysis Ouput.xlsx','Sheet1')

RealEstateData = pd.DataFrame()