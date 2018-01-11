
# coding: utf-8

# In[552]:


import requests
import pandas as pd
from bs4 import BeautifulSoup
import mechanicalsoup
from datetime import datetime

baseUrl = 'https://salesweb.civilview.com'
url = 'https://salesweb.civilview.com/Sales/SalesSearch?countyId=9'
detailed_url = 'https://salesweb.civilview.com/Sales/SaleDetails?PropertyId=361762545'
url2 = 'https://salesweb.civilview.com/Sales/SalesSearch'
browser = mechanicalsoup.StatefulBrowser()

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


def HTMLTableToDF(table, **kwargs):
    
    n_columns = 0
    n_rows=0
    column_names = []
    listing_url = str()
    
    for row in table.findAll('tr'):

        # Determine the number of rows in the table
        td_tags = row.findAll('td')
        if len(td_tags) > 0:
            n_rows+=1
            if n_columns == 0:
                # Set the number of columns for our table
                n_columns = len(td_tags)

        # Handle column names if we find them
        th_tags = row.findAll('th')
        if len(th_tags) > 0 and len(column_names) == 0:
            for th in th_tags:
                if th.has_attr('class'):
                    column_names.append('Listing URL')
                else:
                    column_names.append(th.text)         

    # Safeguard on Column Titles
    if len(column_names) > 0 and len(column_names) != n_columns:
        raise Exception("Column titles do not match the number of columns")

    columns = column_names if len(column_names) > 0 else range(0,n_columns)
    df = pd.DataFrame(columns = columns,
                      index= range(0,n_rows))
    row_marker = 0
    for row in table.findAll('tr'):
        column_marker = 0
        columns = row.findAll('td')
        for column in columns:
            if column.has_attr('class'):
                listing_url = baseUrl + column.find('a').get('href')
                df.iloc[row_marker,column_marker] = listing_url
            else:
                df.iloc[row_marker,column_marker] = column.text
            column_marker += 1
        if len(columns) > 0:
            row_marker += 1
    print(kwargs)
    print('county' in kwargs.keys())
    if 'county' in kwargs.keys():
        df['County, State'] = kwargs['county']
        df['Status'] = kwargs['status']
    return df


def URLDetails(details_url):
    
    global listingDetails
    global statusTypes
    
    listingDetailsFormatted = [detail.replace(' :', '') for detail in listingDetails]
    listing_details = {detail: None for detail in listingDetailsFormatted}
    
    browser.open(details_url)
    details_soup = browser.get_current_page()
    details_soup_first_table = details_soup.find('table')
    
    n = 0
    n_table = 0
    for table in details_soup.findAll('table'):
        n_table += 1
        if n_table == 1:
            for row in table.findAll('tr'):
                
                test = 0
                n_col = 0
                for column in row.findAll('td'):
                    n_col += 1

                    if column.text in listingDetails and n_col == 1: 
                        details_label = column.text.replace(' :', "")
                        test = 1

                    if n_col == 2 and test == 1:
                        listing_details[details_label] = column.text
                        test = 0

                    if column.text not in listingDetails and n_col == 1:
                        raise Exception('Missing listing details!!! Add ' + column.text + ' to listingDetails!'  )
        if n_table == 2:
            DetailsDF = HTMLTableToDF(table)
            print(DetailsDF)
            statusCount = len(table.findAll('tr'))
            listing_details['Status Count'] = statusCount
            n_row = 0
            for row in table.findAll('tr'):
                n_row += 1
                test = 0
                n_col = 0
                purchased = 0
                for column in row.findAll('td'):
                    n_col += 1

                    if n_col == 1 and column.text not in statusTypes:
                        raise Exception('Missing status type!!! Add ' + column.text + ' to statusTypes!')
                    
                    if n_row == 2 and n_col == 1:
                        listing_details['Latest Status'] = column.text
                        if column.text in purchaseTypes:
                            listing_details['Purchased?'] = 'Yes'
                        else:
                            listing_details['Purchased?'] = 'No'
                        
                    if n_row == 2 and n_col == 2:
                        listing_details['Latest Status Date'] = column.text
                        
                    if n_row == 2 and n_col == 3 and listing_details['Purchased?'] == 'Yes':
                        listing_details['Purchased Amount'] = column.text
                    
                    
        if n_table == 3:
            raise Exception('More than 2 tables on page. Investigate further at ' + browser.get_url())
            
    return listing_details

def HTMLtoDF(url):
    
    startTime = datetime.now()
    
    global RealEstateData
    
    browser.open(url)
    soup = browser.get_current_page()
    
    if 'NJ' not in soup.find('h3').text:
        return print('Not a NJ county.')
    else:
        county_state_title = soup.find('h3').text    
        hyphen_position = county_state_title.find('-')
        county_state = county_state_title[:hyphen_position]
    
    open_table = soup.find('table')
    if open_table == None:
        return print('No open table data.')
    OpenDF = HTMLTableToDF(open_table, county=county_state, status='Open')
    
    browser.select_form()
    
    try:
        browser['IsOpen'] = 'false'
        browser.submit_selected()

    except:
        OpenDF['Status'] = 'Unknown'
    
    closed_soup = browser.get_current_page()
    closed_table = closed_soup.find('table')
    if closed_table == None:
        return print('No closed table data')
    ClosedDF = HTMLTableToDF(closed_table, county=county_state, status='Closed')
    
    UrlDF = pd.concat([OpenDF, ClosedDF], axis=0, ignore_index=True)
    
    DFIndex = UrlDF.index.values
    
    latestStatus = []
    owedAmount = []
    newPlaintiff = []
    newDefendant = []
    purchasedAmount = []
    courtCase = []
    statusCount = []
    
    for index, row in UrlDF.iterrows():
            details = URLDetails(row['Listing URL'])
            latestStatus.append(details['Latest Status'])
            newPlaintiff.append(details['Plaintiff'])
            newDefendant.append(details['Defendant'])
            courtCase.append(details['Court Case #'])
            statusCount.append(details['Status Count'])
            if details['Approx. Judgment*'] == None:
                owedAmount.append(details['Approx. Upset*'])
            else:
                owedAmount.append(details['Approx. Judgment*'])
            if details['Purchased?'] == 'Yes':
                purchasedAmount.append(details['Purchased Amount'])
            else:
                purchasedAmount.append('Not Applicable')
    
    UrlDF['Plaintiff'] = newPlaintiff
    UrlDF['Defendant'] = newDefendant
    
    RealEstateData = pd.concat([RealEstateData, UrlDF.assign(LastStatus=latestStatus, AmountOwed=owedAmount,                                                             PurchasedAmount=purchasedAmount, CourtCase=courtCase,                                                             StatusCount=statusCount)], axis=0, ignore_index=True)
    
    RealEstateData = RealEstateData[['Sales Date', 'Status', 'Sheriff #', 'CourtCase', 'Plaintiff', 'Defendant',                                     'Address', 'County, State', 'LastStatus', 'StatusCount', 'PurchasedAmount',                                     'AmountOwed', 'Listing URL']]
    
    print(datetime.now() - startTime)
    
    return RealEstateData


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

