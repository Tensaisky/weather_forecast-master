import requests
import time
from time import sleep
import pymysql

url_yangpu='http://www.tianqi.com/yangpuqu/'
url_pudong='http://www.tianqi.com/pudong/'
url_chongming='http://www.tianqi.com/chongming/'
sql_pudong = "UPDATE `weather_pudong` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"
sql_yangpu = "UPDATE `weather_yangpu` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"
sql_chongming = "UPDATE `weather_chongming` set `pm25`=%(pm25)s,`temp_max`=%(temp_max)s,`temp_min`=%(temp_min)s,`temp_now`=%(temp_now)s WHERE DATE = %(date)s"

while(1):
    for index_for_choose in range(3):
        if index_for_choose == 0:
            url = url_pudong
            sql = sql_pudong
        elif index_for_choose == 1:
            url = url_yangpu
            sql = sql_yangpu
        else:
            url = url_chongming
            sql = sql_chongming
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        start = html.find('<p class="now">')
        start = start + 15
        end = start + 500
        data = html[start:end]
        list_keys = ['pm25','temp_max','temp_min','temp_now']
        temp_now = data.split('</b>')[0].split('b>')[1]
        pm25 = data.split('PM: ')[1].split('</h6>')[0]
        temp_MaxAndMin = data.split('</b>')[2].split('℃')[0]
        temp_min = temp_MaxAndMin.split(' ~ ')[0]
        temp_max = temp_MaxAndMin.split(' ~ ')[1]
        date_now = time.strftime('%Y%m%d%H')
        
        date_now_dict = {}
        keys = ['date','pm25','temp_max','temp_min','temp_now']
        values = [date_now,pm25,temp_max,temp_min,temp_now]
        date_now_dict = dict(zip(keys,values))
        # print(date_now_dict)
        
        connection = pymysql.connect(
            host = 'localhost',
            port = 3306,
            user = 'root',
            password = 'NX_water2018',
            database = 'weather_temp',
            charset = 'utf8'
        )
        cursor = connection.cursor()
        effect_row = cursor.execute(sql,date_now_dict)
        connection.commit()
        connection.close()
    
    sleep(1800)