import requests
import pandas as pd
from bs4 import BeautifulSoup
from utilities.utility import html_table_to_df, html_to_df, url_details

url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=8'
detailed_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=361762545'
baseUrl = 'https://salesweb.civilview.com'

##

RealEstateData = pd.DataFrame()
CountyURLs = {}

##

r = requests.get(url)
RealEstateSoup = BeautifulSoup(r.text, 'lxml')

##

#HTMLtoDF(url)

html_table_to_df(RealEstateSoup.find('table'))