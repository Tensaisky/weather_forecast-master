# 得到当前时刻的温度数据
# url 统一资源定位符
#windows+r cmd 打开命令  输入pip install requests 回车
#api.map.baidu.com(百度服务器地址)
#https://blog.csdn.net/dayun555/article/details/79167188
import requests
#引入python中内置的包
import json
import time

city='杨浦'
url='http://api.map.baidu.com/telematics/v3/weather?location=%s&output=json&ak=TueGDhCvwI6fOrQnLM0qmXxY9N0OkOiQ&callback=?'%city
#使用requests发送请求，接受返回的结果
response=requests.get(url)
# print(type(response.text))
#使用loads函数，将json字符串转换为python的字典或列表
rs_dict=json.loads(response.text)
# print(rs_dict)
#取出error
error_code=rs_dict['error']
#如果取出的error为0，表示数据正常，否则没有查询到天气信息
if error_code==0:
#从字典中取出数据
    results=rs_dict['results']
    #根据索引取出城市天气信息字典
    info_dict=results[0]
    #取出天气信息列表
    weather_data=info_dict['weather_data'][0]
    print(weather_data)
date_now = time.strftime('%Y%m%d%H')
pm25=info_dict['pm25']
temp_now = str(weather_data['date']).split('℃')[0].split('实时：')[1]
temp_max = str(weather_data['temperature']).split(' ~ ')[0]
temp_min = str(weather_data['temperature']).split(' ~ ')[1].split('℃')[0]

date_now_dict = {}
keys = ['date','pm25','temp_max','temp_min','temp_now']
values = [date_now,pm25,temp_max,temp_min,temp_now]
date_now_dict = dict(zip(keys,values))
print(date_now_dict)
