import requests
import json
import time
import pymysql
from time import sleep

# 崇明没有pm25数据，用上海数据代替
city1='浦东'
city2='杨浦'
city3='崇明'
city='上海'
url_pudong='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city1
url_yangpu='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city2
url_chongming='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city3
url_shanghai='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city
sql_pudong = "UPDATE `weather_pudong` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"
sql_yangpu = "UPDATE `weather_yangpu` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"
sql_chongming = "UPDATE `weather_chongming` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"
sql_chongming2 = "UPDATE `weather_chongming` set `pm25`=%(pm25)s WHERE DATE = %(date)s"


while(1):
    for index_for_choose in range(4):
        if index_for_choose == 0:
            url = url_pudong
            sql = sql_pudong
        elif index_for_choose == 1:
            url = url_yangpu
            sql = sql_yangpu
        elif index_for_choose == 2:
            url = url_shanghai
            sql = sql_chongming2
        else:
            url = url_chongming
            sql = sql_chongming

        response = requests.get(url)
        rs_dict = json.loads(response.text)
        error_code = rs_dict['error']
        if error_code == 0:
            results = rs_dict['results']
            info_dict = results[0]
            weather_data = info_dict['weather_data'][0]
        date_now = time.strftime('%Y%m%d%H')
        pm25 = info_dict['pm25']
        temp_now = str(weather_data['date']).split('℃')[0].split('实时：')[1]
        temp_max = str(weather_data['temperature']).split(' ~ ')[0]
        temp_min = str(weather_data['temperature']).split(' ~ ')[1].split('℃')[0]

        date_now_dict = {}
        keys = ['date', 'pm25', 'temp_max', 'temp_min', 'temp_now']
        values = [date_now, pm25, temp_max, temp_min, temp_now]
        date_now_dict = dict(zip(keys, values))

        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='weather_temp',
            charset='utf8'
        )
        cursor = connection.cursor()

        effect_row = cursor.execute(sql, date_now_dict)
        connection.commit()
        connection.close()
    sleep(1800)