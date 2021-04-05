# importing the Libraries
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd

class Covid1():
    global url
    url = 'https://www.mygov.in/corona-data/covid19-statewise-status/'
    def GetOverAllInfo():
        sources = requests.get(url)
        print(sources) 
        soup = BeautifulSoup(sources.content,"html.parser")
        for i in soup.findAll('div',{'class':'field field-name-field-total-vaccinations field-type-text field-label-above'}):
            for j in i.findAll('div',{'class':'field-items'}):
                Total_Vaccinations = j.text
        for i in soup.findAll('div',{'class':'field field-name-field-total-vaccinations-today field-type-text field-label-above'}):
            for j in i.findAll('div',{'class':'field-items'}):
                Total_Vaccinations_Today = j.text
        for i in soup.findAll('div',{'class':'field field-name-field-last-vaccination-date field-type-text field-label-above'}):
            for j in i.findAll('div',{'class':'field-items'}):
                Last_Vaccination_date = j.text

        # looping over each card in a single page
        for card in soup.findAll( 'div',{'class':'content'}):   
            for i in card.findAll('div',{'class':'field field-name-field-covid-india-as-on field-type-text field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    date_time = j.text
            for i in card.findAll('div',{'class':'field field-name-field-district-reporting field-type-text field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    District_Reporting = j.text
            for i in card.findAll('div',{'class':'field field-name-field-last-total-active field-type-number-integer field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    Last_Total_Active_Case = j.text
            for i in card.findAll('div',{'class':'field field-name-field-last-total-cured field-type-number-integer field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    Last_Total_Cured = j.text
            for i in card.findAll('div',{'class':'field field-name-field-last-total-death field-type-number-integer field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    Last_Total_death = j.text
        if sources.status_code==200:
    #         print(sources.status_code)
            data = {'Date Time':date_time
                    ,'District Reporting PDF url':District_Reporting
                    , 'Last Total Active Case':Last_Total_Active_Case
                    , 'Last Total Cured':Last_Total_Cured
                    , 'Last Total death':Last_Total_death
                    , 'Total Vaccinations':Total_Vaccinations
                    , 'Total Vaccinations Today':Total_Vaccinations_Today
                    , 'Last Vaccination date':Last_Vaccination_date
                }
        else:
    #         print(sources.status_code)
            data = {'Data':'data not available'}
        return data

    # GetOverAllInfo()

    def GetStateWiseData():
        STATE_NAME = []
        TOTAL_CONFIRMED = []
        CURED_DISCHARGED_MIGRATED = []
        DEATH = []
        sources = requests.get(url)
        #parsing the whole page
        soup = BeautifulSoup(sources.content,"html.parser")
        for card in soup.findAll( 'div',{'class':"field field-name-field-select-state field-type-list-text field-label-above"}):   
            for i in card.findAll('div',{'class':'field-items'}):
                STATE_NAME.append(i.text)
        for card in soup.findAll( 'div',{'class':"field field-name-field-total-confirmed-indians field-type-number-integer field-label-above"}):   
            for i in card.findAll('div',{'class':'field-items'}):
                TOTAL_CONFIRMED.append(i.text)
        for card in soup.findAll( 'div',{'class':"field field-name-field-cured field-type-number-integer field-label-above"}):   
            for i in card.findAll('div',{'class':'field-items'}):
                CURED_DISCHARGED_MIGRATED.append(i.text)
        for card in soup.findAll( 'div',{'class':"field field-name-field-deaths field-type-number-integer field-label-above"}):   
            for i in card.findAll('div',{'class':'field-items'}):
                DEATH.append(i.text)
                
        if sources.status_code!=200:
            return 'data not available'
        # creating the dataframe and assigning each column with the data from the lists 
        df = pd.DataFrame({
            'STATE_NAME': STATE_NAME,
            'TOTAL_CONFIRMED':TOTAL_CONFIRMED,
            'CURED_DISCHARGED_MIGRATED':CURED_DISCHARGED_MIGRATED,
            'DEATH':DEATH
            })
        return df
    # df = GetStateWiseData()
    #get data in cleaned for States

    def GetStateReport(df, state):
        state1 = state.lower()
        # df = GetStateWiseData()
        if type(df)==str:
            return {'Data':'data not available'}
        sources = requests.get(url)
        #parsing the whole page
        soup = BeautifulSoup(sources.content,"html.parser")
        for card in soup.findAll( 'div',{'class':'content'}):   
            for i in card.findAll('div',{'class':'field field-name-field-covid-india-as-on field-type-text field-label-above'}):
                for j in i.findAll('div',{'class':'field-items'}):
                    date_time = j.text
    #     print(state1)
        temp = df[df['STATE_NAME'].apply(lambda x: state1 == x.lower())]
        if len(temp)==1:
            st_list = list(set(temp['STATE_NAME'].values))
        else:
            df_cntry = df[df['STATE_NAME'].apply(lambda x: state1 in x.lower())]
            st_list = list(set(df_cntry['STATE_NAME'].values))
        states = st_list[0]
        temp2 = df[df['STATE_NAME']==states]
        TOTAL_CONFIRMED = temp2['TOTAL_CONFIRMED'].values[0]
        CURED_DISCHARGED_MIGRATED = temp2['CURED_DISCHARGED_MIGRATED'].values[0]
        DEATH = temp2['DEATH'].values[0]
        data = {'Date Time':date_time
            , 'State':states
            , 'TOTAL_CONFIRMED':TOTAL_CONFIRMED
            , 'CURED_DISCHARGED_MIGRATED':CURED_DISCHARGED_MIGRATED
            , 'DEATH':DEATH
            }
        return data

    # GetStateReport(df, state="maha")
    # data1 = GetStateReport(df, state="maha")
    # data1

