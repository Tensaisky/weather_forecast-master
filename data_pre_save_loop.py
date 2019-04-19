import requests
import json
from time import sleep
import pymysql

url_yangpu='http://www.weather.com.cn/weathern/101021700.shtml'
url_chongming='http://www.weather.com.cn/weathern/101021100.shtml'
url_pudong='http://www.weather.com.cn/weathern/101020600.shtml'

while(1):
    for index in range(3):
        if index == 0:
            url = url_yangpu
        elif index == 1:
            url = url_chongming
        else:
            url = url_pudong
            
        headers = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        html = response.text
        start1 = html.find('var hour3data=[')
        start2 = start1 + 16
        end = start2 + 1700
        hour24_data = html[start2:end]
        hour24_data = hour24_data.split('],')[0]
        list1 = hour24_data.split('},')
        data24 = []
        length_data = len(list1)
        for index in range(length_data):
            if index != length_data - 1:
                data24.append(list1[index] + "}")
            if index == length_data - 1:
                data24.append(list1[length_data - 1])
        data24_dict_list = []
        for index in range(length_data):
            data24_dict = json.loads(data24[index])
            data24_dict_list.append(data24_dict)
            
        if index == 0:
            sqlExit_yangpu = "SELECT * FROM `weather_yangpu`  WHERE date = '%s'" % (data24_dict_list[index]['jf'])
            sqlUpdate_yangpu = 'INSERT INTO `weather_yangpu` (`date`,`temp_pre`) VALUES (%(jf)s, %(jb)s)'
        elif index == 1:
            sqlExit_chongming = "SELECT * FROM `weather_chongming`  WHERE date = '%s'" % (data24_dict_list[index]['jf'])
            sqlUpdate_chongming = 'INSERT INTO `weather_chongming` (`date`,`temp_pre`) VALUES (%(jf)s, %(jb)s)'
        else:
            sqlExit_pudong = "SELECT * FROM `weather_pudong`  WHERE date = '%s'" % (data24_dict_list[index]['jf'])
            sqlUpdate_pudong = 'INSERT INTO `weather_pudong` (`date`,`temp_pre`) VALUES (%(jf)s, %(jb)s)'

        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='root',
            database='weather_temp',
            charset='utf8'
        )
        cursor = connection.cursor()
        
        for index in range(len(data24_dict_list)):
            sqlExit = sqlExit_pudong
            res = cursor.execute(sqlExit)
            if res:
                # 不知道怎么处理了，不想打印信息
                #  print('数据已存在')
                do_nothing = 0
            else:
                sqlUpdate = sqlUpdate_pudong
                effect_row = cursor.execute(sqlUpdate, data24_dict_list[index])
                connection.commit()
        connection.close()
    print('循环了一次')
    sleep(36000)
    