import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/')
def hello_world():     
#     return 'Hello, World!!!... <br><br> <a href="http://127.0.0.1:5000/GetAPIs">Get APIs Link...</a>'
    return 'Hello, World! <br><br> <a href="https://covid-webapi.herokuapp.com/GetAPIs">Get APIs Link...</a>'



# data = {'GetOverall':'http://127.0.0.1:5000/GetOverall'
#     , 'GetDate':'http://127.0.0.1:5000/GetDate'
#     , 'GetCountryList': 'http://127.0.0.1:5000/GetCountryList'
#     , 'GetCountryReport': 'http://127.0.0.1:5000/GetCountryReport?CountryName=US'
#     , 'GetLatestCountryReport': 'http://127.0.0.1:5000/GetLatestCountryReport?CountryName=US'
#     , 'GetLatestCountryReport with Date (before 4 days)': 'http://127.0.0.1:5000/GetLatestCountryReport?CountryName=INDIA&Date(m/d/yy)=4/3/21'
#     }

# http://127.0.0.1:5000/GetAPIs
@app.route('/GetAPIs',methods=['GET'])
def GetData():
    data = {'GetOverall':'https://covid-webapi.herokuapp.com/GetOverall'
                , 'GetDate':'https://covid-webapi.herokuapp.com/GetDate'
                , 'GetCountryList': 'https://covid-webapi.herokuapp.com/GetCountryList'
                , 'GetCountryReport': 'https://covid-webapi.herokuapp.com/GetCountryReport?CountryName=US'
                , 'GetLatestCountryReport': 'https://covid-webapi.herokuapp.com/GetLatestCountryReport?CountryName=US'
                , 'GetLatestCountryReport with Date (before 4 days)': 'https://covid-webapi.herokuapp.com/GetLatestCountryReport?CountryName=INDIA&Date(m/d/yy)=4/3/21'
                }
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

if __name__=="__main__":
    app.run(debug=True)