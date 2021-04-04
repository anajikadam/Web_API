import pandas as pd

class Covid():
    CONF_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
    DEAD_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
    RECV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'

    covid_conf = pd.read_csv(CONF_URL)
    covid_dead = pd.read_csv(DEAD_URL)
    covid_recv = pd.read_csv(RECV_URL)

    #get data in cleaned time series format for country
    def process_data(data,cntry='US',window=3):
        conf_ts = data
        conf_ts_cntry = conf_ts[conf_ts['Country/Region']==cntry]
        final_dataset = conf_ts_cntry.T[4:].sum(axis='columns').diff().rolling(window=window).mean()[40:]
        df = pd.DataFrame(final_dataset,columns=['Total'])
        return df

    #get overall wordlwide total for confirmed, recovered and dead cases
    def get_overall_total(df):
        return df.iloc[:,-1].sum()

    #get total for confirmed, recovered and dead for country 
    # df1,df2,df3 is covid_conf, covid_dead, covid_recv
    def get_cntry_total(df1,df2,df3,cntry='US'):
        conf = df1[df1['Country/Region']==cntry].iloc[:,4:].sum(axis = 1).values[0]
        dead = df2[df2['Country/Region']==cntry].iloc[:,4:].sum(axis = 1).values[0]
        recv = df3[df3['Country/Region']==cntry].iloc[:,4:].sum(axis = 1).values[0]
        return conf,dead,recv

    #get total for confirmed, recovered and dead for country 
    def get_cntry_total_latest(df1,df2,df3,cntry,date):
        conf = df1[df1['Country/Region']==cntry][date].values[0]
        dead = df2[df2['Country/Region']==cntry][date].values[0]
        recv = df3[df3['Country/Region']==cntry][date].values[0]
        return conf,dead,recv

    # get latest Date Report
    def get_Date(df):
        date = df.columns[-1]
        return date

    # select specific country
    def select_cntrys(df,cntry):
        cntry = cntry.lower()
        temp = df[df['Country/Region'].apply(lambda x: cntry == x.lower())]
        if len(temp)==1:
            cntry_list = list(set(temp['Country/Region'].values))
        else:
            df_cntry = df[df['Country/Region'].apply(lambda x: cntry in x.lower())]
            cntry_list = list(set(df_cntry['Country/Region'].values))
        # return only one country
        contry0 = cntry_list[0]
        index = df[df['Country/Region']==contry0].index[0]
        lat = df['Lat'][index]
        Long = df['Long'][index]
        return lat, Long, contry0

    #get total country and names
    def get_cntry_names(df):
        total_cntry = len(set(df['Country/Region']))
        cntrys = list(set(df['Country/Region']))
        return total_cntry, cntrys
    
    date_conf = get_Date(covid_conf)
    date_dead = get_Date(covid_dead)
    date_recv = get_Date(covid_recv)

    conf_overall_total = get_overall_total(covid_conf)
    dead_overall_total = get_overall_total(covid_dead)
    recv_overall_total = get_overall_total(covid_recv)

    cntry = 'India'
    conf_cntry_total, dead_cntry_total, recv_cntry_total = get_cntry_total(
                            covid_conf,covid_dead,covid_recv,cntry)
    # print(f'{cntry} Confirmed:',conf_cntry_total)
    # print(f'{cntry} Dead:',dead_cntry_total)
    # print(f'{cntry} Recovered:',recv_cntry_total)

    cntry = 'India'
    Latest_date = get_Date(covid_conf)
    conf_cntry_total_latest, dead_cntry_total_latest, recv_cntry_total_latest = get_cntry_total_latest(
                            covid_conf, covid_dead, covid_recv, cntry,Latest_date)
    # print(f'{cntry} Confirmed:',conf_cntry_total_latest)
    # print(f'{cntry} Dead:',dead_cntry_total_latest)
    # print(f'{cntry} Recovered:',recv_cntry_total_latest)


