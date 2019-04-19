# 保存预测数据
import requests
import json
import time
import pymysql

# 101021700为杨浦区代码
url='http://www.weather.com.cn/weathern/101021700.shtml'
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}
response=requests.get(url, headers=headers)
response.encoding='utf-8'
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
    if index != length_data-1:
        data24.append(list1[index]+"}")
    if index == length_data-1:
        data24.append(list1[length_data-1])
data24_dict_list = []
for index in range(length_data):
    data24_dict = json.loads(data24[index])
    data24_dict_list.append(data24_dict)

connection = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'root',
    database = 'weather_temp',
    charset = 'utf8'
)
cursor = connection.cursor()

for index in range(len(data24_dict_list)):
    sqlExit = "SELECT * FROM `weather_yangpu`  WHERE date = '%s'" % (data24_dict_list[index]['jf'])
    res = cursor.execute(sqlExit)
    if res:
        print("数据已存在")
    else:
        effect_row = cursor.execute('INSERT INTO `weather_yangpu` (`date`,`temp_pre`) VALUES (%(jf)s, %(jb)s)', data24_dict_list[index])
        connection.commit()
connection.close()
