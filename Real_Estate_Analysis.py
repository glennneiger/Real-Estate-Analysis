import requests
import pandas as pd
from bs4 import BeautifulSoup
from utilities.utility import HTMLTableToDF, HTMLtoDF, URLDetails

url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=8'
detailed_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=361762545'
baseUrl = 'https://salesweb.civilview.com'

##

RealEstateData = pd.DataFrame()
CountyURLs = {}

##

r = requests.get(baseUrl)
RealEstateSoup = BeautifulSoup(r.text, 'lxml')

for county in RealEstateSoup.findAll('a'):
    CountyURLs[county.text] = baseUrl + county.get('href')

##

HTMLtoDF(url)