# importing the Libraries
import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd

class Covid2():
    global url, df11,df22,data1, date1
    url = 'https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/'

    def GetCovidTotal():
        sources = requests.get(url)
        print(sources) 
        if sources.status_code!=200:
            return 'url data not available'
        #parsing the whole page
        soup = BeautifulSoup(sources.content,"html.parser")
        # looping over each card in a single page  
        for i in soup.findAll('div',{'class':'col col-sm contact-section'}):
            date = i.text
        state_list, dist_list = [], []
        for i in soup.findAll('div',{'class':'skgm-td state-td'}):
            state_list.append(i.text.strip())
        for i in soup.findAll('div',{'class':'skgm-tr'}):
            dist_list.append(i.text)
        No_State = len(state_list)
        No_dist = (len(dist_list)-No_State)      # dist_list contain state name alse
        for card in soup.findAll( 'div',{"class":"skgm-th total-cases"}):   
            for i in card.findAll('div',{'class':'td-tc'}):
                Cases = i.text
            for i in card.findAll('div',{'class':'td-tdc'}):
                Last_Cases = i.text
            for i in card.findAll('div',{'class':'td-tr'}):
                Cured = i.text
            for i in card.findAll('div',{'class':'td-tdr'}):
                Last_Cured = (i.text)
            for i in card.findAll('div',{'class':'td-ta'}):
                Active = i.text
            for i in card.findAll('div',{'class':'td-td'}):
                Deaths = i.text
            for i in card.findAll('div',{'class':'td-tdd'}):
                Last_Deaths = i.text
        data = {'Date':date, 'Overall Total':{'Cases':Cases, 'Cured':Cured, 'Active':Active, 'Deaths':Deaths},
                'Last 24 hours Increase':{'Cases':Last_Cases, 'Cured':Last_Cured, 'Deaths':Last_Deaths},
                'In available data':
                {'Number of States and Union Territories of INDIA ':str(No_State),
                'List of States and Union Territories of INDIA ':state_list,
                'Number of Districts and other state':str(No_dist)}
                }
        return data
    # data1 = GetCovidTotal()
    def GetCovidStateData():
        STATE_UT = []
        Cases = []
        Cured = []
        Active = []
        Deaths = []
        Last_Cases = []
        Last_Cured = []
        Last_Deaths = []
        sources = requests.get(url)
        print(sources) 
        if sources.status_code!=200:
            return 'url data not available'
        #parsing the whole page
        soup = BeautifulSoup(sources.content,"html.parser")
        # looping over each card in a single page
        for card in soup.findAll( 'section',{"id":"covid-19-table"}):   
            for i in card.findAll('div',{'class':'skgm-td state-td'}):
                STATE_UT.append(i.text.strip())
            for i in card.findAll('div',{'class':'td-sc'}):
                Cases.append(i.text)
            for i in card.findAll('div',{'class':'td-sdc'}):
                Last_Cases.append(i.text)
            for i in card.findAll('div',{'class':'td-sr'}):
                Cured.append(i.text)
            for i in card.findAll('div',{'class':'td-sdr'}):
                Last_Cured.append(i.text)
            for i in card.findAll('div',{'class':'td-sa'}):
                Active.append(i.text)
            for i in card.findAll('div',{'class':'td-sd'}):
                Deaths.append(i.text)
            for i in card.findAll('div',{'class':'td-sdd'}):
                Last_Deaths.append(i.text)
        # creating the dataframe and assigning each column with the data from the lists 
        df = pd.DataFrame({
            'STATE_UT': STATE_UT,
            'Cases':Cases,
            'Cured':Cured,
            'Active':Active,
            'Deaths':Deaths,
            'New_Cases':Last_Cases,
            'New_Cured':Last_Cured,
            'New_Deaths':Last_Deaths
            })
        df['New_Cases'].replace('','0',inplace=True)
        df['New_Cured'].replace('','0',inplace=True)
        df['New_Deaths'].replace('','0',inplace=True)
        return df

    data1 = GetCovidTotal()
    date1 = data1['Date']
    df11 = GetCovidStateData()
    # df1 = GetCovidStateData()
    def GetCovidDistrictData():
        temp_dist = []
        Districts = []
        Cases = []
        Cured = []
        Active = []
        Deaths = []
        Last_Cases = []
        Last_Cured = []
        Last_Deaths = []
        sources = requests.get(url)
        print(sources)
        if sources.status_code!=200:
            return 'url data not available'
        #parsing the whole page
        soup = BeautifulSoup(sources.content,"html.parser")
        # looping over each card in a single page
        for card in soup.findAll( 'div',{"class":"skgm-districts"}):   
            for i in card.findAll('div',{'class':'skgm-tr'}):
                for i in i.findAll('div',{'class':'skgm-td'}):
                    temp_dist.append(i.text)
            for i in card.findAll('div',{'class':'td-dc'}):
                Cases.append(i.text)
            for i in card.findAll('div',{'class':'td-ddc'}):
                Last_Cases.append(i.text)
            for i in card.findAll('div',{'class':'td-dr'}):
                Cured.append(i.text)
            for i in card.findAll('div',{'class':'td-ddr'}):
                Last_Cured.append(i.text)
            for i in card.findAll('div',{'class':'td-da'}):
                Active.append(i.text)
            for i in card.findAll('div',{'class':'td-dd'}):
                Deaths.append(i.text)
            for i in card.findAll('div',{'class':'td-ddd'}):
                Last_Deaths.append(i.text)
        # Find out only District
        for i in range(0,len(temp_dist),5):
            Districts.append(temp_dist[i])
        # creating the dataframe and assigning each column with the data from the lists 
        df_temp = pd.DataFrame({
            'Districts': Districts,
            'Cases':Cases,
            'Cured':Cured,
            'Active':Active,
            'Deaths':Deaths,
            'New_Cases':Last_Cases,
            'New_Cured':Last_Cured,
            'New_Deaths':Last_Deaths
            })
        df_temp['New_Cases'].replace('','0',inplace=True)
        df_temp['New_Cured'].replace('','0',inplace=True)
        df_temp['New_Deaths'].replace('','0',inplace=True)
        
        df1 = df11    # Get covid state wise data
        if type(df1)==str:
            return'Covid State Data data not available'
        state = list(df1['STATE_UT'])
        num_dist = []
        for card in soup.findAll( 'div',{"class":"skgm-states"}): 
            w = 0
            for i in card.findAll('div',{'class':"skgm-tr"}):
                w+=1
                #print(i.text)
            #print(w-1)       # w-1 because it contain state name also
            num_dist.append(w-1)
        state_list = []
        for index,numb in enumerate(num_dist):
            for j in range(0,numb):
                state_list.append(state[index])
        # final df 
        df = df_temp
        df['STATE_UT'] = state_list
        return df

    
    df22 = GetCovidDistrictData()
    def GetStateReportFinal(state):
        # data1 = Covid2.GetCovidTotal()
        date = date1
        # print(date)
        state1 = state.lower()  # default white space 
        df1 = df11   # Get covid state wise data
        # df1 = Covid2.GetCovidStateData()    # Get covid state wise data
        if type(df1)==str:
            return'Covid State Data data not available'
        df2 = df22   # Get covid District wise data
        if type(df1)==str:
            return'Covid District Data data not available'
        
        temp = df1[df1['STATE_UT'].apply(lambda x: state1 == x.lower())]
        if len(temp)==1:
            st_list = list(set(temp['STATE_UT'].values))
        else:
            df_cntry = df1[df1['STATE_UT'].apply(lambda x: state1 in x.lower())]
            st_list = list(set(df_cntry['STATE_UT'].values))
        states = st_list[0]
        temp2 = df1[df1['STATE_UT']==states]
        temp3 = df2[df2['STATE_UT']==states]
        STATE_UT = temp2['STATE_UT'].values[0]
        Cases = temp2['Cases'].values[0]
        Cured = temp2['Cured'].values[0]
        Active = temp2['Active'].values[0]
        Deaths = temp2['Deaths'].values[0]
        last_Cases = temp2['New_Cases'].values[0]
        last_Cured = temp2['New_Cured'].values[0]
        Last_Deaths = temp2['New_Deaths'].values[0]
        Districts = list(temp3['Districts'].values)
        dist_data = {}
        for i in Districts:
            temp4 = temp3[temp3['Districts']==i]
            Cases1 = temp4['Cases'].values[0]
            Cured1 = temp4['Cured'].values[0]
            Active1 = temp4['Active'].values[0]
            Deaths1 = temp4['Deaths'].values[0]
            last_Cases1 = temp4['New_Cases'].values[0]
            last_Cured1 = temp4['New_Cured'].values[0]
            Last_Deaths1 = temp4['New_Deaths'].values[0]
            dist_data.update({i:{'Cases':Cases1, 'Cured':Cured1, 'Active':Active1, 'Deaths':Deaths1
                                ,'Last 24 hours Increase': {'Cases': last_Cases1,'Cured': last_Cured1, 'Deaths': Last_Deaths1},
                                }})
        data = {'Date Time':date
            , 'Detail Data for state':{'State Name':STATE_UT
            , 'Total Number of Cases':Cases
            , 'Total Number of Cured':Cured
            , 'Total Number of Active':Active
            , 'Total Number of Deaths':Deaths
                ,'Last 24 hours Increase': {'Cases': last_Cases,'Cured': last_Cured, 'Deaths': Last_Deaths},
            }
            , 'Districts':dist_data,
            }
        return data
    # data1 = GetStateReportFinal(state="maha")
    #get data in cleaned for States
    def GetDistrictReportFinal(dist):
        date = date1
        dist1 = dist.lower()  # default white space 

        df2 = df22   # Get covid District wise data
        if type(df2)==str:
            return'Covid District Data data not available'
        
        temp = df2[df2['Districts'].apply(lambda x: dist1 == x.lower())]
        if len(temp)==1:
            dist_list = list(set(temp['Districts'].values))
        else:
            dist_df = df2[df2['Districts'].apply(lambda x: dist1 in x.lower())]
            dist_list = list(set(dist_df['Districts'].values))
        distr = dist_list[0]
        temp2 = df2[df2['Districts']==distr]
        STATE_UT = temp2['STATE_UT'].values[0]
        Districts = temp2['Districts'].values[0]
        Cases = temp2['Cases'].values[0]
        Cured = temp2['Cured'].values[0]
        Active = temp2['Active'].values[0]
        Deaths = temp2['Deaths'].values[0]
        last_Cases = temp2['New_Cases'].values[0]
        last_Cured = temp2['New_Cured'].values[0]
        Last_Deaths = temp2['New_Deaths'].values[0]

        data = {'Date Time':date
            , 'Districts Data':{'Districts Name':Districts, 'State Name': STATE_UT
            , 'Total Number of Cases':Cases
            , 'Total Number of Cured':Cured
            , 'Total Number of Active':Active
            , 'Total Number of Deaths':Deaths
                ,'Last 24 hours Increase': {'Cases': last_Cases,'Cured': last_Cured, 'Deaths': Last_Deaths},
            }
            }
        return data

    # data3 = GetDistrictReportFinal(dist="pune")


    