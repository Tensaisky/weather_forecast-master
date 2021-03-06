# 得到未来一段时间的预测温度
import requests
import json

# 101021700为杨浦区代码
# 101021100为崇明
# 101020600为浦东
url='http://www.weather.com.cn/weathern/101021700.shtml'
# url='http://www.weather.com.cn/weathern/101021100.shtml'
# url='http://www.weather.com.cn/weathern/101020600.shtml'
headers = {
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) Chrome/50.0.2661.102'
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Mobile Safari/537.36'
}
response=requests.get(url, headers=headers)
response.encoding='utf-8'
html = response.text
start1 = html.find('var hour3data=[')
# print(len('var hour3data=['))
start2 = start1 + 16
# print(start2)
end = start2 + 1700
# print(end)
hour24_data = html[start2:end]
hour24_data = hour24_data.split('],')[0]
# print(hour24_data)
# print(type(hour24_data))
list1 = hour24_data.split('},')
# print(list1)
# 字符串转成列表
data24 = []
length_data = len(list1)
for index in range(length_data):
    if index != length_data-1:
        data24.append(list1[index]+"}")
    if index == length_data-1:
        data24.append(list1[length_data-1])
# 字符串转成词典
print(data24)
data24_dict_list = []
for index in range(length_data):
    data24_dict = json.loads(data24[index])
    # print(data24_dict)
    data24_dict_list.append(data24_dict)
print(data24_dict_list)
# print('   时间    温度')
# for index in range(len(list1)):
#     print('%s %s'%(data24_dict_list[index]['jf'],data24_dict_list[index]['jb']))
keys_hour24 = []
values_hour24 = []
for index in range(len(data24_dict_list)):
    keys_hour24.append(data24_dict_list[index]['jf'])
    values_hour24.append(data24_dict_list[index]['jb'])
data24_dict_data = dict(zip(keys_hour24,values_hour24))
print(data24_dict_data)