import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

text1 = 'Hello, World! <br><br> <a href="https://covid-webapi.herokuapp.com/GetAPIs">Get APIs Link...</a>'
text2 = 'Hello, World! <br><br> <a href="http://127.0.0.1:5000/GetAPIs">Get APIs Link...</a>'
@app.route('/')
def hello_world():
    return text1

data1 = {'GetOverall':'http://127.0.0.1:5000/GetOverall'
        , 'GetDate':'http://127.0.0.1:5000/GetDate'
        , 'GetCountryList': 'http://127.0.0.1:5000/GetCountryList'
        , 'GetCountryReport': 'http://127.0.0.1:5000/GetCountryReport?CountryName=US'
        , 'GetLatestCountryReport': 'http://127.0.0.1:5000/GetLatestCountryReport?CountryName=US'
        , 'GetLatestCountryReport with Date (before 4 days)': 'http://127.0.0.1:5000/GetLatestCountryReport?CountryName=INDIA&Date(m/d/yy)=4/3/21'
        , 'GetLastCountryReport': 'http://127.0.0.1:5000/GetLastCountryReport'
        , 'GetLatestStateReport': 'http://127.0.0.1:5000/GetLatestStateReport?StateName=Mahar'
        , 'GetCovidCountryReport': 'http://127.0.0.1:5000/GetCovidCountryReport'
        , 'GetStateReport': 'http://127.0.0.1:5000/GetStateReport?StateName=Mahar'
        , 'GetDistrictReport': 'http://127.0.0.1:5000/GetDistrictReport?DistrictName=pune'
        }
data2 = {'GetOverall':'https://covid-webapi.herokuapp.com/GetOverall'
        , 'GetDate':'https://covid-webapi.herokuapp.com/GetDate'
        , 'GetCountryList': 'https://covid-webapi.herokuapp.com/GetCountryList'
        , 'GetCountryReport': 'https://covid-webapi.herokuapp.com/GetCountryReport?CountryName=US'
        , 'GetLatestCountryReport': 'https://covid-webapi.herokuapp.com/GetLatestCountryReport?CountryName=US'
        , 'GetLatestCountryReport with Date (before 4 days)': 'https://covid-webapi.herokuapp.com/GetLatestCountryReport?CountryName=INDIA&Date(m/d/yy)=4/3/21'
        , 'GetLastCountryReport': 'https://covid-webapi.herokuapp.com/GetLastCountryReport'
        , 'GetLatestStateReport': 'https://covid-webapi.herokuapp.com/GetLatestStateReport?StateName=Mahar'
        , 'GetCovidCountryReport': 'https://covid-webapi.herokuapp.com/GetCovidCountryReport'
        , 'GetStateReport': 'https://covid-webapi.herokuapp.com/GetStateReport?StateName=Mahar'
        , 'GetDistrictReport': 'https://covid-webapi.herokuapp.com/GetDistrictReport?DistrictName=pune'
        }
# http://127.0.0.1:5000/GetAPIs
@app.route('/GetAPIs',methods=['GET'])
def GetData():
    data = data2
    return jsonify({'success': True, 'message': "SUCCESS"
                    ,'data':data, 'status': 200})

# http://127.0.0.1:5000/GetDate
@app.route('/GetDate',methods=['GET'])
def GetDate():
    from Data import Covid
    date = Covid.Latest_date
    data = {'Date Format':'m/d/yy'
            , 'Latest Date For Confirmed_global Dataset':Covid.date_conf
            , 'Latest Date For Death_global Dataset':Covid.date_dead
            , 'Latest Date For Recovered_global Dataset':Covid.date_recv
            }
    return jsonify({'success': True, 'message': "SUCCESS"
                    ,'data':data, 'status': 200})  

# http://127.0.0.1:5000/GetCountryList
@app.route('/GetCountryList',methods=['GET'])
def GetCountryList():
    from Data import Covid
    total, cntryList = Covid.get_cntry_names(Covid.covid_conf)
    print(len(cntryList))
    data = {'Total Number of countries Data Available':total
            , 'List of countries name':cntryList
            }
    return jsonify({'success': True, 'message': "SUCCESS"
                    ,'data':data, 'status': 200})  

# http://127.0.0.1:5000/GetOverall
@app.route('/GetOverall',methods=['GET'])
def GetOverall():
    from Data import Covid
    conf_count, conf_date = Covid.GetPeakDataOverAll(Covid.covid_conf)
    death_count, death_date = Covid.GetPeakDataOverAll(Covid.covid_dead)
    recv_count, recv_date =Covid.GetPeakDataOverAll(Covid.covid_recv)
    max = {
            'Confirmed Cases':{'Count':str(conf_count),'Date':str(conf_date)}
            , 'Death cases':{'Count':str(death_count),'Date':str(death_date)}
            , 'Recovered cases':{'Count':str(recv_count),'Date':str(recv_date)}
    }
    data = {
            'Confirmed Cases':str(Covid.conf_overall_total)
            , 'Death cases':str(Covid.dead_overall_total)
            , 'Recovered cases':str(Covid.recv_overall_total)
            }
    return jsonify({'success': True, 'message': "SUCCESS", 'metaData':'Overall Worldwide Cases Report'
                    ,'Max Cases':max
                    ,'data':data, 'status': 200})  

# http://127.0.0.1:5000/GetCountryReport?CountryName=India
@app.route('/GetCountryReport',methods=['GET'])
def GetCountryReport():
    from Data import Covid
    contryName = request.args.get('CountryName', 'India')
    Lat, Long, spc_cntry = Covid.select_cntrys(Covid.covid_conf, contryName)
    conf_cntry_total, dead_cntry_total, recv_cntry_total =Covid.get_cntry_total(
                            Covid.covid_conf,Covid.covid_dead,Covid.covid_recv,spc_cntry)
    conf_count, conf_date = Covid.GetPeakDate(Covid.covid_conf,spc_cntry)
    death_count, death_date = Covid.GetPeakDate(Covid.covid_dead,spc_cntry)
    recv_count, recv_date =Covid.GetPeakDate(Covid.covid_recv,spc_cntry)
    max = {
            'Confirmed Cases':{'Count':str(conf_count),'Date':str(conf_date)}
            , 'Death cases':{'Count':str(death_count),'Date':str(death_date)}
            , 'Recovered cases':{'Count':str(recv_count),'Date':str(recv_date)}
    }
    data = {
            'Confirmed Cases':str(conf_cntry_total)
            , 'Death cases':str(dead_cntry_total)
            , 'Recovered cases':str(recv_cntry_total)
            }
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Cases Report for '+spc_cntry
                    ,'Country Name': spc_cntry
                    ,'Coordinates ': {'Latitude': str(Lat),'Longitude': str(Long)}
                    ,'Max Cases':max
                    ,'data':data, 'status': 200})  

# http://127.0.0.1:5000/GetLatestCountryReport?CountryName=US&Date(m/d/yy)=4/3/21
@app.route('/GetLatestCountryReport',methods=['GET'])
def GetLatestCountryReport():
    from Data import Covid
    cntry = request.args.get('CountryName', 'India')
    date = request.args.get('Date(m/d/yy)', Covid.Latest_date)  
    a = int(date.split('/')[1])    # day in date input
    b = int(Covid.Latest_date.split('/')[1])   # day in date from dataset
    if a>b:
        return jsonify({'success': False, 'message': "Data is not available for the date"
                    , 'status': 300})   
    Lat, Long, spc_cntry = Covid.select_cntrys(Covid.covid_conf, cntry)  
    conf_cntry_total_latest, dead_cntry_total_latest, recv_cntry_total_latest = Covid.get_cntry_total_latest(
                            Covid.covid_conf,Covid.covid_dead,Covid.covid_recv,spc_cntry,date)
    data = {
            'Confirmed Cases':str(conf_cntry_total_latest)
            , 'Death cases':str(dead_cntry_total_latest)
            , 'Recovered cases':str(recv_cntry_total_latest)
            }
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Cases Report for '+spc_cntry+' on Latest Date '+date
                    ,'Country Name': spc_cntry
                    ,'Coordinates ': {'Latitude': str(Lat),'Longitude': str(Long)}
                    ,'data':data, 'status': 200})  

# 'http://127.0.0.1:5000/GetLastCountryReport'
@app.route('/GetLastCountryReport',methods=['GET'])
def GetLastCountryReport():
    from Data1 import Covid1
    data1 = Covid1.GetOverAllInfo()
    data = data1
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Covid-19 Report for India from mygov.in'
                    ,'data':data, 'status': 200}) 

# http://127.0.0.1:5000/GetLatestStateReport?StateName=Mahar
@app.route('/GetLatestStateReport',methods=['GET'])
def GetLatestStateReport():
    stateName = request.args.get('StateName', 'Maharashtra')
    from Data1 import Covid1
    df =  Covid1.GetStateWiseData()
    data1 = Covid1.GetStateReport(df, stateName)
    data = data1
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Covid-19 Report for '+data['State']+' from mygov.in'
                    ,'data':data, 'status': 200}) 

# http://127.0.0.1:5000/GetCovidCountryReport
@app.route('/GetCovidCountryReport',methods=['GET'])
def GetCovidCountryReport():
    from Data2 import Covid2
    data1 = Covid2.GetCovidTotal()
    data = data1
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Covid-19 Report for India from (https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/)'
                    ,'data':data, 'status': 200}) 

# http://127.0.0.1:5000/GetStateReport?StateName=Mahar'
@app.route('/GetStateReport',methods=['GET'])
def GetStateReport():
    stateName = request.args.get('StateName', 'Maharashtra')
    from Data2 import Covid2
    data =  Covid2.GetStateReportFinal(stateName)
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Covid-19 Report District wise for '+data['Detail Data for state']['State Name']+' from from (https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/)'
                    ,'data':data, 'status': 200}) 

# http://127.0.0.1:5000/GetDistrictReport?DistrictName=pune
@app.route('/GetDistrictReport',methods=['GET'])
def GetDistrictReport():
    distName = request.args.get('DistrictName', 'Mumbai')
    from Data2 import Covid2
    data =  Covid2.GetDistrictReportFinal(distName)
    return jsonify({'success': True, 'message': "SUCCESS"
                    , 'metaData':'Overall Covid-19 Report of District '+data['Districts Data']['Districts Name']+' from (https://www.grainmart.in/news/covid-19-coronavirus-india-state-and-district-wise-tally/)'
                    ,'data':data, 'status': 200}) 

if __name__=="__main__":
    app.run(debug=True)